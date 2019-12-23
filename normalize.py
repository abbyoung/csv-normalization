import csv
import sys
import datetime 
import pytz

def format_timestamp(time):
    """ Returns formatted timestamp 

        Parameters
        ----------
        time : str
            Expects format %m/%d/%y %H:%M:%S %p
            e.g. 04/01/19 12:00:00 PM
        
        Returns
        -------
        date_time : str
            datetime object converts to str and returns in ISO-8601 format

    """

    # Innput assumed to be in PST
    pst_tz = pytz.timezone("US/Pacific")

    # Output must be converted to EST
    est_tz = pytz.timezone("US/Eastern")

    # Create datetime object for tz manipulation
    date_time_obj = datetime.datetime.strptime(time, '%m/%d/%y %H:%M:%S %p')
    date_time_obj = pst_tz.localize(date_time_obj)

    # Return data as EST timezone and in ISO-8601 format
    return date_time_obj.astimezone(est_tz).isoformat()

def format_zip(zipcode):
    """ Returns formatted zipcode 

        Parameters
        ----------
        zipcode : str
        
        Returns
        -------
        zipcode: str
            Formatted to 5 chars. Adds leading 0s if fewer than 5.

    """
    return '{0:0>5}'.format(zipcode)

def format_full_name(name):
    """ Returns formatted zipcode 

        Parameters
        ----------
        name : str
        
        Returns
        -------
        name: str
            Converts full name to all uppercase letters
            
    """
    return name.upper()

def time_in_seconds(time):
    """ Returns total time in seconds  

        Parameters
        ----------
        time : str
        
        Returns
        -------
        seconds: int
            Includes all hours, minutes, seconds, and millisconds
            
    """
    h,m,s = time.split(':')
    s, ms = s.split('.')
    seconds = int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000
    return seconds

def sum_seconds(t1, t2):
    """ Returns formatted zipcode 

        Parameters
        ----------
        t1 : int
        t2 : int
            Both variables are ints representing a time duration in seconds

        Returns
        -------
        time: int
            Sum of t1 and t2
        
    """
    return time_in_seconds(t1) + time_in_seconds(t2)

def read_csv():
    # In case of broken UTF-8, reconfig input and replace characters
    sys.stdin.reconfigure(encoding='utf-8', errors='replace')
    
    # By using DictReader, we can access our columns by key
    reader = csv.DictReader(sys.stdin)
    header = reader.fieldnames
    
    # DictWriter requires fieldnames
    writer = csv.DictWriter(sys.stdout, fieldnames=header)
    
    # Write fieldnames to stdout
    writer.writeheader()

    for i, row in enumerate(reader):
        try:
            new_row = {
                header[0]: format_timestamp(row['Timestamp']),
                header[1]: row['Address'], 
                header[2]: format_zip(row['ZIP']), 
                header[3]: format_full_name(row['FullName']),
                header[4]: str(time_in_seconds(row['FooDuration'])),
                header[5]: str(time_in_seconds(row['BarDuration'])),
                header[6]: str(sum_seconds(row['FooDuration'], row['BarDuration'])),
                header[7]: row['Notes']
            }

            # Write normalized row to stdoutt
            writer.writerow(new_row)

        except:
            # If there is an error processing any column in the row due to
            # malformed data, drop the entire row.
            sys.stderr.write('Warning: Row %d cannot be processed. Proceeding with remaining rows.\n' % (i+1))
    
def main():
    read_csv()

main()
