from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/")
def index():
    return app.send_static_file("index.html")

@app.route("/fetch-data", methods=["POST"])
def fetch_data():
    ticker = request.form["ticker"]

    # Yahoo Finance scraping
    url = f"https://finance.yahoo.com/quote/{ticker}/key-statistics?p={ticker}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    pe_ratio = soup.find("td", {"data-test": "PE_RATIO-value"}).text
    pb_ratio = soup.find("td", {"data-test": "PB_RATIO-value"}).text

    # SEC Edgar scraping
    url = f"https://www.sec.gov/cgi-bin/browse-edgar?CIK={ticker}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    debt = soup.find("td", text="Long-Term Debt").find_next_sibling("td").text
    cash = soup.find("td", text="Cash and cash equivalents").find_next_sibling("td").text
    equity = soup.find("td", text="Total Equity").find_next_sibling("td").text

    # Free cash flow scraping from Yahoo Finance
    url = f"https://finance.yahoo.com/quote/{ticker}/cash-flow?p={ticker}
