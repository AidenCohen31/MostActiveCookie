from collections import defaultdict
import sys
from os.path import exists
import datetime

def parse_csv(path):
    """
    Parse the csv and store it in memory
    """
    data = defaultdict(lambda : defaultdict(int))
    #store values in hashtable of hashtables where first key is dates and second is cookie
    with open(path, "r") as files:
        line = files.readline()
        for line in files:
            split_arr = line.split(",")
            data[split_arr[1].split("T")[0]][split_arr[0]] += 1 #split time on T to extract date
    return data

if __name__== "__main__":
    # validate inputs
    try:
        path = sys.argv[1]
        date = sys.argv[sys.argv.index('-d') + 1]
        arr = date.split("-")
        assert exists(path),"path does not exist"
        assert (len(arr) == 3 and sum([i.isnumeric() for i in arr]) == 3 and
            datetime.datetime(int(arr[0]),int(arr[1]),int(arr[2]))), "invalid date"
    except ValueError as e:
        sys.exit(e)
    except AssertionError as e:
        sys.exit(e)
    except Exception as e:
        sys.exit("Did not input correct parameters")
    
    dates = parse_csv(path)
    try:
        highest = max(dates[date].values())
    except ValueError:
        sys.exit("No data for date")
    for i in dates[date].keys():
        if(dates[date][i] == highest):
            print(i)
