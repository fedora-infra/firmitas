#!/usr/bin/env python

import sys
from cryptography import x509
from cryptography.hazmat.backends import default_backend
import requests
from datetime import datetime, timedelta


def check_ssl_certificate(crt_url):
    try:
        # Get Certificate from URL
        response = requests.get(crt_url)
        certificate = response.text

        # Load and parse the certificate
        cert_data = x509.load_pem_x509_certificate(certificate.encode(), default_backend())

        # Get the common name (CN) from the certificate
        common_name = cert_data.subject.rfc4514_string()

        # Check the validity dates of the certificate
        not_after = cert_data.not_valid_after

        # Calculate the number of days remaining until the expiration date
        days_left = (not_after - datetime.now()).days

        # Print the certificate details
        print(f"Common Name (CN): {common_name}")
        print(f"Days Remaining until Expiration: {days_left}")

        # Check if expiration is within 30 days
        if days_left <= 30:
            print("Certificate expiration within 10 days!")

    except requests.exceptions.RequestException as e:
        print("Error downloading the certificate:", e)
    except Exception as e:
        print("Error loading or parsing the certificate:", e)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python script.py <crt_url>")
    else:
        crt_url = sys.argv[1]
        check_ssl_certificate(crt_url)
