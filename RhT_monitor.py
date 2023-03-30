'''RhT Monitor: simple python utility to monitor temperature and 
relative humidity.

Copyright (C) 2022 George A. Perdrizet II
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.'''

import os.path
import board
import busio
import pandas as pd
from datetime import datetime
from adafruit_ms8607 import MS8607
import Adafruit_MCP9808.MCP9808 as MCP9808

import config

# Get current time
current_datetime = datetime.now()

# Get date as string for output file name.
current_date = current_datetime.date()
current_date = current_date.strftime('%Y-%m-%d')
print(f'Current datetime: {current_datetime}')
print(f'Current date: {current_date}')

# Generate output file name based on current date
# This way every day we will have a new datafile
output_file = f'{config.RAW_DATA_PATH}/{current_date}.csv'

# Check if data output file exists
if os.path.exists(output_file) == True:
    
    # If it does, load it to append more data
    sensor_data_df = pd.read_csv(output_file)

elif os.path.exists(output_file) == False:
    
    # If it doesn't exist, make empty dataframe to hold results
    column_names = [
        'Datetime',
        'MCP9808 temperature (\N{DEGREE SIGN}C)',
        'MCP9808 temperature (\N{DEGREE SIGN}F)',
        'MS8607 temperature (\N{DEGREE SIGN}C)',
        'MS8607 temperature (\N{DEGREE SIGN}F)',
        'MS8607 pressure (kPa)',
        'MS8607 relative humidity (%)'
    ]

    sensor_data_df = pd.DataFrame(columns=column_names)

print(f'Reading sensors')

# Read data from MS8607 sensor (temp., pressure and humidity)
i2c = busio.I2C(board.SCL, board.SDA)
MS8607_data = MS8607(i2c)
MS8607_tempC = round(MS8607_data.temperature, 1)
MS8607_tempF = round((MS8607_tempC * (9/5)) + 32, 1)
MS8607_pressure = round(MS8607_data.pressure / 10, 1)
MS8607_humidity = round(MS8607_data.relative_humidity, 1)
print(f'MS8607 - Pressure: {MS8607_pressure} kPa, Temperature: {MS8607_tempC} \N{DEGREE SIGN}C, {MS8607_tempF} \N{DEGREE SIGN}F, Relative humidity: {MS8607_humidity}')

# Read data from MCP9808 sensor (temp. only)
sensor = MCP9808.MCP9808()
MCP9808_tempC = round(sensor.readTempC(), 1)
MCP9808_tempF = round((MCP9808_tempC * (9/5)) + 32, 1)
print(f'MCP9808 - Temperature: {MCP9808_tempC} \N{DEGREE SIGN}C, {MCP9808_tempF} \N{DEGREE SIGN}F')

# Assemble data into row to be added to growing dataframe
new_row = [current_datetime, MCP9808_tempC, MCP9808_tempF, MS8607_tempC, MS8607_tempF, MS8607_pressure, MS8607_humidity]

# Add new data to dataframe
sensor_data_df.loc[len(sensor_data_df)] = new_row

# Save progress
sensor_data_df.to_csv(output_file, index=False)