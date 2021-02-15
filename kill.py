import os
import psutil
import signal

drivers = [p for p in psutil.process_iter() if p.name() == 'chromedriver']

for driver in drivers:
    print(driver.gids())
    print(driver.pid)

    group_id = os.getpgid(driver.pid)
    print(group_id)
