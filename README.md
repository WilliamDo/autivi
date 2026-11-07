
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
