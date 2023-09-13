# This is script for downloading CVS files with stock data from finance.yahoo.com
# It works in the following way:
# 1. Search for a needed company on finance.yahoo.com
# 2. Download Historical Stock data

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from web_scraping.driver import ChromeDriver

COMPANY = "Microsoft"
START_DATE = "08/01/2022"
END_DATE = "08/01/2023"
DOWNLOAD_DIR = "/tmp"


def setup_driver(download_dir):
    chrome_options = webdriver.ChromeOptions()
    prefs = {'download.default_directory': download_dir}
    chrome_options.add_experimental_option('prefs', prefs)
    chrome_options.headless = True
    return chrome_options


def download_stock_data(company_name, download_to, start_date=None, end_date=None):
    app = ChromeDriver(options=setup_driver(download_to))
    driver = app.driver
    app.open("https://finance.yahoo.com")

    # Search for company
    search_el = driver.find_element(By.ID, "yfin-usr-qry")
    search_el.send_keys(company_name)
    # TODO: refactor to explicit waits
    # wait until all results are loaded
    driver.implicitly_wait(3)
    driver.find_element(By.XPATH,
                        '//*[@id="header-search-form"]/div[2]/div[1]/div/ul[1]/li[1]/div[1]/div[2]/strong').click()
    driver.implicitly_wait(3)

    # Navigate to Historical Data tab
    driver.find_element(By.XPATH, '//*[@id="quote-nav"]/ul/li[5]/a/span').click()

    # Select dates
    if start_date and end_date:
        driver.find_element(By.XPATH,
                            '//*[@id="Col1-1-HistoricalDataTable-Proxy"]'
                            '/section/div[1]/div[1]/div[1]/div/div/div[1]').click()
        start = driver.find_element(By.NAME, "startDate")
        start.send_keys(start_date)
        end = driver.find_element(By.NAME, "endDate")
        end.send_keys(end_date)
        driver.find_element(By.XPATH, '//*[@id="dropdown-menu"]/div/div[3]/button[1]').click()

    # Download CVS file
    driver.find_element(By.XPATH,
                        '//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[1]/div[2]/span[2]/a/span').click()
    # wait until file is downloaded
    time.sleep(3)


if __name__ == "__main__":
    download_stock_data(COMPANY, download_to="/tmp")
