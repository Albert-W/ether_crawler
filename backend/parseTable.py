from datetime import datetime, timedelta 

def string_to_delta(string_delta):
    tl = string_delta.split()
    # sec ago
    if len(tl) == 2:
        return timedelta(0,1,0)
    # 17 secs ago
    # 1 min ago
    # 8 mins ago
    # 1 hr 53 mins ago
    # 4 days 10 hrs ago
    d = {
        'sec':"seconds",
        "secs":"seconds",
        "min":"minutes",
        "mins":"minutes",
        "hr":"hours",
        "hrs":'hours',
        'day':'days',
        'days':'days',
        'week':'weeks',
        'weeks':'weeks'
    }
    parsed = [ [tl[i],tl[i+1]] for i in range(0, len(tl)-1, 2)]
    time_dict = dict( (d[unit], float(value)) for value, unit in parsed)
    dt = timedelta(**time_dict)

    return dt

def string_to_secs(str):
    dt = string_to_delta(str)
    return dt.total_seconds() 

def string_to_time(str):
    return datetime.now() - string_to_delta(str)    


def value(gas):
    l = gas.split()
    return l[0]


dty = {
    "Last Seen":float,
    "Gas Price":float,
    "Datetime":datetime
}


if __name__ == "__main__":
    time = "4 days 10 hrs ago"    
    time2 = 'sec ago'
    print(string_to_delta(time2))
    print(string_to_delta(time))
    print(string_to_secs(time))
    print(string_to_time(time))


