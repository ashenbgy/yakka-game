#!/usr/bin/env python3
"""Yaksha Kombat LAN server.

Serves the game files (like `python3 -m http.server`) and relays LAN
multiplayer messages between two browsers over a WebSocket at /ws.
Standard library only.

    python3 server.py            # port 8000 (next free port if busy)
    python3 server.py 9000       # a specific port
"""
import base64
import hashlib
import http.server
import json
import os
import random
import socket
import struct
import sys
import threading

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"

rooms = {}  # code -> {"host": Client, "guest": Client | None}
lock = threading.Lock()


class Client:
    def __init__(self, sock):
        self.sock = sock
        self.send_lock = threading.Lock()
        self.room = None
        self.partner = None

    def send(self, text):
        data = text.encode()
        n = len(data)
        if n < 126:
            head = struct.pack("!BB", 0x81, n)
        elif n < 65536:
            head = struct.pack("!BBH", 0x81, 126, n)
        else:
            head = struct.pack("!BBQ", 0x81, 127, n)
        try:
            with self.send_lock:
                self.sock.sendall(head + data)
        except OSError:
            pass

    def send_json(self, **msg):
        self.send(json.dumps(msg))


def recv_exact(sock, n):
    buf = b""
    while len(buf) < n:
        chunk = sock.recv(n - len(buf))
        if not chunk:
            raise ConnectionError
        buf += chunk
    return buf


def recv_message(sock):
    """Return the next text message, None on close. Handles fragmentation and pings."""
    parts = []
    while True:
        b1, b2 = recv_exact(sock, 2)
        fin, opcode = b1 & 0x80, b1 & 0x0F
        n = b2 & 0x7F
        if n == 126:
            n = struct.unpack("!H", recv_exact(sock, 2))[0]
        elif n == 127:
            n = struct.unpack("!Q", recv_exact(sock, 8))[0]
        mask = recv_exact(sock, 4) if b2 & 0x80 else b"\0\0\0\0"
        payload = bytearray(recv_exact(sock, n))
        for i in range(n):
            payload[i] ^= mask[i % 4]
        if opcode == 0x8:  # close
            return None
        if opcode == 0x9:  # ping -> pong
            sock.sendall(struct.pack("!BB", 0x8A, len(payload)) + bytes(payload))
            continue
        if opcode in (0x0, 0x1, 0x2):
            parts.append(bytes(payload))
            if fin:
                return b"".join(parts).decode(errors="replace")


def leave(c):
    with lock:
        room = rooms.get(c.room)
        if room:
            if room["host"] is c or room["guest"] is c:
                rooms.pop(c.room, None)
        partner, c.partner = c.partner, None
    if partner:
        partner.partner = None
        partner.send_json(t="left")


def handle_ws(sock):
    c = Client(sock)
    try:
        while True:
            text = recv_message(sock)
            if text is None:
                break
            if c.partner:  # paired: relay everything verbatim
                c.partner.send(text)
                continue
            try:
                msg = json.loads(text)
            except ValueError:
                continue
            if msg.get("t") == "host":
                with lock:
                    code = str(random.randint(1000, 9999))
                    while code in rooms:
                        code = str(random.randint(1000, 9999))
                    rooms[code] = {"host": c, "guest": None}
                    c.room = code
                c.send_json(t="room", code=code)
            elif msg.get("t") == "join":
                code = str(msg.get("code", "")).strip()
                with lock:
                    room = rooms.get(code)
                    ok = room is not None and room["guest"] is None
                    if ok:
                        room["guest"] = c
                        c.room = code
                        host = room["host"]
                        c.partner, host.partner = host, c
                if ok:
                    host.send_json(t="paired", role="host")
                    c.send_json(t="paired", role="guest")
                else:
                    c.send_json(t="nojoin")
    except (ConnectionError, OSError):
        pass
    finally:
        leave(c)
        try:
            sock.close()
        except OSError:
            pass


class Handler(http.server.SimpleHTTPRequestHandler):
    extensions_map = {**http.server.SimpleHTTPRequestHandler.extensions_map,
                      ".glb": "model/gltf-binary", ".fbx": "application/octet-stream",
                      ".hdr": "application/octet-stream", ".svg": "image/svg+xml"}

    def do_GET(self):
        if self.path == "/ws" and self.headers.get("Upgrade", "").lower() == "websocket":
            key = self.headers["Sec-WebSocket-Key"]
            accept = base64.b64encode(hashlib.sha1((key + GUID).encode()).digest()).decode()
            self.send_response(101, "Switching Protocols")
            self.send_header("Upgrade", "websocket")
            self.send_header("Connection", "Upgrade")
            self.send_header("Sec-WebSocket-Accept", accept)
            self.end_headers()
            self.wfile.flush()
            self.connection.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            self.close_connection = True
            handle_ws(self.connection)
            return
        super().do_GET()

    def log_message(self, fmt, *args):
        pass  # keep the console readable


def lan_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("10.255.255.255", 1))  # no packet is sent; just picks the LAN interface
        return s.getsockname()[0]
    except OSError:
        return "127.0.0.1"
    finally:
        s.close()


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    server = None
    for port in [PORT] if len(sys.argv) > 1 else range(PORT, PORT + 20):
        try:
            server = http.server.ThreadingHTTPServer(("0.0.0.0", port), Handler)
            PORT = port
            break
        except OSError:
            print(f"Port {port} is busy (another server is using it).", flush=True)
    if server is None:
        sys.exit("No free port found. Stop the other server (Ctrl+C in its terminal) or pass a port: python3 server.py 9000")
    server.daemon_threads = True
    print("Yaksha Kombat server running", flush=True)
    print(f"  This PC:        http://localhost:{PORT}", flush=True)
    print(f"  Other LAN PCs:  http://{lan_ip()}:{PORT}", flush=True)
    print("Press Ctrl+C to stop.", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.", flush=True)
