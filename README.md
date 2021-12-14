# Amazon-Scraper
Scrape amazon.com using Scrapy in Python to get product details of all categories.

## HOW TO RUN?
- Clone the repository.
- Navigate to the Amazon_Scraper folder in terminal.
- Run the command `scrapy crawl amazon_spider -o filename.csv` to run the crawler

## REQUIREMENTS
- Python 3
- Scrapy module for python `pip install Scrapy`
- Install these two modules to get around amazon captcha, it makes amazon think that requests are coming from multiple users `pip install scrapy-fake-useragent` `pip install scrapy-user-agents`
