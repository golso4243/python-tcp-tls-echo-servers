# Python TCP/TLS Echo Servers and Clients

<br>

Minimal Python implementations of TCP and TLS echo servers and clients.
Designed for networking labs and packet capture analysis in Wireshark to demonstrate plaintext vs encrypted traffic.

<br>

Full lab walk-through on [Medium](https://medium.com/@gage.a.olson/observing-plaintext-vs-encrypted-traffic-with-python-and-wireshark-a-hands-on-lab-af007c3461a5).

<br>

## Features

- **TCP Echo Server** → echoes data over plaintext TCP.

- **TCP Echo Client** → sends sensitive-looking test data in plaintext.

- **TLS Echo Server** → echoes data securely using a self-signed certificate.

- **TLS Echo Client** → transmits the same data over TLS with optional key logging for Wireshark.

- Logging of connection times and packet counts for visibility.

<br>

## Why

- Show how **plaintext traffic exposes sensitive data** (credentials, API keys, etc.).

- Contrast with **TLS-encrypted traffic**, where payloads are unreadable in Wireshark.

- Educational use only — not production-ready.

<br>

## Setup

### 1. Generate Self-Signed Certificate

``` Shell 
openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days 365 -nodes -subj "/CN=pc1.local"
```
This will create `cert.pem` and `key.pem` for the TLS server. **These two files must reside in the same folder as the tls_echo_server.py file.** 

<br>

### 2. Run a Server

TCP Server
``` Bash
python tcp_echo_server.py
```

TLS Server
``` Bash
python tls_echo_server.py
```

<br>

### 3. Run a Client

TCP (Plaintext) Client
``` Bash
python tcp_echo_client.py
```

TLS (encrypted) Client
``` Bash
python tls_echo_client.py
```

<br>

## Wireshark
### Packet Capture

1. Start a capture on the interface your client/server use.

2. Use filters to isolate traffic:

IP filter:
``` ini
host 192.168.x.x and host 192.168.x.x
```

TCP Echo Server/Client (port 5000):
``` ini
tcp.port == 5000
```

TLS Echo Server/Client (port 5443):
``` ini
tcp.port == 5443
```

### Observations

- With the **TCP client/server**, payloads (login, SSN, API keys, etc.) are visible in plaintext.
- With the **TLS client/server**, payloads appear encrypted and unreadable.
- If you set tls_secrets.log, load it into Wireshark (Preferences → Protocols → TLS → (Pre)-Master-Secret log filename) to decrypt TLS sessions for lab analysis.

<br>

## Notes

- For **educational use only** — do not use with real sensitive data.
- Blocking, single-threaded design (one client at a time).
- Production-ready systems require concurrency, proper error handling, and verified certificates.

<br>

## License
This project is provided under the MIT License.















