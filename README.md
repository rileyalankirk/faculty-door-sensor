# Door Sensor Project

## Problem
Students do not know if the Computer Science professors are in their offices unless they walk over and see if the office doors are open.


## Solution
Authors: **Benjamin Anderson** and **Caelin Finn McCool**

Utilize sensors to detect which office doors are open or closed. A graphical display, which is constantly updating, shows which professors' doors are open or closed. If a door is open, then it is assumed a professor is available.

## Additional Features
Authors: **Matt Kosack** and **Riley Kirkpatrick**

Refactored original solution extensively. Furthermore, can now access the graphical display of which doors are open through a website on the local Moravian network.
Also can access statistics on what hours each day professors' doors are open.


## Requirements
Raspberry Pi (running Raspberry Pi OS)
* If following the setup strictly

Python
* Install with `sudo apt install python3`
* Install pip with `sudo apt install python3-pip`

Redis 
* Install with `sudo apt install redis`

## Setup
* Create a virtual environment
    * Make sure you are in the root of the repository in the faculty-door-sensor directory
    * Run `python3 -m venv .venv` to setup the virtual environment in the directory .venv/
    * Run `. .venv/bin/activate` to activate the virtual environment
* Install the required Python libraries with `pip3 install -r requirements.txt`
* Install the project's source code as an editable package with `pip3 install -e .`

## Additional Setup
* Enable ntp syncing to keep time in sync
    * To get possible timezones: `timedatectl list-timezones`
    * Set timezone example: `sudo timedatectl set-timezone America/New_York`
    * Setup config for syncing time
        * Run `sudo nano /etc/systemd/timesyncd.conf`
        * In this file make sure FallbackNTP is set to local pool servers. US example:

        [Time]
        FallbackNTP = 0.us.pool.ntp.org 1.us.pool.ntp.org 2.us.pool.ntp.org 3.us.pool.ntp.org
        * To finish editing in nano hit CTRL-X and then ENTER

* Begin syncing time
    * Run `sudo timedatectl set-ntp true`

## Client Side Door Sensor GUI, Webserver, Collecting Data
* Make sure you are in the root of the repository in the faculty-door-sensor directory
* Run `. .venv/bin/activate` to activate the virtual environment if not activated already
* Run `cd src/FacultyDoorSensor/client_side`
* Run client side door sensor GUI
    * Run `python3 door_display.py`
* Run webserver
    * Run `python3 webserver.py`
* Run collection of data
    * Run `redis-server`
    * Run `python3 collect_data.py`

## View Website
* On computer running webserver
    * In a web browser, type `localhost:8080` in the address bar
* On another computer on the same network as the webserver
    * Obtain IP of server, can be retrieved by running `ifconfig -a` on the webserver
    * In a web browser, type `<IP of webserver>:8080` in the address bar

## Door Sensor Server
TODO...

## Notes
Disabling the screensaver for client side monitor:

* Run `sudo apt install xscreensaver`
* Go into the Preferences option on the main desktop menu
* Select the Screen Saver application and then disable screen saver in the drop down menu on the first tab

