import time
import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def setup_driver():
    options = Options()
    # options.add_argument("--headless")  
    driver = webdriver.Chrome(options=options)
    return driver

# Wait for all products to load
def load_all_products(driver):
    WebDriverWait(driver, 30).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.list--gallery--C2f2tvm.search-item-card-wrapper-gallery"))
    )
    time.sleep(60)  

def get_product_data_from_elements(driver):
    product_elements = driver.find_elements(By.CSS_SELECTOR, 'div.list--gallery--C2f2tvm.search-item-card-wrapper-gallery')
    products = []

    for product in product_elements:
        soup = BeautifulSoup(product.get_attribute('outerHTML'), "html.parser")

        title = soup.select_one("h3.multi--titleText--nXeOvyr")
        title_text = title.text.strip() if title else "N/A"
        
        price_elements = soup.select("div.multi--price-sale--U-S0jtj span")
        price_text = ''.join([span.text.strip() for span in price_elements]) if price_elements else "N/A"
        
        products.append([title_text, price_text])

    return products

def save_to_csv(products):
    with open("aliexpress_products.csv", "w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows([["Product Name", "Price"]] + products)

def main():
    product_name = input("Enter product name: ")
    driver = setup_driver()
    driver.get(f"https://www.aliexpress.com/wholesale?SearchText={product_name.replace(' ', '+')}")
    
    load_all_products(driver)
    all_product_data = get_product_data_from_elements(driver)
    save_to_csv(all_product_data)
    driver.quit()

if __name__ == "__main__":
    main()
