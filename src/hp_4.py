# hp_4.py
#
from datetime import datetime, timedelta
from csv import DictReader, DictWriter
from collections import defaultdict


def reformat_dates(old_dates):
    """Accepts a list of date strings in format yyyy-mm-dd, re-formats each
    element to a format dd mmm yyyy--01 Jan 2001."""
    dts=[]
    for d in old_dates:
        
        res = datetime.datetime.strptime(d, "%Y-%m-%d").strftime('%d %b %Y')
        dts.append(res)
        
    return dts


def date_range(start, n):
    """For input date string `start`, with format 'yyyy-mm-dd', returns
    a list of of `n` datetime objects starting at `start` where each
    element in the list is one day after the previous."""
    if not isinstance(start, str) or not isinstance(n, int):
        
        raise TypeError()
    
    dates = []
    
    st = datetime.strptime(start, '%Y-%m-%d')
    
    for i in range(n):
        
        dates.append(st + timedelta(days=i))
        
    return dates


def add_date_range(values, start_date):
    """Adds a daily date range to the list `values` beginning with
    `start_date`.  The date, value pairs are returned as tuples
    in the returned list."""
    num_days = len(values)
    
    date_range_list = date_range(start_date, num_days)

   
    ret = list(zip(date_range_list, values))
    return ret


def fees_report(infile, outfile):
    """Calculates late fees per patron id and writes a summary report to
    outfile."""
    hdrs = ("book_uid,isbn_13,patron_id,date_checkout,date_due,date_returned".
              split(','))
    
    fines = defaultdict(float)
    
    with open(infile, 'r') as f:
        data = DictReader(f, fieldnames=hdrs)
        rows = [row for row in data]

    rows.pop(0)
       
    for line_1 in rows:
       
        patronID = line_1['patron_id']
        
        date_due = datetime.strptime(line_1['date_due'], "%m/%d/%Y")
        
        date_returned = datetime.strptime(line_1['date_returned'], "%m/%d/%Y")
        
        late_days = (date_returned - date_due).days
        
        fines[patronID]+= 0.25 * late_days if late_days > 0 else 0.0
        
                 
    finalIst = [
        {'patron_id': p, 'late_fees': f'{f:0.2f}'} for p, f in fines.items()
    ]
    with open(outfile, 'w') as f:
        
        writer = DictWriter(f,['patron_id', 'late_fees'])
        writer.writeheader()
        writer.writerows(finalIst)


# The following main selection block will only run when you choose
# "Run -> Module" in IDLE.  Use this section to run test code.  The
# template code below tests the fees_report function.
#
# Use the get_data_file_path function to get the full path of any file
# under the data directory.

if __name__ == '__main__':
    
    try:
        from src.util import get_data_file_path
    except ImportError:
        from util import get_data_file_path

    # BOOK_RETURNS_PATH = get_data_file_path('book_returns.csv')
    BOOK_RETURNS_PATH = get_data_file_path('book_returns_short.csv')

    OUTFILE = 'book_fees.csv'

    fees_report(BOOK_RETURNS_PATH, OUTFILE)

    # Print the data written to the outfile
    with open(OUTFILE) as f:
        print(f.read())
