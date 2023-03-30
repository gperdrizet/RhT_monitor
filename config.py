'''RhT Monitor: simple python utility to monitor temperature and 
relative humidity.

Copyright (C) 2022 George A. Perdrizet II
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.'''

import os

BASE_PATH = os.path.dirname(os.path.realpath(__file__))
DATA_PATH = f'{BASE_PATH}/data'
RAW_DATA_PATH = f'{DATA_PATH}/raw_data'