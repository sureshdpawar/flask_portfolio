
## Overview of the App

This is my personnel portfolio app.

This app is developed using Python's Flask framework.

## Run it locally
From Linux machine root directory ec2-linux
```sh
python3 -m venv venv/  
source ./venv/bin/activate
python main.py --host 0.0.0.0 --port 5000

nohup python main.py --host 0.0.0.0 --port 5000 --debug > flask.log 2>&1 &
```
From Windows machine root directory
```sh
windows local
.\venv\Scripts\activate
python main.py --debug
```