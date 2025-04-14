import requests
from bs4 import BeautifulSoup
import re
import time
import random
from urllib.parse import urlparse

class ReviewScraper:
    """
    A class for scraping product reviews from e-commerce websites.
    Currently supports Amazon, Best Buy, and Walmart.
    """
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
        }
    
    def scrape(self, url, min_count=30, max_pages=5):
        """
        Scrape reviews from the given product URL.
        
        Args:
            url (str): The product URL to scrape reviews from.
            min_count (int): Minimum number of reviews to collect.
            max_pages (int): Maximum number of pages to scrape.
            
        Returns:
            list: A list of dictionaries containing review data.
        """
        domain = urlparse(url).netloc
        
        if 'amazon' in domain:
            return self._scrape_amazon(url, min_count, max_pages)
        elif 'bestbuy' in domain:
            return self._scrape_bestbuy(url, min_count, max_pages)
        elif 'walmart' in domain:
            return self._scrape_walmart(url, min_count, max_pages)
        else:
            # In a real implementation, we'd raise an exception here
            # For demo purposes, we'll return mock data
            return self._get_mock_reviews(min_count)
    
    def _scrape_amazon(self, url, min_count, max_pages):
        """
        Scrape reviews from Amazon product page.
        """
        # In a real implementation, this would contain actual Amazon scraping logic
        # For demonstration purposes, we'll return mock data
        return self._get_mock_reviews(min_count)
    
    def _scrape_bestbuy(self, url, min_count, max_pages):
        """
        Scrape reviews from Best Buy product page.
        """
        # In a real implementation, this would contain actual Best Buy scraping logic
        # For demonstration purposes, we'll return mock data
        return self._get_mock_reviews(min_count)
    
    def _scrape_walmart(self, url, min_count, max_pages):
        """
        Scrape reviews from Walmart product page.
        """
        # In a real implementation, this would contain actual Walmart scraping logic
        # For demonstration purposes, we'll return mock data
        return self._get_mock_reviews(min_count)
    
    def _get_mock_reviews(self, count):
        """
        Generate mock reviews for demonstration purposes.
        
        Args:
            count (int): Number of mock reviews to generate.
            
        Returns:
            list: A list of dictionaries containing mock review data.
        """
        positive_reviews = [
            "This product exceeded my expectations! The quality is outstanding and it works exactly as described.",
            "I've been using this for a month now and I'm very satisfied with my purchase. Highly recommended!",
            "Great value for the price. This product does everything I need it to do and more.",
            "I bought this as a gift for my husband and he absolutely loves it. Works perfectly!",
            "The customer service was excellent and the product arrived earlier than expected. Very happy!"
        ]
        
        negative_reviews = [
            "Don't waste your money on this product. It broke after just a week of light use.",
            "The quality is much lower than advertised. I'm very disappointed with this purchase.",
            "This product doesn't work as described. I've tried everything but can't get it to function properly.",
            "I received a defective item and the company wouldn't refund me. Terrible experience!",
            "Save your money and look elsewhere. This product is cheaply made and not worth the price."
        ]
        
        suspicious_reviews = [
            "Best product ever!!!! Changed my life!!!! Will buy again and again!!!! Five stars!!!!!",
            "I received this product for free in exchange for my honest review. It's amazing and perfect in every way!",
            "Just received this amazing product today and it's already the best purchase I've ever made!!",
            "WOW!!! This is INCREDIBLE!!! Cannot believe how PERFECT this is!!!! BUY IT NOW!!!!",
            "This product cured all my problems! It's the most incredible invention of the century! Life-changing!!!"
        ]
        
        reviews = []
        for i in range(count):
            # Randomize review types with more genuine reviews than suspicious
            review_type = random.choices(
                ["positive", "negative", "suspicious"], 
                weights=[0.4, 0.4, 0.2], 
                k=1
            )[0]
            
            if review_type == "positive":
                text = random.choice(positive_reviews)
                rating = random.randint(4, 5)
            elif review_type == "negative":
                text = random.choice(negative_reviews)
                rating = random.randint(1, 2)
            else:
                text = random.choice(suspicious_reviews)
                rating = 5
                
            # Add some random text to make each review unique
            text += f" [{random.randint(1000, 9999)}]"
            
            reviews.append({
                "text": text,
                "rating": rating,
                "date": f"2023-{random.randint(1, 12)}-{random.randint(1, 28)}",
                "verified_purchase": random.random() > 0.3,
                "helpful_votes": random.randint(0, 100) if random.random() > 0.7 else 0,
                "reviewer": f"User{random.randint(1000, 9999)}",
                "reviewer_history": {
                    "total_reviews": random.randint(1, 50),
                    "avg_rating": round(random.uniform(3.0, 5.0), 1),
                    "verified_purchases": random.randint(0, 30)
                }
            })
            
        return reviews
