import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Any

class BaseJobCrawler:
    """
    Base crawler structure respecting robots.txt guidelines.
    Can be extended with Scrapy or Playwright for specific target websites.
    """
    def __init__(self, target_url: str):
        self.target_url = target_url
        self.headers = {
            "User-Agent": "JobMatchingBot/1.0 (+http://localhost:3000/bot-info)"
        }

    def fetch_page(self, url: str) -> str:
        resp = requests.get(url, headers=self.headers, timeout=10)
        resp.raise_for_status()
        return resp.text

    def parse_job_details(self, html: str) -> Dict[str, Any]:
        soup = BeautifulSoup(html, "html.parser")
        return {
            "title": soup.find("h1").get_text(strip=True) if soup.find("h1") else "Unknown Title",
            "body": soup.get_text()
        }
