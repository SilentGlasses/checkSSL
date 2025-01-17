```
┌─┐┬ ┬┌─┐┌─┐┬┌─╔═╗╔═╗╦  
│  ├─┤├┤ │  ├┴┐╚═╗╚═╗║  
└─┘┴ ┴└─┘└─┘┴ ┴╚═╝╚═╝╩═╝
```

**Secure Sockets Layer** (SSL) certificates are a cornerstone of online security, ensuring that data exchanged between a user's browser and a website is encrypted and secure. These digital certificates authenticate the identity of a website, instilling trust in users by confirming that they are interacting with a legitimate entity. By enabling HTTPS (Hypertext Transfer Protocol Secure), SSL certificates safeguard sensitive information, such as login credentials, financial transactions, and personal data, from being intercepted by malicious actors. In today’s digital landscape, where cybersecurity threats are increasingly sophisticated, SSL certificates are essential for maintaining privacy, fostering trust, and ensuring regulatory compliance for businesses and individuals alike.

## Why is SSL important to security and risk managment

SSL (Secure Sockets Layer) is a critical component of modern security and risk management strategies. It provides encryption for data in transit, ensuring that sensitive information—such as passwords, credit card numbers, and personal details—remains private and protected from eavesdropping or interception. This encryption reduces the risk of data breaches, a major concern for organizations and individuals alike.

From a risk management perspective, SSL helps mitigate threats such as man-in-the-middle attacks, session hijacking, and impersonation by verifying the authenticity of websites through digital certificates. This authentication fosters trust between users and online platforms, an essential factor for businesses that handle sensitive transactions or user data.

Additionally, SSL compliance is often mandated by regulations like GDPR, HIPAA, and PCI DSS, making it a necessary component of legal and operational risk management. Without SSL, organizations expose themselves to reputational damage, financial penalties, and the potential loss of customer trust. By implementing SSL, businesses not only strengthen their security posture but also proactively address critical risks in an evolving threat landscape.

Maintaining their validity and security is critical:

1. **Trust and Authentication**: Certificates verify the identity of websites, servers, or systems, preventing impersonation and man-in-the-middle attacks. An expired or compromised certificate undermines trust, causing users or systems to question the authenticity of the connection.
2. **Data Encryption**: Certificates enable secure communication through encryption protocols like TLS/SSL. Invalid certificates can lead to unencrypted connections, exposing sensitive data to attackers.
3. **Compliance Requirements**: Many industries have strict compliance regulations (e.g., GDPR, PCI DSS) that mandate the use of valid, secure certificates to protect data. Non-compliance can result in legal and financial consequences.
4. **Avoiding Downtime**: Expired certificates can disrupt services, resulting in loss of business, customer dissatisfaction, and reputational damage. Proactively managing certificate renewals helps prevent such issues.
5. **Mitigating Security Risks**: Compromised certificates can be exploited for phishing, spoofing, or other malicious activities. Regularly updating and properly managing certificates minimizes these risks.

## Best Practices

- Monitor certificate expiration dates.
- Automate renewal processes where possible.
- Use strong cryptographic algorithms.
- Revoke and replace compromised certificates immediately.

# The Script

## Features

- **Domain Validation**: Validates domain existence before checking SSL certificates.
- **Expiration Checks**: Reports the number of days remaining until expiration.
- **Thresholds**: Configurable warning and critical thresholds for expiration alerts.
- **Email Notifications**: Sends email alerts for domains with certificates nearing expiration.
- **Concurrency**: Uses multithreading for faster processing.
- **Logging**: Logs all errors to a file and prints domain-specific errors in a human-readable format in the terminal.

## Requirements

- Python 3.8 or higher

Required Python libraries:

- ssl
- socket
- yaml
- smtplib
- email
- termcolor
- tabulate
- concurrent.futures

### Dependencies

- Install dependencies manually:
```
pip3 install termcolor tabulate pyyaml
```
- Install using requirments file:
```
pip3 install -r requirements.txt 
```

## Setup

### Configuration File

Create a `config.yaml` file in the script directory with the following structure:

```
warning_threshold: 30    # Days before expiration to trigger a warning
critical_threshold: 10   # Days before expiration to trigger a critical alert
smtp:
  smtp_server: "smtp.example.com"
  smtp_port: 587
  use_tls: true
  sender_email: "your_email@example.com"
  recipient_email: "recipient_email@example.com"
  username: "your_username"
  password: "your_password"
domain_file: "domains.txt"  # Path to the file containing the list of domains
```

### Domains File

Create a `domains.txt` file listing the domains to check, one per line:

```
example.com
example.org
example.net
```

## Usage

You can run the script two ways in your Terminal.

- Using the python Command:
```
python ssl_cert_checker.py
```
- Using the Script’s Filename Directly:
```
./ssl_cert_checker.py
```

### Terminal Output

The script displays a table of results:

```
Domain             Expiry Date    Days Remaining    Status
example.com        2024-01-31     15                WARNING
example.org        2024-05-15     120               OK
example.net        2024-01-20     5                 CRITICAL
```

If errors occur, they are displayed after the results in a human-readable format:

```
Domain/Certificate Errors:
Domain validation failed: invalid-domain.com
Failed to check certificate for expired-domain.com: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed (_ssl.c:1123)
```

### Logs

All errors are logged in `ssl_checker.log`.

### Email Alerts

If any domains have a "WARNING" or "CRITICAL" status, an email is sent to the configured recipient.

## Notes

- Ensure the SMTP credentials in the `config.yaml` file are correct for email functionality.
- Adjust the `warning_threshold` and `critical_threshold` as needed.

## Contributing

If you'd like to contribute, please fork the repository and create a pull request with your changes.

## License

This project is licensed under the MIT License.
