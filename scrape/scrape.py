import requests
from bs4 import BeautifulSoup
import re
from enum import Enum

# import scrape.amazon as amazon
import walmart

class WebsiteType(Enum):
    AMAZON = 1
    WALMART = 2

def get_website_type(url: str) -> WebsiteType:
    """
    Determines the website type (Amazon or Walmart) based on the given URL.
    If the URL does not belong to a supported website, an exception is raised.
    The regex pattern in the search function looks for the presence of 'amazon.' or 'walmart.' in the URL.
    If it finds 'amazon.', the function returns the AMAZON enum value.
    If it finds 'walmart.', the function returns the WALMART enum value.
    If neither is found, an exception is raised.

    Args:
        url (str): The product page URL.

    Returns:
        WebsiteType: An enum value representing the website type (Amazon or Walmart).

    Raises:
        Exception: If the URL does not belong to a supported website.
    """
    if re.search(r'amazon\.', url):
        return WebsiteType.AMAZON
    elif re.search(r'walmart\.', url):
        return WebsiteType.WALMART
    else:
        raise Exception('Unsupported website')

def get_data(url: str) -> None:
    """
    Fetches and processes reviews from the specified product page URL.
    Based on the website type determined by the `get_website_type` function,
    this function calls the appropriate extraction functions to fetch and process
    reviews for Amazon or Walmart product pages.

    Args:
        url (str): The product page URL.
    """
    website_type = get_website_type(url)

    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "accept-language": "en-US;en;q=0.9",
        "accept-encoding": "gzip, deflate, br",
    }

    try:
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            product_page_soup = BeautifulSoup(res.text, 'html.parser')
    except:
        pass

    if website_type == WebsiteType.AMAZON:
        # Call Amazon-specific functions to fetch and process reviews
        pass
    elif website_type == WebsiteType.WALMART:
        # Call Walmart-specific functions to fetch and process reviews
        product_title = walmart.get_product_name(product_page_soup)
        product_description = walmart.get_product_description(product_page_soup)
        product_category = walmart.get_product_category(product_page_soup)
        product_reviews = walmart.fetch_and_process_reviews(product_page_soup)

    return product_title, product_description, product_reviews





# def get_page(url: str):
#     # Send a request to the website and get the HTML content
#     response = requests.get(url)
#     html_content = response.text

#     # Parse the HTML content using BeautifulSoup
#     soup = BeautifulSoup(html_content, 'html.parser')

#     # Navigate to review page
#     if "walmart" in url:
#         review_page = soup.find('a', {'class': 'see-all-reviews'})

def test():
    url = "https://www.walmart.com/ip/SAMSUNG-T7-500GB-USB-3-2-Gen-2-10Gbps-Type-C-External-Solid-State-Drive-Portable-SSD-Black-MU-PC500T-AM/142416044"
    get_data(url)

if __name__ == "__main__":
    test()