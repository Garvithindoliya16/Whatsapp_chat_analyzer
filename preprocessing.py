# import re
# import pandas as pd


# def preprocess(data):

    

#     cleaned_data = data.replace('\u202f', ' ').lower()
    
#     if(re.search(r'\b(am|pm)\b', cleaned_data)):
#         pattern= r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{1,2}\s?(?:am|pm|AM|PM)?\s-\s'
#     else:
#         pattern=r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{1,2}\s-\s' 
    

#     messages = re.split(pattern,data)[1:]
#     dates=re.findall(pattern,data)
#     df=pd.DataFrame({'user_message':messages, 'date':dates})
#     if(re.search(r'\b(am|pm)\b', cleaned_data)):
#         df['date'] = pd.to_datetime(df['date'], format='%d/%m/%y, %I:%M %p - ')
#     else:
#         df['date'] = pd.to_datetime(df['date'],format='%d/%m/%Y, %H:%M - ')


#     #seperate user name and messages
#     users=[]
#     messages=[]
#     for message in df['user_message']:
#         entry=re.split('([\w\W]+?):\s',message)
#         if entry[1:]:
#             users.append(entry[1])
#             messages.append(entry[2])
#         else:
#             users.append('group_notification')
#             messages.append(entry[0])

#     df['user']=users
#     df['message']=messages
#     df.drop(columns=['user_message'],inplace=True)

#     #seperating year,day,date,hour,minute
#     df['year'] = df['date'].dt.year
#     df['month'] = df['date'].dt.month_name()
#     df['day'] = df['date'].dt.day
#     df['hour'] = df['date'].dt.hour
#     df['minute'] = df['date'].dt.minute
#     df['month_num'] = pd.to_datetime(df['month'], format='%B').dt.month
#     df['only_date']=df['date'].dt.date
#     df['day_name']=df['date'].dt.day_name()

#     period = []
#     for hour in df[['day_name', 'hour']]['hour']:
#         if hour == 23:
#             period.append(str(hour) + "-" + str('00'))
#         elif hour == 0:
#             period.append(str('00') + "-" + str(hour + 1))
#         else:
#             period.append(str(hour) + "-" + str(hour + 1))

#     df['period'] = period
    
#     df=df[df['message'].groupby(df['user']).transform('count') >= 5]

#     return df

import re
import pandas as pd
from datetime import datetime


def infer_date_format(date_samples):
    """
    Infer whether the format is MM/DD/YY or DD/MM/YY
    based on the first few valid date samples.
    """
    mmdd_count = 0
    ddmm_count = 0

    for date_text in date_samples[:10]:
        try:
            # remove trailing commas, times, etc.
            date_part = date_text.split(",")[0].strip()
            day, month, year = [int(x) for x in date_part.split("/")[:3]]
            # If the first number > 12, then it's definitely day first
            if day > 12:
                ddmm_count += 1
            else:
                mmdd_count += 1
        except Exception:
            continue

    # Default to DD/MM/YY if uncertain
    if ddmm_count > mmdd_count:
        return "%d/%m/%y"
    else:
        return "%m/%d/%y"


def preprocess(data):
    cleaned_data = data.replace('\u202f', ' ').lower()

    # Detect if time uses AM/PM or 24h
    if re.search(r'\b(am|pm)\b', cleaned_data):
        pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{1,2}\s?(?:am|pm|AM|PM)?\s-\s'
    else:
        pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{1,2}\s-\s'

    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    df = pd.DataFrame({'user_message': messages, 'date': dates})

    # ===== Infer date format =====
    inferred_fmt = infer_date_format(dates)
    has_ampm = re.search(r'\b(am|pm)\b', cleaned_data)

    # Build final datetime format
    if has_ampm:
        datetime_fmt = inferred_fmt + ", %I:%M %p - "
    else:
        datetime_fmt = inferred_fmt + ", %H:%M - "

    # Try parsing dates
    try:
        df['date'] = pd.to_datetime(df['date'], format=datetime_fmt, errors='coerce')
    except Exception:
        # fallback if year has 4 digits
        datetime_fmt = datetime_fmt.replace("%y", "%Y")
        df['date'] = pd.to_datetime(df['date'], format=datetime_fmt, errors='coerce')

    # separate username and message
    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    # Extract components
    df = df.dropna(subset=['date'])
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    df['month_num'] = df['date'].dt.month
    df['only_date'] = df['date'].dt.date
    df['day_name'] = df['date'].dt.day_name()

    # Hourly period column
    period = []
    for hour in df['hour']:
        if hour == 23:
            period.append(f"{hour}-00")
        elif hour == 0:
            period.append(f"00-{hour + 1}")
        else:
            period.append(f"{hour}-{hour + 1}")
    df['period'] = period

    # Filter out inactive users
    df = df[df['message'].groupby(df['user']).transform('count') >= 5]

    return df
