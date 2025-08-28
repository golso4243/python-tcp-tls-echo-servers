# tcp_echo_server.py
import socket
from datetime import datetime

# Define the server host and port.
# HOST = "0.0.0.0" means the server listens on all available network interfaces.
# PORT = 5000 is the chosen port number to bind the server.
HOST, PORT = "0.0.0.0", 5000

def format_timestamp():
  """Return the current time as a formatted string (HH:MM:SS)."""
  return datetime.now().strftime("%H:%M:%S")

# --- Server Startup Information ---
print()
print("-" * 50)
print(f"TCP Echo Server listening on {HOST}:{PORT}")
print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("-" * 50)

# Create a TCP socket using IPv4 (AF_INET).
# SOCK_STREAM specifies a TCP socket (as opposed to UDP).
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

  # Bind the socket to the host and port.
  s.bind((HOST, PORT))

  # Put the socket into listening mode so it can accept connections.
  s.listen()

  # Server loop: continuously accept incoming client connections.
  while True:

    # Accept an incoming client connection.
    # conn is a new socket object used to communicate with the client.
    # addr contains the client's (IP, port).
    conn, addr = s.accept()
    with conn:

      # Log the connection start with a timestamp.
      connection_start = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
      print(f"\nConnection established from {addr[0]}:{addr[1]} at {connection_start}")

      packet_count = 0  # Track number of packets received from the client.

      # Receive data in chunks of 1024 bytes.
      # The loop continues until the client closes the connection (recv returns empty).
      while data := conn.recv(1024):

        # Increment the packet counter for each successful packet from the client.
        packet_count += 1

        # Send the same data back to the client (echo).
        conn.sendall(data)

      # Log the connection closure with timestamp and packet count.
      connection_end = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
      print(f"Connection closed at {connection_end}")
      print(f"Total packets: {packet_count}")
      print()
