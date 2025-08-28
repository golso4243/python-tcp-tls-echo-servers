# tls_echo_client.py
import socket
import ssl
import time
from datetime import datetime

# Define the server IP and port to connect to.
# Must match the TLS echo server's configuration.
SERVER_IP = "YOUR_SERVER_IP"
PORT = 5443

# Sample sensitive-looking data to simulate sending over a network.
# NOTE: These are only placeholders and should never be sent in plain text
# in a real-world application. They are for demonstration purposes only.
sensitive_data = [
  "LOGIN: admin:password123",
  "SSN: 123-45-6789",
  "CREDIT_CARD: 4111-1111-1111-1111",
  "API_KEY: sk_live_51H1234567890abcdefghijklmnopqrstuvwxyz",
  "PASSWORD: SuperSecretPassword2024!",
  "EMAIL: john.doe@company.com",
  "PHONE: +1-555-123-4567",
  "ADDRESS: 123 Main St, Anytown, USA 12345",
  "BANK_ACCOUNT: 9876543210",
  "SSH_PRIVATE_KEY: -----BEGIN OPENSSH PRIVATE KEY-----"
]

# --- TLS Context Setup ---
# Create a default SSL context configured for client use.
context = ssl.create_default_context()

# For lab/testing purposes, disable certificate verification and hostname check.
# WARNING: Never disable these checks in production environments!
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

# Optional: log TLS session secrets so tools like Wireshark can decrypt traffic.
# A file named "tls_secrets.log" will be created in the working directory.
context.keylog_filename = "tls_secrets.log"

# Establish a plain TCP connection first.
with socket.create_connection((SERVER_IP, PORT)) as sock:

  # Wrap the TCP socket with TLS using the SSL context.
  # The server_hostname parameter is required by the SSL library, even if
  # hostname verification is disabled.
  with context.wrap_socket(sock, server_hostname="pc1.local") as ssock:

    # Log the connection establishment time.
    connection_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print()
    print(f"TLS connection established to {SERVER_IP}:{PORT} at {connection_time}")

    packets_sent = 0  # Track the number of packets sent.

    # Iterate through each item in the sensitive_data list.
    for data in sensitive_data:

      # Encode the string into bytes.
      msg = f"{data}".encode()

      # Send the message securely to the server.
      ssock.sendall(msg)

      # Receive the echoed response (up to 4096 bytes).
      response = ssock.recv(4096)

      # Increment the packet counter based on packets sent to server.
      packets_sent += 1

      # Delay 1 second to make traffic easier to observe in monitoring tools.
      time.sleep(1)

    # Log the disconnection time and packet summary.
    disconnect_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"TLS connection closed at {disconnect_time}")
    print(f"Total packets sent: {packets_sent}")
    print()
