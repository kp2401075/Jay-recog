from datetime import datetime, time

# get current time
now = datetime.now()
now_time = now.time()

# the starting and ending time range
startHour = 9
startMin = 30
endHour = 20
endMin = 30

# function which returns true if current time is in the range, else return false
def withinRange():  #{
    if time(startHour, startMin) <= now.time() <= time(endHour, endMin):
        return True
    else:
        return False
#}

# check if current time is within the range and do something
if withinRange():
    print "within range"
else:
    print "not within range"
