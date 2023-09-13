from selenium import webdriver


class ChromeDriver:
    def __init__(self, **kwargs):
        self.driver = webdriver.Chrome(**kwargs)

    def __del__(self):
        self.driver.close()

    def open(self, url, width=1600, height=864):
        self.driver.get(url)
        self.driver.set_window_size(width, height)
