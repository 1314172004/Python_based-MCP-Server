Crypto Market MCP Server

A Python-based MCP (Model Context Protocol) server that provides:

✔ Real-time cryptocurrency ticker data

✔ Historical data (via CCXT)

✔ FastAPI REST endpoints

✔ Error handling

✔ Caching layer

✔ Full test coverage using pytest

✔ Ready to deploy on any system

🔧 Tech Stack

Python 3.10+

FastAPI

CCXT (exchange API wrapper)

Uvicorn

propcache (TTL caching)

Pytest

📦 Installation

Clone the repository:

git clone <your_repo_link>
cd assignment1


Create virtual environment:

python -m venv .venv


Activate it:

Windows:

.venv\Scripts\activate


Mac/Linux:

source .venv/bin/activate


Install dependencies:

pip install -r requirements.txt

🚀 Running the Server
uvicorn app.main:app --reload


Visit:

http://127.0.0.1:8000


You should see:

{"message": "Crypto MCP Server running"}

📡 API Endpoints
1. Health Check
GET /

2. Live Ticker
GET /ticker/{exchange}/{symbol}


Example:

/ticker/binance/BTC-USDT

🧪 Running Tests
pytest -q


Expected output:

2 passed

📁 Project Structure
assignment1/
│── app/
│   ├── __init__.py
│   ├── main.py
│   ├── fetcher.py
│   └── cache.py
│── tests/
│   └── test_main.py
│── requirements.txt
│── README.md

✔ Notes & Assumptions

CCXT is used for exchange communication.

Caching implemented using propcache (TTL: 5 seconds).

Server is intentionally simple for internship assignment.

Fully tested and ready to deploy.

👨‍💻 Author

Aswini