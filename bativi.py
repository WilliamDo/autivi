from pynput import keyboard
from queue import Queue, Full
from threading import Thread
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By

driver = Chrome()
presses = Queue(maxsize=1)

def worker():
    while True:
        key = presses.get()
        print(f"worker {key}")
        if key.char == '1':
            play_vtvgo("https://vtvgo.vn/xem-truc-tuyen-kenh-vtv1-1.html")
        elif key.char == '2':
            play_vtvgo("https://vtvgo.vn/xem-truc-tuyen-kenh-vtv2-2.html")
        elif key.char == '3':
            play_vtvgo("https://vtvgo.vn/xem-truc-tuyen-kenh-vtv3-3.html")
        elif key.char == '4':
            play_vtvgo("https://vtvgo.vn/xem-truc-tuyen-kenh-vtv4-4.html")
        else:
            print(key.char)

Thread(target=worker, daemon=True).start()

def play_vtvgo(url):
    driver.get(url)
    
    play_button = driver.find_element(By.CSS_SELECTOR, "button.vjs-play-control")
    play_button.click()

    full_screen_button = driver.find_element(By.CSS_SELECTOR, "button.vjs-fullscreen-control")
    #full_screen_button.click()

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
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()

# ...or, in a non-blocking fashion:
listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()
