from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

# Set up the Selenium driver
def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--log-level=3')  # Minimize logging
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    return webdriver.Chrome(options=chrome_options)

# Function to scrape the table and convert to DataFrame
def scrape_reviews(url):
    driver = setup_driver()
    data = []

    driver.get(url)

        # Wait and click on the "See all reviews" link
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="reviews-medley-footer"]/div[2]/a'))
    ).click()
    
    # time.sleep(3000)
    # Wait for email input field and enter email
    email_input = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "ap_email_login"))
    )
    email_input.send_keys("")#idhar apna email daalna hai
    enter_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, "continue"))
    )
    enter_button.click()
    
    password_input = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "ap_password"))
    )
    password_input.send_keys("")#idhar password
    
    sign_in_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, "signInSubmit"))
    )
    sign_in_button.click()
    
    time.sleep(5000)

    try:
        driver.get(url)

        # Wait and click on the "See all reviews" link
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="reviews-medley-footer"]/div[2]/a'))
        ).click()
        
        exit()

        time.sleep(60)  # Give a little time for the new page to load

        tables = driver.page_source
        reviews_titles = []
        reviews = []

        soup = BeautifulSoup(tables, 'html.parser')
        
        # Get review titles and ratings
        spans = soup.find_all('a', class_='a-size-base a-link-normal review-title a-color-base review-title-content a-text-bold')
        for span in spans:
            try:
                title = span.find_all('span')[2].text.strip()
                rating = span.find('span', class_='a-icon-alt').text.strip()
                reviews_titles.append((rating, title))
            except:
                continue
        
        # Get review text
        review_blocks = soup.find_all("span", {"data-hook": "review-body"})
        reviews = [block.find("span").text.strip() for block in review_blocks]

        driver.quit()
        return reviews_titles, reviews

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()
        print("FAIL")
        return [], []

# Main function
def main():
    url = "https://www.amazon.in/ASIAN-Wonder-13-Sports-Running-Shoes/dp/B01N54ZM9W/ref=sr_1_5"
    reviews_titles, reviews = scrape_reviews(url)

    for i in range(len(reviews_titles)):
        print(reviews_titles[i])
        print(reviews[i])
        print("\n")

if __name__ == "__main__":
    main()
