# tls_echo_server.py
import socket
import ssl
from datetime import datetime


# Define the server host and port.
# HOST = "0.0.0.0" means the server listens on all available network interfaces.
# PORT = 5443 is chosen for secure TLS connections (commonly used for HTTPS).
HOST = "0.0.0.0"
PORT = 5443


def format_timestamp():
  """Return the current time as a formatted string (HH:MM:SS)."""
  return datetime.now().strftime("%H:%M:%S")


# --- TLS Context Setup ---
# Create a new SSLContext configured for TLS server operations.
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)

# Load the server's certificate and private key.
# - cert.pem must contain a valid X.509 certificate.
# - key.pem must contain the corresponding private key.
context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")

# --- Server Startup Information ---
print()
print("-" * 50)
print(f"TLS Echo Server listening on {HOST}:{PORT}")
print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("-" * 50)

# Create a raw TCP socket first.
with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:

  # Bind the socket to the host and port.
  sock.bind((HOST, PORT))

  # Allow up to 5 pending connection requests (backlog).
  sock.listen(5)

  # Wrap the TCP socket with TLS to secure communication.
  with context.wrap_socket(sock, server_side=True) as ssock:

    # Main server loop: continuously accept TLS client connections.
    while True:

      # Accept an incoming TLS client connection.
      conn, addr = ssock.accept()
      with conn:

        # Log the connection start with a timestamp.
        connection_start = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\nTLS connection established from {addr[0]}:{addr[1]} at {connection_start}")

        packet_count = 0  # Track number of messages received.

        # Receive and echo data until the client disconnects.
        while True:

          # Read up to 4096 bytes at a time.
          data = conn.recv(4096)
          if not data:
            break  # Exit loop if client closes the connection.

              # Increment the packet counter for each packet received from the client.
              packet_count += 1
              
              # Echo the received data back to the client.
              conn.sendall(data)

              # Log the connection closure with timestamp and packet count.
              connection_end = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
              print(f"TLS connection closed at {connection_end}")
              print(f"Total packets: {packet_count}")
              print()
