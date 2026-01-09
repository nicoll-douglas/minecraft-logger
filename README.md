# Minecraft Logger

A key/mouse logger I use to log movement input in [Lunar Client](https://www.lunarclient.com/) to CSV files.

## Run Locally

### Prerequisities

- [xdotool](https://github.com/jordansissel/xdotool) - This project makes use of the `xdotool` command-line tool and so only works running Linux with the X11 display server.
- [Python 3.14.2](https://www.python.org/downloads/release/python-3142/) - I had some issues installing the [pynput](https://pypi.org/project/pynput/) library with previous versions so the version I used to get it working is recommended.
- Disclaimer: There are also some implementation-specific details in this project which are tailored for my own personal use so this project most likely won't work for others, however this project is easily forkable.

### 1. Install

```
# Clone repo
git clone https://github.com/nicoll-douglas/minecraft-logger.git
cd minecraft-logger/

# Set up Python environment
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Run

```
# Have a quick look at the config.py file before running in order
# to see the keys that are monitored by the logger as well as the 
# keys that control the logger's state.

python main.py
```
