import xml.etree.ElementTree as ET
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from datetime import datetime, timezone
import base64
import argparse
import subprocess
from rich.console import Console
from rich.table import Table
from rich.text import Text

# Initialize the console for rich output
console = Console()


# Function to copy XML file from the server using SCP
def copy_xml_from_server(user, server_ip, remote_path, local_path):
    try:
        # Construct the scp command
        scp_command = f"scp {user}@{server_ip}:{remote_path} {local_path}"

        # Execute the scp command
        subprocess.run(scp_command, shell=True, check=True)
        console.print(f"[green]Successfully copied XML file from {server_ip}.[/green]")
    except subprocess.CalledProcessError as e:
        console.print(f"[red]Error: {e}[/red]")


# Function to extract certificates from XML
def extract_certificates_from_xml(file):
    tree = ET.parse(file)
    root = tree.getroot()

    certificates = []
    for cert_elem in root.findall('.//ds:X509Certificate', namespaces={'ds': 'http://www.w3.org/2000/09/xmldsig#'}):
        cert_base64 = cert_elem.text.strip()
        certificates.append(cert_base64)

    return certificates


# Function to check certificate validity
def check_certificate_validity(cert_base64):
    cert_der = base64.b64decode(cert_base64)

    cert = x509.load_der_x509_certificate(cert_der, default_backend())

    # Getting current date in UTC
    current_date = datetime.now(timezone.utc)

    # Extracting Subject
    subject = cert.subject.rfc4514_string()

    # Validity check
    if cert.not_valid_before_utc <= current_date <= cert.not_valid_after_utc:
        warning_period = cert.not_valid_after_utc - cert.not_valid_before_utc
        return (True, cert.not_valid_before_utc, cert.not_valid_after_utc, subject, warning_period)
    else:
        return (False, cert.not_valid_before_utc, cert.not_valid_after_utc, subject, None)


# Function to validate certificates in XML
def validate_certificates_in_xml(file):
    certificates = extract_certificates_from_xml(file)

    # Create a table for output
    table = Table(title="Certificate Validity Report")

    table.add_column("Subject", style="cyan", justify="left")
    table.add_column("Valid From", style="green")
    table.add_column("Valid Until", style="red")
    table.add_column("Remaining Validity", style="blue", justify="center")
    table.add_column("Status", style="yellow", justify="center")

    for cert_base64 in certificates:
        is_valid, valid_from, valid_until, subject, warning_period = check_certificate_validity(cert_base64)

        status = "Valid" if is_valid else "Invalid"
        status_color = "green" if is_valid else "red"

        # Prepare warning period display
        warning_period_display = str(warning_period.days) + " days" if warning_period else "N/A"

        # Add a row to the table
        table.add_row(
            Text(subject, style="cyan"),
            Text(str(valid_from), style=status_color),
            Text(str(valid_until), style=status_color),
            Text(warning_period_display, style="blue"),
            Text(status, style=status_color)
        )

    # Print the table to console
    console.print(table)


# Main function to handle arguments and execution flow
def main():
    parser = argparse.ArgumentParser(description="Validate certificates in an XML file.")
    parser.add_argument('user', type=str, help='Username for the server')
    parser.add_argument('server_ip', type=str, help='IP address of the server')
    parser.add_argument('remote_path', type=str, help='Path to the XML file on the server')
    parser.add_argument('local_path', type=str, help='Local path to save the XML file')

    args = parser.parse_args()

    # Copy XML file from the server
    copy_xml_from_server(args.user, args.server_ip, args.remote_path, args.local_path)

    # Validate certificates in the copied XML file
    validate_certificates_in_xml(args.local_path)


# Entry point
if __name__ == "__main__":
    main()
