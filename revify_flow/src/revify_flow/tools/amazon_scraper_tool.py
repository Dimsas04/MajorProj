# from typing import Optional
# from crewai.tools import tool
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from bs4 import BeautifulSoup
# import time
# import os
# import sys
# import pandas as pd
# from dotenv import load_dotenv

# @tool()
# class AmazonScraperTool():
#     name: str = "amazon_scraper_tool"
#     description: str = "Scrapes customer reviews from Amazon product pages"

#     def __init__(self):
#         super().__init__(
#             name=self.name,
#             description=self.description,
#             func=self._scrape_reviews
#         )
        
#         # Load environment variables
#         load_dotenv()
#         self.username = os.getenv('NUMBER')
#         self.password = os.getenv('PASSWORD')
        
#         # Check if credentials are available
#         if not self.username or not self.password:
#             print("⚠️ Error: Missing credentials in .env file")
#             print("Please ensure your .env file contains:")
#             print("NUMBER=your_email_or_phone_number")
#             print("PASSWORD=your_amazon_password")

#     def __call__(self, url: str) -> str:
#         # wrap your existing `_scrape_reviews()` here
#         return self._scrape_reviews(url)

#     def _scrape_reviews(self, url: str, target_reviews: int = 50, product_name: Optional[str] = None) -> str:
#         """
#         Scrape reviews from Amazon product page
        
#         Args:
#             url: Amazon product URL
#             target_reviews: Number of reviews to scrape (default: 50)
#             product_name: Optional name to use for the product (default: extracted from page)
            
#         Returns:
#             Path to the CSV file containing the scraped reviews
#         """
#         # Check for credentials
#         if not self.username or not self.password:
#             return "Error: Missing Amazon credentials in .env file"
        
#         print(f"Starting to scrape {target_reviews} reviews from: {url}")
        
#         # Set up the driver and scrape reviews
#         try:
#             reviews_titles, reviews_texts, ratings = self._perform_scraping(url, target_reviews)
            
#             # Save to CSV
#             if not product_name:
#                 product_name = "Amazon Product"  # Default name if not provided
                
#             csv_path = self._save_to_csv(reviews_titles, reviews_texts, ratings, product_name)
            
#             return f"Successfully scraped {len(reviews_texts)} reviews. Data saved to {csv_path}"
        
#         except Exception as e:
#             return f"Error during scraping: {str(e)}"

#     def _perform_scraping(self, url, target_reviews):
#         """Internal method to handle the actual scraping logic"""
#         driver = self._setup_driver()
#         review_titles = []
#         reviews = []
#         ratings = []

#         try:
#             print(f"Opening URL: {url}")
#             driver.get(url)

#             # Wait and click on the "See all reviews" link
#             print("Looking for 'See all reviews' link...")
#             WebDriverWait(driver, 20).until(
#                 EC.element_to_be_clickable((By.XPATH, '//*[@id="reviews-medley-footer"]/div[2]/a'))
#             ).click()
            
#             # Wait for email input field and enter email
#             print("Logging in with provided credentials...")
#             email_input = WebDriverWait(driver, 20).until(
#                 EC.presence_of_element_located((By.ID, "ap_email_login"))
#             )
#             print(f"Using username: {self.username[:2]}...{self.username[-2:]}")
#             email_input.send_keys(self.username)
            
#             enter_button = WebDriverWait(driver, 20).until(
#                 EC.element_to_be_clickable((By.ID, "continue"))
#             )
#             enter_button.click()
            
#             password_input = WebDriverWait(driver, 20).until(
#                 EC.presence_of_element_located((By.ID, "ap_password"))
#             )
#             password_input.send_keys(self.password)
            
#             sign_in_button = WebDriverWait(driver, 20).until(
#                 EC.element_to_be_clickable((By.ID, "signInSubmit"))
#             )
#             sign_in_button.click()
            
#             page_count = 1
#             max_pages = 10  # Maximum number of pages to scrape
            
#             # Continue until we reach target_reviews or max_pages
#             while len(reviews) < target_reviews and page_count <= max_pages:
#                 print(f"Scraping page {page_count}...")
#                 # Wait for reviews to load
#                 time.sleep(5)  # Give more time for page to load
                
#                 tables = driver.page_source
                
#                 soup = BeautifulSoup(tables, 'html.parser')
#                 ret_bodies = soup.find_all('span', {'data-hook': 'review-body'})
#                 ret_titles = soup.find_all('a', {'data-hook': 'review-title'})  
#                 ret_ratings = soup.find_all('span', class_='a-icon-alt')
                
#                 print(f"Found {len(ret_bodies)} reviews on this page")
                
#                 # Process found reviews up to target_reviews
#                 for i in range(min(len(ret_bodies), target_reviews - len(reviews))):
#                     review_titles.append(ret_titles[i].text.strip())
#                     reviews.append(ret_bodies[i].text.strip())
#                     ratings.append(ret_ratings[i].text.strip())
                
#                 # Stop if we've reached our target
#                 if len(reviews) >= target_reviews:
#                     print(f"✅ Reached target of {target_reviews} reviews.")
#                     break
                    
#                 # Try to go to next page
#                 try:
#                     print("Looking for next page button...")
#                     next_button = WebDriverWait(driver, 10).until(
#                         EC.element_to_be_clickable((By.CSS_SELECTOR, "li.a-last a"))
#                     )
#                     next_button.click()
#                     page_count += 1
#                     time.sleep(2)  # Brief pause after clicking
#                 except Exception as e:
#                     print(f"No more pages available: {str(e)}")
#                     break
                    
#             print(f"Scraping complete. Retrieved {len(reviews)} reviews.")
            
#         except Exception as e:
#             print(f"Error during scraping: {str(e)}")
#         finally:
#             driver.quit()
        
#         # Limit to target_reviews in case we got more
#         return review_titles[:target_reviews], reviews[:target_reviews], ratings[:target_reviews]

#     def _setup_driver(self):
#         """Set up the Selenium WebDriver with appropriate options"""
#         chrome_options = Options()
#         chrome_options.add_argument('--disable-gpu')
#         chrome_options.add_argument('--disable-dev-shm-usage')
#         chrome_options.add_argument('--no-sandbox')
#         chrome_options.add_argument('--log-level=3')  # Minimize logging
#         chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
#         chrome_options.add_experimental_option('useAutomationExtension', False)
#         chrome_options.add_experimental_option("detach", True)  # Keep browser open after script finishes
#         prefs = {
#             "credentials_enable_service": False,         # Disables the password manager
#             "profile.password_manager_enabled": False    # Disables the password manager UI
#         }
#         chrome_options.add_experimental_option("prefs", prefs)
        
#         return webdriver.Chrome(options=chrome_options)

#     def _save_to_csv(self, titles, reviews, ratings, product_name="Amazon Product"):
#         """Save reviews to CSV in format compatible with preprocessing.ipynb"""
#         # Create a DataFrame
#         df = pd.DataFrame({
#             "id": range(1, len(titles) + 1),
#             "name": product_name,
#             "brand": "Amazon",
#             "categories": "Product",
#             "primaryCategories": "Product",
#             "reviews.doRecommend": [True if r.startswith("5") or r.startswith("4") else False for r in ratings],
#             "reviews.rating": [float(r.split()[0]) if r and r[0].isdigit() else 0 for r in ratings],
#             "reviews.text": reviews,
#             "reviews.title": titles
#         })
        
#         # Save to CSV
#         filename = "scraped_reviews.csv"
#         df.to_csv(filename, index=False)
#         print(f"✅ Saved {len(df)} reviews to {filename}")
#         return filename

from typing import ClassVar, Optional, Dict, Any, Type
from pydantic import BaseModel, Field, PrivateAttr
from crewai.tools import BaseTool
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import os
import pandas as pd
from dotenv import load_dotenv

# Define the input schema using Pydantic
class AmazonScraperSchema(BaseModel):
    url: str = Field(
        description="Amazon product URL to scrape reviews from"
    )
    target_reviews: int = Field(
        default=50,
        description="Number of reviews to scrape",
        ge=1,  # Greater than or equal to 1
        le=500  # Less than or equal to 500
    )
    product_name: Optional[str] = Field(
        default=None,
        description="Optional name to use for the product (default: extracted from page)"
    )

class AmazonScraperTool(BaseTool):
    """Tool that scrapes customer reviews from Amazon product pages"""
    
    # name: ClassVar[str] = "amazon_scraper_tool"
    # description: ClassVar[str] = "Scrapes customer reviews from Amazon product pages"
    # args_schema: Type[BaseModel] = AmazonScraperSchema
    name: str = "amazon_scraper_tool"
    description: str = "Scrapes customer reviews from Amazon product pages"
    args_schema: Type[BaseModel] = AmazonScraperSchema

    

    # Use class variables to store credentials
    # _username: str = PrivateAttr()
    # _password: str = PrivateAttr()

    def __init__(self):
        # First initialize the parent class
        super().__init__()

        # Load environment variables
        load_dotenv()
        self._username = os.getenv('NUMBER')
        self._password = os.getenv('PASSWORD')
        # Store credentials as class variables, not instance attributes
        # AmazonScraperTool._username = os.getenv('NUMBER')
        # AmazonScraperTool._password = os.getenv('PASSWORD')
        
        
        

        # Check if credentials are available
        if not self._username or not self._password:
            print("⚠️ Error: Missing credentials in .env file")
            print("Please ensure your .env file contains:")
            print("NUMBER=your_email_or_phone_number")
            print("PASSWORD=your_amazon_password")
        # Check if credentials are available
        # if not AmazonScraperTool._username or not AmazonScraperTool._password:
        #     print("⚠️ Error: Missing credentials in .env file")
        #     print("Please ensure your .env file contains:")
        #     print("NUMBER=your_email_or_phone_number")
        #     print("PASSWORD=your_amazon_password")
            
        # Initialize the parent class
        # super().__init__()
    
    def _run(self, url: str, target_reviews: int = 50, product_name: Optional[str] = None) -> str:
        """Run the tool with the given inputs."""
        # Check for credentials
        if not self._username or not self._password:
            return "Error: Missing Amazon credentials in .env file"
        # Check for credentials
        # if not AmazonScraperTool._username or not AmazonScraperTool._password:
        #     return "Error: Missing Amazon credentials in .env file"
        
        print(f"Starting to scrape {target_reviews} reviews from: {url}")
        
        # Set up the driver and scrape reviews
        try:
            reviews_titles, reviews_texts, ratings = self._perform_scraping(url, target_reviews)
            
            # Save to CSV
            if not product_name:
                product_name = "Amazon Product"  # Default name if not provided
                
            csv_path = self._save_to_csv(reviews_titles, reviews_texts, ratings, product_name)
            
            return f"Successfully scraped {len(reviews_texts)} reviews. Data saved to {csv_path}"
        
        except Exception as e:
            return f"Error during scraping: {str(e)}"

    def _perform_scraping(self, url, target_reviews):
        """Internal method to handle the actual scraping logic"""
        driver = self._setup_driver()
        review_titles = []
        reviews = []
        ratings = []

        try:
            print(f"Opening URL: {url}")
            driver.get(url)

            # Wait and click on the "See all reviews" link
            print("Looking for 'See all reviews' link...")
            WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="reviews-medley-footer"]/div[2]/a'))
            ).click()
            
            # Wait for email input field and enter email
            print("Logging in with provided credentials...")
            email_input = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.ID, "ap_email_login"))
            )
            print(f"Using username: {self._username[:2]}...{self._username[-2:]}")
            email_input.send_keys(self._username)
            
            enter_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.ID, "continue"))
            )
            enter_button.click()
            
            password_input = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.ID, "ap_password"))
            )
            password_input.send_keys(self._password)
            
            sign_in_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.ID, "signInSubmit"))
            )
            sign_in_button.click()
            
            page_count = 1
            max_pages = 10  # Maximum number of pages to scrape
            
            # Continue until we reach target_reviews or max_pages
            while len(reviews) < target_reviews and page_count <= max_pages:
                print(f"Scraping page {page_count}...")
                # Wait for reviews to load
                time.sleep(5)  # Give more time for page to load
                
                tables = driver.page_source
                
                soup = BeautifulSoup(tables, 'html.parser')
                ret_bodies = soup.find_all('span', {'data-hook': 'review-body'})
                ret_titles = soup.find_all('a', {'data-hook': 'review-title'})  
                ret_ratings = soup.find_all('span', class_='a-icon-alt')
                
                print(f"Found {len(ret_bodies)} reviews on this page")
                
                # Process found reviews up to target_reviews
                for i in range(min(len(ret_bodies), target_reviews - len(reviews))):
                    review_titles.append(ret_titles[i].text.strip())
                    reviews.append(ret_bodies[i].text.strip())
                    ratings.append(ret_ratings[i].text.strip())
                
                # Stop if we've reached our target
                if len(reviews) >= target_reviews:
                    print(f"✅ Reached target of {target_reviews} reviews.")
                    break
                    
                # Try to go to next page
                try:
                    print("Looking for next page button...")
                    next_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "li.a-last a"))
                    )
                    next_button.click()
                    page_count += 1
                    time.sleep(2)  # Brief pause after clicking
                except Exception as e:
                    print(f"No more pages available: {str(e)}")
                    break
                    
            print(f"Scraping complete. Retrieved {len(reviews)} reviews.")
            
        except Exception as e:
            print(f"Error during scraping: {str(e)}")
        finally:
            driver.quit()
        
        # Limit to target_reviews in case we got more
        return review_titles[:target_reviews], reviews[:target_reviews], ratings[:target_reviews]

    def _setup_driver(self):
        """Set up the Selenium WebDriver with appropriate options"""
        chrome_options = Options()
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--log-level=3')  # Minimize logging
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        prefs = {
            "credentials_enable_service": False,         # Disables the password manager
            "profile.password_manager_enabled": False    # Disables the password manager UI
        }
        chrome_options.add_experimental_option("prefs", prefs)
        
        return webdriver.Chrome(options=chrome_options)

    def _save_to_csv(self, titles, reviews, ratings, product_name="Amazon Product"):
        """Save reviews to CSV in format compatible with preprocessing.ipynb"""
        # Create a DataFrame
        df = pd.DataFrame({
            "id": range(1, len(titles) + 1),
            "name": product_name,
            "brand": "Amazon",
            "categories": "Product",
            "primaryCategories": "Product",
            "reviews.doRecommend": [True if r.startswith("5") or r.startswith("4") else False for r in ratings],
            "reviews.rating": [float(r.split()[0]) if r and r[0].isdigit() else 0 for r in ratings],
            "reviews.text": reviews,
            "reviews.title": titles
        })
        
        # Save as reviews_cleaned.csv for compatibility with existing code
        compatibility_filename = "scraped_reviews.csv"
        df.to_csv(compatibility_filename, index=False)
        print(f"✅ Saved {len(df)} reviews to {compatibility_filename} for analysis")
        
        return compatibility_filename




# from typing import Optional
# from langchain.tools import tool
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from bs4 import BeautifulSoup
# import time
# import os
# import pandas as pd
# from dotenv import load_dotenv

# # Load environment variables once at module level
# load_dotenv()
# _USERNAME = os.getenv('NUMBER')
# _PASSWORD = os.getenv('PASSWORD')

# @tool
# def amazon_scraper_tool(url: str, target_reviews: int = 50, product_name: Optional[str] = None) -> str:
#     """Scrapes customer reviews from Amazon product pages.
    
#     Args:
#         url: Amazon product URL to scrape reviews from
#         target_reviews: Number of reviews to scrape (default: 50, max: 500)
#         product_name: Optional name to use for the product (default: extracted from page)
        
#     Returns:
#         Path to the CSV file containing the scraped reviews
#     """
#     # Check for credentials
#     if not _USERNAME or not _PASSWORD:
#         return "Error: Missing Amazon credentials in .env file"
    
#     print(f"Starting to scrape {target_reviews} reviews from: {url}")
    
#     # Set up the driver and scrape reviews
#     try:
#         reviews_titles, reviews_texts, ratings = _perform_scraping(url, target_reviews)
        
#         # Save to CSV
#         if not product_name:
#             product_name = "Amazon Product"  # Default name if not provided
            
#         csv_path = _save_to_csv(reviews_titles, reviews_texts, ratings, product_name)
        
#         return f"Successfully scraped {len(reviews_texts)} reviews. Data saved to {csv_path}"
    
#     except Exception as e:
#         return f"Error during scraping: {str(e)}"

# def _perform_scraping(url, target_reviews):
#     """Internal method to handle the actual scraping logic"""
#     driver = _setup_driver()
#     review_titles = []
#     reviews = []
#     ratings = []

#     try:
#         print(f"Opening URL: {url}")
#         driver.get(url)

#         # Wait and click on the "See all reviews" link
#         print("Looking for 'See all reviews' link...")
#         WebDriverWait(driver, 20).until(
#             EC.element_to_be_clickable((By.XPATH, '//*[@id="reviews-medley-footer"]/div[2]/a'))
#         ).click()
        
#         # Wait for email input field and enter email
#         print("Logging in with provided credentials...")
#         email_input = WebDriverWait(driver, 20).until(
#             EC.presence_of_element_located((By.ID, "ap_email_login"))
#         )
#         print(f"Using username: {_USERNAME[:2]}...{_USERNAME[-2:]}")
#         email_input.send_keys(_USERNAME)
        
#         enter_button = WebDriverWait(driver, 20).until(
#             EC.element_to_be_clickable((By.ID, "continue"))
#         )
#         enter_button.click()
        
#         password_input = WebDriverWait(driver, 20).until(
#             EC.presence_of_element_located((By.ID, "ap_password"))
#         )
#         password_input.send_keys(_PASSWORD)
        
#         sign_in_button = WebDriverWait(driver, 20).until(
#             EC.element_to_be_clickable((By.ID, "signInSubmit"))
#         )
#         sign_in_button.click()
        
#         page_count = 1
#         max_pages = 10  # Maximum number of pages to scrape
        
#         # Continue until we reach target_reviews or max_pages
#         while len(reviews) < target_reviews and page_count <= max_pages:
#             print(f"Scraping page {page_count}...")
#             # Wait for reviews to load
#             time.sleep(5)  # Give more time for page to load
            
#             tables = driver.page_source
            
#             soup = BeautifulSoup(tables, 'html.parser')
#             ret_bodies = soup.find_all('span', {'data-hook': 'review-body'})
#             ret_titles = soup.find_all('a', {'data-hook': 'review-title'})  
#             ret_ratings = soup.find_all('span', class_='a-icon-alt')
            
#             print(f"Found {len(ret_bodies)} reviews on this page")
            
#             # Process found reviews up to target_reviews
#             for i in range(min(len(ret_bodies), target_reviews - len(reviews))):
#                 review_titles.append(ret_titles[i].text.strip())
#                 reviews.append(ret_bodies[i].text.strip())
#                 ratings.append(ret_ratings[i].text.strip())
            
#             # Stop if we've reached our target
#             if len(reviews) >= target_reviews:
#                 print(f"✅ Reached target of {target_reviews} reviews.")
#                 break
                
#             # Try to go to next page
#             try:
#                 print("Looking for next page button...")
#                 next_button = WebDriverWait(driver, 10).until(
#                     EC.element_to_be_clickable((By.CSS_SELECTOR, "li.a-last a"))
#                 )
#                 next_button.click()
#                 page_count += 1
#                 time.sleep(2)  # Brief pause after clicking
#             except Exception as e:
#                 print(f"No more pages available: {str(e)}")
#                 break
                
#         print(f"Scraping complete. Retrieved {len(reviews)} reviews.")
        
#     except Exception as e:
#         print(f"Error during scraping: {str(e)}")
#     finally:
#         driver.quit()
    
#     # Limit to target_reviews in case we got more
#     return review_titles[:target_reviews], reviews[:target_reviews], ratings[:target_reviews]

# def _setup_driver():
#     """Set up the Selenium WebDriver with appropriate options"""
#     chrome_options = Options()
#     chrome_options.add_argument('--disable-gpu')
#     chrome_options.add_argument('--disable-dev-shm-usage')
#     chrome_options.add_argument('--no-sandbox')
#     chrome_options.add_argument('--log-level=3')  # Minimize logging
#     chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
#     chrome_options.add_experimental_option('useAutomationExtension', False)
#     prefs = {
#         "credentials_enable_service": False,         # Disables the password manager
#         "profile.password_manager_enabled": False    # Disables the password manager UI
#     }
#     chrome_options.add_experimental_option("prefs", prefs)
    
#     return webdriver.Chrome(options=chrome_options)

# def _save_to_csv(titles, reviews, ratings, product_name="Amazon Product"):
#     """Save reviews to CSV in format compatible with preprocessing.ipynb"""
#     # Create a DataFrame
#     df = pd.DataFrame({
#         "id": range(1, len(titles) + 1),
#         "name": product_name,
#         "brand": "Amazon",
#         "categories": "Product",
#         "primaryCategories": "Product",
#         "reviews.doRecommend": [True if r.startswith("5") or r.startswith("4") else False for r in ratings],
#         "reviews.rating": [float(r.split()[0]) if r and r[0].isdigit() else 0 for r in ratings],
#         "reviews.text": reviews,
#         "reviews.title": titles
#     })
    
#     # Save as reviews_cleaned.csv for compatibility with existing code
#     compatibility_filename = "reviews_cleaned.csv"
#     df.to_csv(compatibility_filename, index=False)
#     print(f"✅ Saved {len(df)} reviews to {compatibility_filename} for analysis")
    
#     return compatibility_filename