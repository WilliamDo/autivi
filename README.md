
```shell
sudo apt update
sudo apt install python3-pyqt6 python3-pyqt6.qtwebengine
```

```shell
sudo systemctl daemon-reload
```

```shell
sudo systemctl enable tv-switcher.service
```

```shell
sudo systemctl start tv-switcher.service
```

```shell
sudo systemctl status tv-switcher.service
```

```shell
sudo journalctl -u tv-switcher.service -f
```


```shell
sudo systemctl daemon-reload
sudo systemctl enable tv-switcher.service
sudo systemctl enable --now tv-switcher-start.timer
sudo systemctl enable --now tv-switcher-stop.timer
```
