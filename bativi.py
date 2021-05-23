from pynput import keyboard
from queue import Queue, Full
from threading import Thread
from time import sleep
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By

driver = Chrome()
presses = Queue(maxsize=1)

vtvgo = {
    '1': "https://vtvgo.vn/xem-truc-tuyen-kenh-vtv1-1.html",
    '2': "https://vtvgo.vn/xem-truc-tuyen-kenh-vtv2-2.html",
    '3': "https://vtvgo.vn/xem-truc-tuyen-kenh-vtv3-3.html",
    '4': "https://vtvgo.vn/xem-truc-tuyen-kenh-vtv4-4.html",
    '5': "https://vtvgo.vn/xem-truc-tuyen-kenh-vtv5-5.html",
    '6': "https://vtvgo.vn/xem-truc-tuyen-kenh-vtv6-6.html",
    '7': "https://vtvgo.vn/xem-truc-tuyen-kenh-vtv7-27.html",
    '8': "https://vtvgo.vn/xem-truc-tuyen-kenh-vtv8-36.html"
}

vtvvn = {

    '1': "https://vtv.vn/truyen-hinh-truc-tuyen/vtv1.htm",
    '2': "https://vtv.vn/truyen-hinh-truc-tuyen/vtv2.htm",
    '3': "https://vtv.vn/truyen-hinh-truc-tuyen/vtv3.htm",
    '4': "https://vtv.vn/truyen-hinh-truc-tuyen/vtv4.htm",
    '5': "https://vtv.vn/truyen-hinh-truc-tuyen/vtv5.htm",
    '6': "https://vtv.vn/vtv6/truyen-hinh-truc-tuyen.htm",
    '7': "https://vtv.vn/truyen-hinh-truc-tuyen/vtv7.htm",
    '8': "https://vtv.vn/vtv8/truyen-hinh-truc-tuyen.htm",
    '9': "https://vtv.vn/truyen-hinh-truc-tuyen/vtv9.htm"
}

def worker():
    while True:
        key = presses.get()
        if key.char in vtvgo:
            print(f"worker {key}")
            play_vtv(vtvgo[key.char])
        else:
            print(key.char)

Thread(target=worker, daemon=True).start()

def play_vtv(url):
    global driver
    
    try:
        driver.quit()
    except:
        print("something went wrong when quitting the driver")

    driver = Chrome()
    driver.get(url)

    try:
        play_button = driver.find_element(By.CSS_SELECTOR, "video.vjs-tech")
        play_button.click()

        sleep(0.5)
        full_screen_button = driver.find_element(By.CSS_SELECTOR, "button.vjs-fullscreen-control")
        full_screen_button.click()

    except:
        print("the button was probably unavailable")


def on_press(key):       
    try:
        presses.put_nowait(key)
        print('alphanumeric key {0} pressed'.format(key.char))

    except AttributeError:
        print('special key {0} pressed'.format(key))
    except Full:
        print('already doing something, try again')

def on_release(key):
    if key == keyboard.Key.esc:
        driver.quit()
        # Stop listener
        return False

# Collect events until released
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
