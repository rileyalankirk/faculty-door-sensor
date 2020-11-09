# Door Sensor Project

## Problem:
Students do not know if the Computer Science professors are in their offices unless they walk over and see if the office doors are open.


## Solution:
Authors: **Benjamin Anderson** and **Caelin Finn McCool**

Utilize sensors to detect which office doors are open or closed. A graphical display, which is constantly updating, shows which professors' doors are open or closed. If a door is open, then it is assumed a professor is available.

## Additional Features:
Authors: **Matt Kosack** and **Riley Kirkpatrick**

Refactored original solution. Furthermore, can now access the graphical display of which doors are open through a website on the local Moravian network.
Also can access statistics on what hours each day professors' doors are usually open.


## Requirements:
redis 
* Install with `sudo apt install redis`

## Setup
Enable ntp syncing to keep time in sync:
* To get possible timezones: `timedatectl list-timezones`
* Set timezone example: `sudo timedatectl set-timezone America/New_York`
* Setup config for syncing time: `sudo nano /etc/systemd/timesyncd.conf`
* Make sure FallbackNTP is set to local pool servers. US example:

        [Time]
        FallbackNTP = 0.us.pool.ntp.org 1.us.pool.ntp.org 2.us.pool.ntp.org 3.us.pool.ntp.org
To begin syncing time:
* Run `sudo timedatectl set-ntp true`


## Notes:
Disabling the screensaver for client side monitor:

* Run `sudo apt install xscreensaver`
* Go into the Preferences option on the main desktop menu
* Select the Screen Saver application and then disable screen saver in the drop down menu on the first tab

