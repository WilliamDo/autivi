import time
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By

driver = Chrome()
driver.get("http://www.vietchannels.com/watch2.php?id=434")

full_screen_button = driver.find_element(By.CSS_SELECTOR, "a.fp-fullscreen.fp-icon")
full_screen_button.click()
