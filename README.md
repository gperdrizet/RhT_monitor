# RhT_monitor
Relative humidity and temperature monitoring.

## Setup notes
### Cron
Measurments are triggered via a cron job. Add the following to the user's cronfile (i.e. **crontab -e**). A measurment every minute seems like a good place to start, but this can be changed to fit the use case.
```
*/1 * * * * python /path/to/RhT_monitor/RhT_monitor.py
```

### CircuitPython (for sensors)
To run the temp/humidity/pressure sensors, we need CircuitPython and the library for the sensors (AdaFruit MS8607 and AdaFruit MCP9808). I am using a RasperryPi Zero W for which detailed instructions can be found here: [CircuitPython](https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/installing-circuitpython-on-raspberry-pi), [MS8607 library](https://learn.adafruit.com/adafruit-te-ms8607-pht-sensor/python-circuitpython) and [MCP9808 library](https://learn.adafruit.com/mcp9808-temperature-sensor-python-library/software). Here is the short version.

Check that you are running python 3* and pip to match, then install CircuitPython:
```
$ sudo pip3 install --upgrade setuptools
$ sudo pip3 install --upgrade adafruit-python-shell
$ wget https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/raspi-blinka.py
$ sudo python3 raspi-blinka.py
```
Note: this will set python 3 as system wide default and requires a reboot to complete. Also, output indicates that pre-installing setuptools may be unnecessary.

Then install the library for the MS8607:
```
sudo pip3 install adafruit-circuitpython-ms8607
```
Next install the library for the MCP9808:
```
$ git clone https://github.com/adafruit/Adafruit_Python_MCP9808.git
$ cd Adafruit_Python_MCP9808
$ sudo python setup.py install
```
Last thing is to change permissions so that non-root users can access I2C devices:
```
$ sudo groupadd i2c
$ sudo chown :i2c /dev/i2c-1
$ sudo chmod g+rw /dev/i2c-1
$ sudo usermod -aG i2c user
```
Then you should be able to access ic2-i without elevating privileges. Test is with:
```
i2cdetect -y 1
```
Output should be something like:
```
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:          -- -- -- -- -- -- -- -- -- -- -- -- -- 
10: -- -- -- -- -- -- -- -- 18 -- -- -- -- -- -- -- 
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
40: 40 -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
70: -- -- -- -- -- -- 76 --
```

### Pandas
Note: had some trouble getting pandas installed on the Raspberry PI 0 W. Installing via pip or pip3 appeared to hang for >1 h. Then fail with error:
```
ERROR: Could not build wheels for pandas, which is required to install pyproject.toml-based projects
```
Could never find a satisfactory explanation. Installing with:
```
$ sudo apt install python-pandas
```
gave 'module not found' errors at run time. Thinking it's maybe a conflict between competing python versions and/or packages installed via pip vs apt. This Pi is a mess... needs a wipe. Finaly got it working with:
```
$ sudo apt install python3-pandas
```
Your mileage may vary.