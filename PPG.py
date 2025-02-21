## Pico y Placa Generator (PPG) - Environmental Zone Project ##
##    19 - Agust - 2024 // Here Technologies (2024)          ##
##        Emi Santos Tinoco - SDS1                           ##


## This tool allows the metadata creation process to be completed  ##
## in one minute with a more user-friendly interface, eliminating  ##
## the need to modify the code. However, it retains the quality of ##
## being open source for any specific requirements you may have.   ##

import streamlit as st
from datetime import datetime, timedelta
import pandas as pd

# Streamlit Config
st.title('Pico y Placa Generator')

# Holidays
holidays = st.text_area(
    "Holydays (format DDMMYYYY):",
    value='25122024'
)
holidays = holidays.replace(" ", "").split(',')

# Holidays convert to datetime
holiday_dates = [datetime.strptime(date, '%d%m%Y').date() for date in holidays]

# Function AddReg 
def addreg(EZname, EZid, Vcat, VcatID, EZvr, EZkeyid, EZtag, EZval, timeft, dayft, monthft, dateft):
    ez_key_names = '5' if EZtag == 'LicensePlateEnding' else '7'
    return {
        'ENVZONE_NAME': EZname,
        'ENVZONE_ID': EZid,
        'Restriction_id': '',
        'vehicle_category': Vcat,
        'vehicle_category_id': VcatID,
        'EZ Vehicle Restrictions': EZvr,
        'EZ_KEY_ID': EZkeyid,
        'EZ_ADDT_TAG': EZtag,
        'EZ_KEY_NAMES': ez_key_names,
        'EZ_VALUES': EZval,
        'timeFrom_timeTo': timeft,
        'dayFrom_dayTo': dayft,
        'monthFrom_monthTo': monthft,
        'dateFrom_dateTo': f'{dateft}-{dateft}'
    }

# Convert mouthn to 'MM-MM'
def monthm(varmonth):
    return f'{varmonth.month:02d}-{varmonth.month:02d}'

# Convert days to 'DD-DD'
def dayy(varname):
    day_map = {
        'Monday': '02-02',
        'Tuesday': '03-03',
        'Wednesday': '04-04',
        'Thursday': '05-05',
        'Friday': '06-06',
        'Saturday': '07-07',
        'Sunday': '01-01'
    }
    return day_map.get(varname, '')

# Vehicle Categories and value
vehicle_categories = {
    'AUTO': 3,
    'CARPOOL': 16,
    'MOTORCYCLE': 2,
    'THROUGH_TRAFFIC': 15,
    'TAXI': 14,
    'TRUCK': 6
}

# Insert text 
EZname = st.text_input('Zone Name:', ' Pico y Placa')
selected_categories = st.multiselect('Vehicle Categories:', list(vehicle_categories.keys()))
EZid= st.text_input('Zone ID:', ' ')
EZvr = st.text_input('Vehicle restriction:',['License Plate Number', 'Max_Total_Weight'])
EZkeyid = st.text_input('Key ID ', 'LIC_PLATE')
EZtag = st.selectbox('Tag:', ['LicensePlateEnding', 'LicensePlateStarting', 'MAX_TOTAL_WGHT'])  
startdate = st.date_input('Start day:', datetime(2025, 1, 1))
enddate = st.date_input('End Day:', datetime(2025, 12, 31))
times = st.text_input('Time Range:', '00:00-23:59')

# Config Ezval for days
ezval = {
    'Monday': st.multiselect('Monday Values:', [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]),
    'Tuesday': st.multiselect('Tuesday Values:', [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]),
    'Wednesday': st.multiselect('Wednesday Values:', [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]),
    'Thursday': st.multiselect('Thursday Values:', [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]),
    'Friday': st.multiselect('Friday Values:', [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]),
    'Saturday': st.multiselect('Saturday Values:', [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]),
    'Sunday': st.multiselect('Sunday Values:', [1, 2, 3, 4, 5, 6, 7, 8, 9, 0])
}

# Start/End date to datetime
f1 = startdate
f2 = enddate
dayT = (f2 - f1).days

# Records Weekdays
records_weekdays = []

# Generate records for the dataframe    
for single_date in (f1 + timedelta(n) for n in range(dayT + 1)):

    if single_date in holiday_dates:
        continue  # Skip holidays

    weekday = single_date.strftime('%A')
    if weekday not in ezval:
        continue  

    ez_values = ezval[weekday]
    day_ft = dayy(weekday)
    month_ft = monthm(single_date)

    for category in selected_categories:
        VcatID = vehicle_categories[category]
        for val in ez_values:
            record = addreg(EZname, EZid, category, VcatID, EZvr, EZkeyid, EZtag, val, times, day_ft, month_ft, single_date.strftime('%Y%m%d'))
            records_weekdays.append(record)

# Create dataframe from lists of records
df_weekdays = pd.DataFrame(records_weekdays)

# Selected columns are in plain text format
df_weekdays['timeFrom_timeTo'] = df_weekdays['timeFrom_timeTo'].astype(str)
df_weekdays['dayFrom_dayTo'] = df_weekdays['dayFrom_dayTo'].astype(str)
df_weekdays['monthFrom_monthTo'] = df_weekdays['monthFrom_monthTo'].astype(str)

# Show Dataframe in the program
st.write('### DataFrame:')
st.dataframe(df_weekdays)

# Export dataframe to CSV
csv = df_weekdays.to_csv(index=False, quoting=1).encode('utf-8')

st.download_button(
    label="Download CSV",
    data=csv,
    file_name='PicoYPlaca_2024.csv',
    mime='text/csv',
)
