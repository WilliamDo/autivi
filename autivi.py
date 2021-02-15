import schedule
import time
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By


def start_tivi():
    with Chrome() as driver:
        driver.get("http://www.vietchannels.com/watch2.php?id=434")

        full_screen_button = driver.find_element(By.CSS_SELECTOR, "a.fp-fullscreen.fp-icon")
        full_screen_button.click()
        time.sleep(50400)

schedule.every().day.at("08:00").do(start_tivi)

while True:
    schedule.run_pending()
    print("started")
    time.sleep(600)
