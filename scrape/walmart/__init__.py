import time

import requests
from bs4 import BeautifulSoup

PRODUCT_DESCRIPTION_PREFIX = "About this itemProduct details"
PRODUCT_DESCRIPTION_DISCLAIMER = "error:We aim to show you accurate product information. Manufacturers, suppliers and others provide what you see here, and we have not verified it.\xa0\xa0See our disclaimer"

def get_all_reviews_url(html_content: str) -> str:
    soup = BeautifulSoup(html_content, 'html.parser')
    all_reviews_button = soup.find('a', {'link-identifier': 'seeAllReviews'})
    if all_reviews_button:
        return all_reviews_button['href']
    else:
        raise Exception('All reviews button not found')

def process_review(review) -> dict:
    reviewer_name = review.find('span', {'class': 'reviewer-name-class'}).text.strip()  # Replace with the actual class
    review_date = review.find('span', {'class': 'review-date-class'}).text.strip()  # Replace with the actual class
    review_text = review.find('div', {'class': 'review-text-class'}).text.strip()  # Replace with the actual class

    return {
        'reviewer_name': reviewer_name,
        'review_date': review_date,
        'review_text': review_text,
    }

def fetch_and_process_reviews(soup: BeautifulSoup) -> list:
    time.sleep(10) # Sleep for a few seconds to avoid being blocked by the website
    # Get the URL for the "all reviews" page
    all_reviews_url = get_all_reviews_url(soup)

    # Fetch the HTML content of the "all reviews" page
    all_reviews_html = requests.get(all_reviews_url)

    # Extract both high-rated and low-rated reviews
    # high_rated_reviews = extract_reviews(all_reviews_html, rating_filter='5')  # Assuming 5 is the highest rating
    # low_rated_reviews = extract_reviews(all_reviews_html, rating_filter='1')  # Assuming 1 is the lowest rating

    # Combine high-rated and low-rated reviews
    # all_reviews = high_rated_reviews + low_rated_reviews

    # Process the reviews to extract the relevant information
    # processed_reviews = [process_review(review) for review in all_reviews]

    # return processed_reviews
    return None

def get_product_name(soup: BeautifulSoup) -> str:
    product_name_tag = soup.find('h1', {'itemprop': 'name'})
    return product_name_tag.get_text().strip() if product_name_tag else None

def get_product_description(soup: BeautifulSoup) -> str:
    product_description_tag = soup.find('section', {'data-testid': 'product-description'})
    if not product_description_tag:
        return None

    return product_description_tag.get_text().replace(PRODUCT_DESCRIPTION_PREFIX, "").replace(PRODUCT_DESCRIPTION_DISCLAIMER, "").strip()