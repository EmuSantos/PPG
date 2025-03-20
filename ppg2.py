"""
##################################################################################
##                      Pico y Placa Generator 2 (PPG2)                          ##
##                         Environmental Zone Project                            ##
##                          Here Technologies (2025)                             ##
##                      Created by Emi Santos Tinoco - SDS1                      ##
##                            Last Updated: 5 March 2025                         ##
##################################################################################

## Description:
## PPG2 is a tool designed to streamline the creation of metadata for vehicle 
## restriction zones, also known as "Pico y Placa". This tool allows users to 
## quickly configure and generate restriction records in a structured format, 
## making the process more efficient while maintaining an open-source nature 
## for customization. 

## Features:
## - User-friendly interface with Streamlit.
## - Automated restriction generation based on user input.
## - Dynamic handling of holidays and date ranges.
## - Support for multiple vehicle categories.
## - Export functionality to CSV format.
## - Customizable restrictions, including weight-based limitations for trucks.

## Usage:
## - Enter the environmental zone name and ID.
## - Select vehicle restriction values and additional tags.
## - Define the applicable date range and time periods.
## - Input restriction values based on license plates or maximum total weight.
## - Add specific truck restrictions when required.
## - Generate and review the resulting DataFrame.
## - Export the data to a CSV file for further processing.

## Dependencies:
## - Python 3.x
## - Streamlit
## - Pandas
## - Datetime

## Notes:
## - Ensure all required fields are correctly filled before generating the DataFrame.
## - The tool prevents duplicate records from being added.
## - Open-source and adaptable for specific implementation needs.

## License:
## - This project follows an open-source model. Users can modify the code to 
##   suit their requirements while maintaining proper attribution.

"""


import streamlit as st
from datetime import datetime, timedelta
import pandas as pd

# Streamlit Config
st.title('Pico y Placa Generator')

# Holidays
holidays = st.text_area(
    "Holidays (format DDMMYYYY):",
    value='01012025, 31122025'
)
holidays = holidays.replace(" ", "").split(',')

# Holidays convert to datetime
holiday_dates = [datetime.strptime(date, '%d%m%Y').date() for date in holidays]

# Function AddReg 
def addreg(EZname, EZid, Vcat, VcatID, EZvr_value, EZkeyid_value, EZkeyname, EZtag, EZval, timeft, dayft, monthft, dateft):
    return {
        'ENVZONE_NAME': EZname,
        'ENVZONE_ID': EZid,
        'Restriction_id': '',
        'vehicle_category': Vcat,
        'vehicle_category_id': VcatID,
        'EZ_VR_VALUES': EZvr_value,  # EZ Vehicle Restrictions
        'EZ_KEY_ID': EZkeyid_value,  # EZ_KEY_ID
        'EZ_KEY_NAMES': EZkeyname,   # EZ_KEY_NAMES
        'EZ_ADDT_TAG': EZtag,
        'EZ_VALUES': EZval,
        'timeFrom_timeTo': timeft,
        'dayFrom_dayTo': dayft,
        'monthFrom_monthTo': monthft,
        'dateFrom_dateTo': f'{dateft}-{dateft}'
    }

# Convert month to 'MM' format (two digits)
def monthm(varmonth):
    return varmonth.strftime('%m')  # Formato de mes con dos cifras


# Convert days to 'DD-DD'
def dayy(varname):
    day_map = {
        'Monday': '02',
        'Tuesday': '03',
        'Wednesday': '04',
        'Thursday': '05',
        'Friday': '06',
        'Saturday': '07',
        'Sunday': '01'
    }
    return day_map.get(varname, '')

# Vehicle Categories and value
vehicle_categories = {
    'AUTO': 3,
    'CARPOOL': 16,
    'MOTORCYCLE': 2,
    'THROUGH_TRAFFIC': 15,
    'TAXI': 14,
    'TRUCK': 6,
    'BUS': 13
}

# Ez_VehicleRestriction Values
EZvr_values = {
    'License Plate Number': 'LIC_PLATE',
    'OVERRIDE': 'OVERRIDE',
    'Max_Total_Weight': 'MAX_TOTAL_WGHT'
}

# Ez_Tag Values
Ez_Tag = {
    'LicensePlate': 3,
    'LicensePlateEnding': 5,
    'LicensePlateStarting': 7
}



# Insert text 
EZname = st.text_input('Zone Name:', 'Pico y Placa')
selected_categories = st.multiselect('Vehicle Categories:', list(vehicle_categories.keys()))
EZid = st.text_input('Zone ID:', '')
EZvr_selected = st.selectbox('Vehicle Restriction Value:', list(EZvr_values.keys()))
EZtag_selected = st.selectbox('EzTag:', list(Ez_Tag.keys()))
startdate = st.date_input('Start day:', datetime(2025, 1, 1))
enddate = st.date_input('End Day:', datetime(2025, 12, 31))
times = st.text_input('Time Range:', '00:00-23:59')

# Config Ezval for days
ezval = {'Monday': st.multiselect('Monday Values:', [1, 2, 3, 4, 5, 6, 7, 8, 9, 0, "ODD", "EVEN"]),
    'Tuesday': st.multiselect('Tuesday Values:', [1, 2, 3, 4, 5, 6, 7, 8, 9, 0, "ODD", "EVEN"]),
    'Wednesday': st.multiselect('Wednesday Values:', [1, 2, 3, 4, 5, 6, 7, 8, 9, 0, "ODD", "EVEN"]),
    'Thursday': st.multiselect('Thursday Values:', [1, 2, 3, 4, 5, 6, 7, 8, 9, 0, "ODD", "EVEN"]),
    'Friday': st.multiselect('Friday Values:', [1, 2, 3, 4, 5, 6, 7, 8, 9, 0, "ODD", "EVEN"]),
    'Saturday': st.multiselect('Saturday Values:', [1, 2, 3, 4, 5, 6, 7, 8, 9, 0, "ODD", "EVEN"]),
    'Sunday': st.multiselect('Sunday Values:', [1, 2, 3, 4, 5, 6, 7, 8, 9, 0, "ODD", "EVEN"])
    }

# Start/End date to datetime
f1 = startdate
f2 = enddate
dayT = (f2 - f1).days

if EZvr_values[EZvr_selected] == 'MAX_TOTAL_WGHT':
    day_texts = st.text_input('Enter Weigth Value:', '')
    selected_days = st.multiselect(
    'Select Days for Truck Restriction:',
    ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
)
    if st.button("Add Truck Information"):
        if selected_days and day_texts:
            for single_date in (startdate + timedelta(n) for n in range((enddate - startdate).days + 1)):
                if single_date in holiday_dates:
                    continue
                
                weekday = single_date.strftime('%A')
                if weekday in selected_days:
                    VcatID = vehicle_categories['TRUCK']
                    record = addreg(
                        EZname, EZid, 'TRUCK', VcatID, 'Max_Total_Weight', 'MAX_TOTAL_WGHT', EZtag_selected, Ez_Tag[EZtag_selected], day_texts, times, dayy(weekday), monthm(single_date), single_date.strftime("%Y%m%d")
                    )
                    
                    if record not in st.session_state.setdefault('records_weekdays', []):
                        st.session_state.records_weekdays.append(record)
            st.success("Days added to the DataFrame.")
        else:
            st.error("Please select at least one day and one value.")


# Records Weekdays
if 'records_weekdays' not in st.session_state:
    st.session_state.records_weekdays = []

# Function to generate records for new data
def generate_records():
    EZvr_value = EZvr_values[EZvr_selected]
    EZkeyid_value = Ez_Tag[EZtag_selected]
    EZkeyname = EZvr_selected

    for single_date in (f1 + timedelta(n) for n in range(dayT + 1)):
        if single_date in holiday_dates:
            continue

        weekday = single_date.strftime('%A')
        if weekday not in ezval or not ezval[weekday]:
            continue

        ez_values = list(set(ezval[weekday]))
        day_ft = dayy(weekday)
        month_ft = monthm(single_date)

        for val in ez_values:
            for category in selected_categories:
                VcatID = vehicle_categories[category]
                record = addreg(EZname, EZid, category, VcatID, EZkeyname, EZvr_value, EZtag_selected, EZkeyid_value, val, times, day_ft, month_ft, single_date.strftime("%Y%m%d"))
                if record not in st.session_state.records_weekdays:
                    st.session_state.records_weekdays.append(record)

# Check if all data is completed
def datos_completos(): 
    return EZname and EZid and EZvr_selected and EZtag_selected and times and selected_categories

# Trigger DataFrame generation
if st.button("Generar DataFrame"):
    if datos_completos():
        generate_records()
        st.success("Successfully generated records.")
    else:
        st.error("Please complete all data before generating the DataFrame.")

# Display DataFrame
df_weekdays = pd.DataFrame(st.session_state.records_weekdays)
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


