# phishforge
Project scaffold for phishforge
# PhishForge: Terminal-Based Phishing Simulation Toolkit

**PhishForge** is a lightweight, Python-based tool for creating realistic phishing simulations directly from the Linux terminal. It generates professional-looking login pages for major brands (Google, Microsoft, PayPal), captures submitted credentials, and logs all activity in real-time.

Designed for **educational purposes**, **security awareness training**, and **red team exercises**, PhishForge helps security professionals and students understand how attackers craft convincing social engineering attacks.

## 🚀 Features
- **Zero Dependencies:** Uses only the Python standard library. No `pip install` required.
- **Realistic Templates:** High-fidelity HTML/CSS replicas of Google, Microsoft, and PayPal login pages.
- **Credential Capture:** Logs all submitted credentials (email, password, session IDs) to a local JSON file.
- **Link Generator:** Automatically generates short, realistic-looking URLs for your simulation.
- **LAN & Local Testing:** Works on `localhost` or your local network IP for immediate testing.
- **Tunnel-Ready:** Designed to work seamlessly with `ngrok` or `cloudflared` for public internet exposure.

## 🛠️ Requirements
- **Python 3.6+**
- **Linux, macOS, or Windows** (with WSL recommended for Linux)
- **Optional:** `ngrok` or `cloudflared` for public URL generation

## 📦 Installation
No installation required. Just clone the repository:

```bash
git clone https://github.com/Rajakumar45/phishforge.git
cd phishforge
python3 phishforge.py --template google --port 8080

Captured data is logged to logs/captures.log in real-time.

{
  "timestamp": "2024-05-20 14:32:01",
  "ip": "192.168.1.105",
  "path": "/secure-session",
  "data": {
    "email": "user@example.com",
    "password": "P@ssw0rd123"
  }
}

🎛️ Advanced Usage

Using ngrok for Public Access
# Terminal 1: Start PhishForge
python3 phishforge.py --template microsoft

# Terminal 2: Start ngrok tunnel
ngrok http 8080
