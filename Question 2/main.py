from lat_long_convert import lat_long_convert
from datetime_convert import convert_into_datetime
from read_csv import read_csv
from dist_bw_location import dist_bw_location
from time_diff import time_diff
from fraud import fraud
from datetime import datetime

# Baseline
start = datetime.now()

# Reading CSV file
transac = read_csv()

# Making time into datetime, Longitude & Latitude
transac = convert_into_datetime(transac)

# Convert Distance into Longitude & Latitude
transac = lat_long_convert(transac)

# Checking Distance Between location
dist_above_20 = dist_bw_location(transac)

# Checking Time Difference
time_30_mins = time_diff(dist_above_20)


# Remove counter/id & Print result
print(fraud(time_30_mins, read_csv()))

# Baseline for Enhancement 2.281092 (lowest)
end = datetime.now()
print(end-start)
