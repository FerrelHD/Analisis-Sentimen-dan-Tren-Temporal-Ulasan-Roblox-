import os
import sys

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.scraper import scrape_roblox_reviews

if __name__ == "__main__":
    scrape_roblox_reviews()
