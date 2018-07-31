# Night Owls Detector

The script provides data of those, who sent the task for review in period between
00:00:00 and 04:00:00

# Quickstart

The program is represented by the module seek_dev_nighters.py. Module seek_dev_nighters.py contains the following functions:

- ```get_midnighter_dt()```
- ```get_pages_count()```
- ```get_user_local_dt()```
- ```is_midnighter()```
- ```load_attempts()```
- ```print_midnighter_activity()```
- ```print_title()```


The program uses these libs from Python standart and third-party libraries:

```datetime```
```request```
```pytz```

**How in works:**

- The program connects to the [devman api](https://devman.org/api/challenges/solution_attempts/)  
- Reads content page by page
- Parses every content record 
- Checks if parsed content(datetime) in 00:00:00 and 04:00:00
- If true, prints to the console output 

# How to Install

Python 3 should be already installed. Then use pip (or pip3 if there is a conflict with old Python 2 setup) to install dependencies:

```bash
pip install -r requirements.txt # alternatively try pip3
```

Remember, it is recommended to use [virtualenv/venv](https://devman.org/encyclopedia/pip/pip_virtualenv/) for better isolation.


# How to run
- Activate virtualenv
``` bash
source <path_to_virtualenv>/bin/activate
```
- Run script with virtualenv-interpreter
```bash
<path_to_virtualenv>/bin/python3.5 seek_dev_nighters.py
```
If everything is fine, you'll see such output:
```text
Midnighters on devman detected:

User ten.iliya.dm sent the task for review at 2018-07-30 02:42:03.635308+03:00
User ten.iliya.dm sent the task for review at 2018-07-30 02:25:59.163326+03:00
User olga.goi sent the task for review at 2018-07-29 00:08:55.316651+03:00
User olga.goi sent the task for review at 2018-07-29 00:03:23.414893+03:00
User rtfmagain sent the task for review at 2018-07-27 02:16:44.371999+03:00
User rtfmagain sent the task for review at 2018-07-27 01:38:23.828371+03:00
```

In case of [devman api](https://devman.org/api/challenges/solution_attempts/) unavailable, you'll see this message:
```text
Site https://devman.org/api/challenges/solution_attempts/ is unavailable!
```

# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)

