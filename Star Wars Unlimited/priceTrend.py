from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
options = Options()
options.headless = True  # Run in headless mode
service = Service('C:\\Users\\brike\\Desktop\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe')  # Update with the path to your WebDriver
driver = webdriver.Chrome(service=service, options=options)
url = "https://www.cardmarket.com/en/StarWarsUnlimited/Products/Singles/Spark-of-Rebellion/Iden-Versio-Inferno-Squad-Commander"
try:
    time.sleep(3)
    driver.get(url)

    price_trend = driver.find_element(By.XPATH, "//dt[.='Price Trend']/following-sibling::dd/span")
    print("Price Trend:", price_trend.text)
except Exception as e:
    print("An error occurred:", e)
# Κλείσιμο του driver
driver.quit()
