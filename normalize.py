import csv
import time
import sys
import os
import datetime 
import pytz

#TODO
# Unicdoe replacement characters, if not proper unicode

def convert_timestamp(time):
    pst_tz = pytz.timezone("US/Pacific")
    est_tz = pytz.timezone("US/Eastern")
    # Create datetime object for manipulation
    date_time_obj = datetime.datetime.strptime(time, '%m/%d/%y %H:%M:%S %p')
    # Assume all timestamps are PST
    date_time_obj = pst_tz.localize(date_time_obj)
    # Return data as EST timezone and in ISO-8601 format
    return date_time_obj.astimezone(est_tz).isoformat()

def format_address(address):
    return address

def format_zip(zipcode):
    return '{0:0>5}'.format(zipcode)

def format_full_name(name):
    return name.upper()

def time_in_seconds(time):
    h,m,s = time.split(':')
    s, ms = s.split('.')
    seconds = int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000
    return seconds

def sum_seconds(t1, t2):
    return time_in_seconds(t1) + time_in_seconds(t2)

def read_csv():
    sys.stdin.reconfigure(encoding='utf-8', errors='replace')

    reader = csv.DictReader(sys.stdin)
    header = reader.fieldnames

    writer = csv.DictWriter(sys.stdout, fieldnames=header)

    writer.writeheader()
    for i, row in enumerate(reader):
        try:
            new_row = {
                header[0]: convert_timestamp(row['Timestamp']),
                header[1]: row['Address'], 
                header[2]: format_zip(row['ZIP']), 
                header[3]: format_full_name(row['FullName']),
                header[4]: str(time_in_seconds(row['FooDuration'])),
                header[5]: str(time_in_seconds(row['BarDuration'])),
                header[6]: str(sum_seconds(row['FooDuration'], row['BarDuration'])),
                header[7]: row['Notes']
            }
            
            writer.writerow(new_row)
        except:
            sys.stderr.write('Warning: Row %d cannot be processed. Proceeding with remaining rows.\n' % (i+1))
    

def main():
    read_csv()

main()