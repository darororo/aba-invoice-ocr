from datetime import datetime

def string_to_date(date_str):
    d = datetime.strptime(date_str, "%b %d, %Y")
    d = d.strftime("%m/%d/%Y")
    return d 


