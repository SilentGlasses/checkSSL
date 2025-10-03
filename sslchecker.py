#!/usr/bin/env python3

import ssl
import socket
import yaml
import smtplib
from email.mime.text import MIMEText
from termcolor import colored
from datetime import datetime
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from tabulate import tabulate

def load_config(file_path):
    try:
        with open(file_path, 'r') as file:
            return yaml.safe_load(file)
    except Exception as e:
        logging.error(f"Failed to load config file: {e}")
        return None

def load_domains(file_path):
    try:
        with open(file_path, 'r') as file:
            return [line.strip() for line in file if line.strip()]
    except Exception as e:
        logging.error(f"Failed to load domains file: {e}")
        return []

def validate_domain(domain):
    try:
        socket.gethostbyname(domain)
        return True
    except socket.gaierror:
        error_message = f"Domain validation failed: {domain}"
        logging.error(error_message)
        return error_message

def check_certificate(domain, port=443):
    try:
        context = ssl.create_default_context()
        context.minimum_version = ssl.TLSVersion.TLSv1_2
        with socket.create_connection((domain, port)) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                expiry_date = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                return {
                    'domain': domain,
                    'expiry_date': expiry_date,
                    'remaining_days': (expiry_date - datetime.now()).days
                }
    except Exception as e:
        error_message = f"Failed to check certificate for {domain}: {e}"
        logging.error(error_message)
        return error_message

def send_email(smtp_config, expiring_domains):
    try:
        msg_content = "\n".join([f"{d['domain']} expires on {d['expiry_date']} ({d['remaining_days']} days remaining)" for d in expiring_domains])
        msg = MIMEText(msg_content)
        msg['Subject'] = "SSL Certificate Expiration Alert"
        msg['From'] = smtp_config['sender_email']
        msg['To'] = smtp_config['recipient_email']

        with smtplib.SMTP(smtp_config['smtp_server'], smtp_config['smtp_port']) as server:
            if smtp_config.get('use_tls', False):
                server.starttls()
            if smtp_config.get('username') and smtp_config.get('password'):
                server.login(smtp_config['username'], smtp_config['password'])
            server.send_message(msg)
        print(colored("Email sent successfully.", "green"))
    except Exception as e:
        logging.error(f"Failed to send email: {e}")

def process_domain(domain, warning_threshold, critical_threshold):
    domain_validation_result = validate_domain(domain)
    if domain_validation_result is True:
        cert_info = check_certificate(domain)
        if isinstance(cert_info, dict):
            remaining_days = cert_info['remaining_days']

            if remaining_days <= critical_threshold:
                status = "CRITICAL"
                color = "red"
            elif remaining_days <= warning_threshold:
                status = "WARNING"
                color = "yellow"
            else:
                status = "OK"
                color = "green"

            return {
                'domain': domain,
                'expiry_date': cert_info['expiry_date'].strftime('%Y-%m-%d'),
                'remaining_days': remaining_days,
                'status': status,
                'color': color
            }
        elif isinstance(cert_info, str):
            return cert_info  # Error message
    elif isinstance(domain_validation_result, str):
        return domain_validation_result  # Error message
    return None

def main():
    logging.basicConfig(filename='ssl_checker.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

    config = load_config('config.yaml')
    if not config:
        return

    domain_file = config.get('domain_file', 'domains.txt')
    domains = load_domains(domain_file)
    smtp_config = config.get('smtp', {})
    warning_threshold = config.get('warning_threshold', 30)
    critical_threshold = config.get('critical_threshold', 7)

    results = []
    expiring_domains = []
    errors = []

    with ThreadPoolExecutor() as executor:
        future_to_domain = {executor.submit(process_domain, domain, warning_threshold, critical_threshold): domain for domain in domains}
        for future in as_completed(future_to_domain):
            domain = future_to_domain[future]
            try:
                result = future.result()
                if isinstance(result, dict):
                    results.append(result)
                    if result['status'] in ["CRITICAL", "WARNING"]:
                        expiring_domains.append(result)
                elif isinstance(result, str):
                    errors.append(result)
            except Exception as e:
                error_message = f"Unexpected error processing {domain}: {e}"
                logging.error(error_message)
                errors.append(error_message)

    # Display results in a tabular format without borders
    table = []
    for result in results:
        table.append([
            result['domain'],
            result['expiry_date'],
            result['remaining_days'],
            colored(result['status'], result['color'])
        ])
    print(tabulate(table, headers=["Domain", "Expiry Date", "Days Remaining", "Status"], tablefmt="plain"))

    # Display errors related to domains or certificates
    if errors:
        print("\nDomain/Certificate Errors:")
        for error in errors:
            print(colored(error, "red"))

    if expiring_domains:
        send_email(smtp_config, expiring_domains)

if __name__ == "__main__":
    main()
