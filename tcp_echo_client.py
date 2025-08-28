# tcp_echo_client.py
import socket
import time
from datetime import datetime

# Define the server IP and port that the client will connect to.
SERVER_IP = "YOUR_SERVER_IP"
PORT = 5000

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

# # Create a TCP socket using IPv4 (AF_INET).
# The context manager ensures the socket closes automatically.
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

  # Connect to the echo server.
  s.connect((SERVER_IP, PORT))

  # Log the connection start time.
  connection_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  print()
  print(f"Connected established to {SERVER_IP}:{PORT} at {connection_time}")

  packets_sent = 0  # Track number of packets sent to the server.

  # Iterate through each item in the sensitive_data list.
  for i, data in enumerate(sensitive_data):

    # Convert the string to bytes before sending.
    msg = f"{data}".encode()

    # Send the encoded message to the server.
    s.sendall(msg)

    # Receive the echoed response (up to 1024 bytes).
    response = s.recv(1024)

    # Increment the packet counter for each successful send.
    packets_sent += 1

    # Delay 1 second between sends to make traffic easier to observe.
    time.sleep(1)
  
  # Log disconnection time and summary statistics.
  disconnect_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  print(f"Connection closed at {disconnect_time}")
  print(f"Total packets sent: {packets_sent}")
  print()
