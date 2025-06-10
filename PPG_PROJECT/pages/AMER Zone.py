"""
##################################################################################
##                      Pico y Placa Generator (PPG)                             ##
##                         Environmental Zone Project                            ##
##                          Here Technologies (2025)                             ##
##                      Created by Emi Santos Tinoco - SDS2                      ##
##                            Last Updated: 8 April 2025                         ##
##################################################################################

## Description:
## PPG is a tool designed to streamline the creation of metadata for vehicle 
## restriction zones, also known as "Pico y Placa". This tool allows users to 
## quickly configure and generate restriction records in a structured format,
## making the process more efficient while maintaining an open-source nature 
## for customization. 
## This tool offers the ability to edit the Metadata on a serial or specific 
## day-to-day basis.

## Features:
## - User-friendly interface with Streamlit.
## - Automated restriction generation based on user input.
## - Dynamic handling of holidays and date ranges.
## - Support for multiple vehicle categories.
## - Export functionality to CSV format.
## - Customizable restrictions, including weight-based limitations for trucks, 
##   cases such as absolute and relative age for cars or the Environmental Badge option.

## Usage:
## - Enter the environmental zone name and ID.
## - Select vehicle restriction values and additional tags.
## - Define the applicable date range and time periods.
## - Input restriction values based on license plates or maximum total weight.
## - Add specific (Day by day, Weigth, Absolute or Relative Vehicle Age or Environmental Badge) restrictions when required.
## - Generate and review the resulting DataFrame.
## - Export the data to a CSV file 
## - Generate and review the MMT Files.

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
import os
from io import BytesIO

# Streamlit Config
st.title("PPG AMER 🚗")

# Holidays by country
holidays_by_country = {
    "Colombia": "01012025, 06012025, 24032025, 17042025, 18042025, 01052025, 02062025, 23062025, 30062025, 20072025, 07082025, 18082025, 13102025, 03112025, 17112025, 08122025, 25122025",
    "México": "01012025, 03022025, 03032025, 17032025, 17042025, 18042025, 01052025, 05052025, 16092025, 03112025, 17112025, 25122025",
    "Brazil": "01012025, 01032025, 02032025, 03032025, 04032025, 05032025, 18042025, 21042025, 01052025, 07092025, 12102025, 02112025, 15112025, 24122025, 25122025, 31122025",
    "Costa Rica": "01012025, 19032025, 11042025, 17042025, 18042025, 01052025, 25072025, 02082025, 15082025, 15092025, 12102025, 24122025, 25122025",
    "Bolivia": "01012025, 22012025, 03032025, 04032025, 18042025, 01052025, 19062025, 21062025, 06082025, 02112025, 03112025, 25122025",
    "Ecuador": "01012025, 03032025, 04032025, 18042025, 01052025, 24052025, 10082025, 09102025, 02112025, 03112025, 25122025",
    "Perú": "01012025, 17042025, 18042025, 01052025, 07062025, 29062025, 23072025, 28072025, 29072025, 06082025, 30082025, 08102025, 01112025, 08122025, 09122025, 25122025",
    "Chile": "01012025, 18042025, 19042025, 01052025, 21052025, 07062025, 20062025, 29062025, 16072025, 15082025, 20082025, 18092025, 19092025, 12102025, 31102025, 01112025, 16112025, 08122025, 14122025, 25122025, 31122025"
}

# Select Country 
country = st.selectbox("Select a country's public holidays:", list(holidays_by_country.keys()))
selected_holidays = holidays_by_country[country]

# Add Manually if you need it 
manual_holidays = st.text_area(
    "Or add holidays manually (format DDMMYYYYYYY, separated by commas):",
    value=selected_holidays
)

# Process Holidays
holidays = manual_holidays.replace(" ", "").split(',')

# Holidays convert to datetime
holiday_dates = [datetime.strptime(date, '%d%m%Y').date() for date in holidays]

# Function AddReg 
def addreg(EZname, EZid, Vcat, VcatID, EZvr_value, EZkeyid_value, EZtag, EZkeyname, EZval, timeft, dayft, monthft, dateft):
    return {
        'ENVZONE_NAME': EZname,
        'ENVZONE_ID': EZid,
        'Restriction_id': '',
        'vehicle_category': Vcat,
        'vehicle_category_id': VcatID,
        'EZ_VR_VALUES': EZvr_value,  # EZ Vehicle Restrictions
        'EZ_KEY_ID': EZkeyid_value,  # EZ_KEY_ID
        'EZ_ADDT_TAG': EZkeyname,   
        'EZ_KEY_NAME': EZtag,      
        'EZ_VALUES': EZval,
        'timeFrom_timeTo': timeft,
        'dayFrom_dayTo': dayft,
        'monthFrom_monthTo': monthft,
        'dateFrom_dateTo': f'{dateft}-{dateft}'
    }

# Convert month to 'MM' format (two digits)
def monthm(varmonth):
    return varmonth.strftime('%m')  

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
    'MOTO': 2,
    'THROUGH_TRAFFIC': 15,
    'TAXI': 14,
    'TRUCK': 6,
    'BUS': 13,
    'DELIVERY TRUCK': 5
}

# Ez_VehicleRestriction Values
EZvr_values = {
    'LICENSE PLATE NUMBER': 'LIC_PLATE',
    'OVERRIDE': 'OVERRIDE',
    'MAX TOTAL WEIGHT': 'MAX_TOTAL_WGHT',
    'MIN TOTAL WEIGHT': 'MIN_TOTAL_WGHT',
    'ENVIRONMENTAL BADGE' : 'ENV_BADGE',
    'ABSOLUTE VEHICLE AGE': 'ABS_VEH_AGE',
    'RELATIVE VEHICLE AGE': 'REL_VEH_AGE'
}

# Ez_Tag Values
Ez_Tag = {
    'LicensePlate': 3,
    'LicensePlateEnding': 5,
    'LicensePlateStarting': 7,
    'Max Total Weight': 8,
    'Min Total Weight': 9,
    'Environmental Badge': 10,
    'Absolute Vehicle Age': 11,
    'Relative Vehicle Age': 12,
    'OVERRIDE':13
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
ezval = {'Monday': st.multiselect('Monday Values:', [1, 2, 3, 4, 5, 6, 7, 8, 9, 0, "ODD", "EVEN", "STICKER"," "]),
    'Tuesday': st.multiselect('Tuesday Values:', [1, 2, 3, 4, 5, 6, 7, 8, 9, 0, "ODD", "EVEN", "STICKER"," "]),
    'Wednesday': st.multiselect('Wednesday Values:', [1, 2, 3, 4, 5, 6, 7, 8, 9, 0, "ODD", "EVEN", "STICKER"," "]),
    'Thursday': st.multiselect('Thursday Values:', [1, 2, 3, 4, 5, 6, 7, 8, 9, 0, "ODD", "EVEN", "STICKER"," "]),
    'Friday': st.multiselect('Friday Values:', [1, 2, 3, 4, 5, 6, 7, 8, 9, 0, "ODD", "EVEN", "STICKER"," "]),
    'Saturday': st.multiselect('Saturday Values:', [1, 2, 3, 4, 5, 6, 7, 8, 9, 0, "ODD", "EVEN", "STICKER"," "]),
    'Sunday': st.multiselect('Sunday Values:', [1, 2, 3, 4, 5, 6, 7, 8, 9, 0, "ODD", "EVEN", "STICKER"," "])
    }

# Start/End date to datetime
f1 = startdate
f2 = enddate
dayT = (f2 - f1).days
                     
## MAX TOTAL WEIGHT function
if EZvr_values[EZvr_selected] == 'MAX_TOTAL_WGHT':
    day_texts = st.text_input('Enter Max Weigth Value:', '')
    selected_days = st.multiselect(
    'Select Days for Truck Restriction:',
    ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
)
    if st.button("Add Truck Information"):
        if selected_days and day_texts:
            for single_date in (startdate + timedelta(n) for n in range((enddate - startdate).days + 1)):
                if single_date in holiday_dates:
                    continue
                for category in selected_categories:    
                    weekday = single_date.strftime('%A')
                    VcatID = vehicle_categories.get(category, 'Unknown')
                    if weekday in selected_days:
                        
                        record = addreg(
                            EZname, EZid, category, VcatID, 'Max_Total_Weight', 'MAX_TOTAL_WGHT', Ez_Tag[EZtag_selected], EZtag_selected, day_texts, times, dayy(weekday), monthm(single_date), single_date.strftime("%Y%m%d")
                        )
                    
                    if record not in st.session_state.setdefault('records_weekdays', []):
                        st.session_state.records_weekdays.append(record)
            st.success("Days added to the DataFrame.")
        else:
            st.error("Please select at least one day and one value.")

## MIN TOTAL WEIGHT function
if EZvr_values[EZvr_selected] == 'MIN_TOTAL_WGHT':
    day_texts = st.text_input('Enter Min Weigth Value:', '')
    selected_days = st.multiselect(
    'Select Days for Truck Restriction:',
    ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
)
    if st.button("Add Truck Information"):
        if selected_days and day_texts:
            for single_date in (startdate + timedelta(n) for n in range((enddate - startdate).days + 1)):
                if single_date in holiday_dates:
                    continue
                for category in selected_categories:    
                    weekday = single_date.strftime('%A')
                    VcatID = vehicle_categories.get(category, 'Unknown')
                    if weekday in selected_days:
                        
                        record = addreg(
                            EZname, EZid, category, VcatID, 'Min_Total_Weight', 'MIN_TOTAL_WGHT', Ez_Tag[EZtag_selected], EZtag_selected, day_texts, times, dayy(weekday), monthm(single_date), single_date.strftime("%Y%m%d")
                        )
                    
                    if record not in st.session_state.setdefault('records_weekdays', []):
                        st.session_state.records_weekdays.append(record)
            st.success("Days added to the DataFrame.")
        else:
            st.error("Please select at least one day and one value.")  

## RELATIVE VEHICLE AGE function
if EZvr_values[EZvr_selected] == 'REL_VEH_AGE':
    selected_date = st.date_input('Enter Age Restriction:')  
    EZval = selected_date.strftime('%d/%m/%Y')  # Format "DD/MM/YYYY"

    selected_days = st.multiselect(
        'Select Days for Relative Vehicle Age Restriction:',
        ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    )

    if st.button("Add Relative Vehicle Age Information"):
        if selected_days and EZval:
            for single_date in (startdate + timedelta(n) for n in range((enddate - startdate).days + 1)):
                if single_date in holiday_dates:
                    continue
                
                weekday = single_date.strftime('%A')
                if weekday in selected_days:
                    ez_values = list(set([EZval]))  # Assigns date to EZ_VALUES
                    
                    for val in ez_values:
                        for category in selected_categories:
                            VcatID = vehicle_categories.get(category, 'Unknown')  
                            record = addreg(
                                EZname, EZid, category, VcatID, 
                                'RELATIVE VEHICLE AGE', 'REL_VEH_AGE', 
                                Ez_Tag.get(EZtag_selected, 'Unknown'), EZtag_selected,  
                                val, times,  
                                dayy(weekday), monthm(single_date), 
                                single_date.strftime("%Y%m%d")
                            )
                            
                            if record not in st.session_state.setdefault('records_weekdays', []):
                                st.session_state.records_weekdays.append(record)

            st.success("Days added to the DataFrame.")
        else:
            st.error("Please select at least one day and enter an age restriction.")

## ENVIRONMENTAL BADGE function ONLY ONE RECORD PER VEHICLE
if EZvr_values[EZvr_selected] == 'ENV_BADGE':
    selected_date = st.date_input('Enter Age Environmental Badge:')  
    EZval = selected_date.strftime('%d/%m/%Y')  # Format "DD/MM/YYYY"

    selected_days = ' '

    # Nuevo input para los meses
    selected_months = st.multiselect(
        'Select Months for Restriction:',
        [f"{i:02}" for i in range(1, 13)],  # "01" to "12"
        default=[f"{i:02}" for i in range(1, 13)]  # Default: all months
    )

    if st.button("Add Environmental Badge Information"):
        if selected_days and EZval and selected_months:
            days_selected_count = len(selected_days)
            day_range = ' '

            sorted_months = sorted(int(month) for month in selected_months)
            month_range = f"{sorted_months[0]:02}-{sorted_months[-1]:02}"

            date_from = startdate.strftime('%Y%m%d')
            date_to = enddate.strftime('%Y%m%d')
            date_range = f"{date_from}"
            
            if date_range.count(' ') > 1:
                parts = date_range.split(' ')
                date_range = f"{parts[0]}{parts[1]}"

            for category in selected_categories:
                VcatID = vehicle_categories.get(category, 'Unknown')  
                record = addreg(
                    EZname, EZid, category, VcatID, 
                    'ABSOLUTE VEHICLE AGE', 'ABS_VEH_AGE',
                    Ez_Tag.get(EZtag_selected, 'Unknown'), EZtag_selected, 
                    EZval, ' ', ' ', month_range, ' '
                )

                if record not in st.session_state.setdefault('records_weekdays', []):
                    st.session_state.records_weekdays.append(record)

            st.success("Restriction successfully added for each selected vehicle category.")
        else:
            st.error("Please select at least one day, one month, and enter an age restriction.")

## ABSOLUTE VEHICLE AGE function ONLY ONE RECORD PER VEHICLE
if EZvr_values[EZvr_selected] == 'ABS_VEH_AGE':
    selected_date = st.date_input('Enter Age Restriction:')  
    EZval = selected_date.strftime('%d/%m/%Y')  # Format "DD/MM/YYYY"

    selected_days = st.multiselect(
        'Select Days for Absolute Vehicle Age Restriction:',
        ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    )

    # Nuevo input para los meses
    selected_months = st.multiselect(
        'Select Months for Restriction:',
        [f"{i:02}" for i in range(1, 13)],  # "01" to "12"
        default=[f"{i:02}" for i in range(1, 13)]  # Default: all months
    )

    if st.button("Add Absolute Vehicle Age Information"):
        if selected_days and EZval and selected_months:
            # Determinar número de días seleccionados para dayFrom_dayTo
            days_selected_count = len(selected_days)
            day_range = f"0{days_selected_count}" if days_selected_count < 10 else str(days_selected_count)

            # Determinar rango de meses seleccionados
            sorted_months = sorted(int(month) for month in selected_months)
            month_range = f"{sorted_months[0]:02}-{sorted_months[-1]:02}"

            # Construir dateFrom_dateTo a partir de startdate y enddate
            date_range = f"{startdate.strftime('%Y%m%d')}-{enddate.strftime('%Y%m%d')}"

            for category in selected_categories:
                VcatID = vehicle_categories.get(category, 'Unknown')  
                record = addreg(
                    EZname, EZid, category, VcatID, 
                    'ABSOLUTE VEHICLE AGE', 'ABS_VEH_AGE',
                    Ez_Tag.get(EZtag_selected, 'Unknown'), EZtag_selected, 
                    EZval, times, day_range, month_range, date_range
                )

                if record not in st.session_state.setdefault('records_weekdays', []):
                    st.session_state.records_weekdays.append(record)

            st.success("Restriction successfully added for each selected vehicle category.")
        else:
            st.error("Please select at least one day, one month, and enter an age restriction.")

##---------------------------Restrictions by Day----------------------##
def group_by_consecutive_weeks(dates):
    """Groups dates by consecutive weeks, even if they don't start on Monday."""
    weeks = []
    current_week = []

    for date in dates:
        # Append dates into weeks
        if len(current_week) == 7 or (len(current_week) > 0 and date.weekday() == 0):
            weeks.append(current_week)
            current_week = []

        current_week.append(date)

    # Append the last week
    if current_week:
        weeks.append(current_week)

    return weeks


# Usar un checkbox con un key único y almacenar su estado en session_state
if 'restriction_by_day' not in st.session_state:
    st.session_state.restriction_by_day = False

restriction_by_day = st.checkbox("Restriction Day by Day", key="restriction_by_day_checkbox")
st.session_state.restriction_by_day = restriction_by_day

if st.session_state.restriction_by_day:
    # Group dates by month
    day_count = (enddate - startdate).days + 1
    dates_by_month = {}

    for n in range(day_count):
        current_date = startdate + timedelta(days=n)

        # Skip holidays
        if current_date in holiday_dates:
            continue

        month_name = current_date.strftime('%B %Y')
        
        if month_name not in dates_by_month:
            dates_by_month[month_name] = []

        dates_by_month[month_name].append(current_date)

    # Display weekly input by month
    plates_per_day = {}

    st.write("### Enter plate numbers")

    for month, dates in dates_by_month.items():
        weeks = group_by_consecutive_weeks(dates)

        with st.expander(f"📅 {month}", expanded=False):  # Collapsible month section
            for week_num, week_dates in enumerate(weeks, start=1):
                st.write(f"**Week {week_num}**")

                num_days = len(week_dates)
                cols = st.columns(num_days)  # Columns for each day in the week

                for i, date in enumerate(week_dates):
                    weekday = date.strftime('%A')
                    plate_input = cols[i].text_area(
                        f"{weekday} - {date.strftime('%d')}", 
                        key=f"{month}_{date.strftime('%d')}"
                    )

                    plates = [plate.strip() for plate in plate_input.split(',') if plate.strip()]

                    if plates:
                        plates_per_day[date] = plates  # Records plates per day
else:
    plates_per_day = {}  # If it is not activated, leave plates_per_day empty


##---------------------------Restrictions by Day END----------------------##

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
        
        if st.session_state.restriction_by_day and single_date in plates_per_day:
            ez_values = plates_per_day[single_date]  #  Use day-specific values
        else:
            # If there are no specific values, use those of ezval (multiselect).
            if weekday not in ezval or not ezval[weekday]:
                continue
            ez_values = list(set(ezval[weekday]))

        day_ft = dayy(weekday)
        month_ft = monthm(single_date)

        for val in ez_values:
            for category in selected_categories:
                VcatID = vehicle_categories[category]
                record = addreg(
                    EZname, EZid, category, VcatID, EZkeyname, EZvr_value, 
                    EZkeyid_value, EZtag_selected, val, times, day_ft, month_ft, 
                    single_date.strftime("%Y%m%d")
                )
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

# Sort the DataFrame by the EZ_ADDT_TAG column in ascending order
df_weekdays = pd.DataFrame(st.session_state.records_weekdays)
if 'EZ_ADDT_TAG' in df_weekdays.columns:
    df_weekdays.sort_values(by='EZ_ADDT_TAG', ascending=True, inplace=True)

# ABS_VEH_AGE Date
if not df_weekdays.empty and 'EZ_KEY_NAME' in df_weekdays.columns:
    df_weekdays.loc[df_weekdays['EZ_KEY_NAME'] == 10, 'dateFrom_dateTo'] = df_weekdays.loc[df_weekdays['EZ_KEY_NAME'] == 10, 'dateFrom_dateTo'].str[:-18]


if 'vehicle_category' in df_weekdays.columns:
    df_weekdays.sort_values(by='vehicle_category', ascending=True, inplace=True)

if 'EZ_KEY_NAME' in df_weekdays.columns:
    df_weekdays.sort_values(by='EZ_KEY_NAME', ascending=True, inplace=True)


st.write('### EZ MetaData:')
st.dataframe(df_weekdays)

# Generate dynamic file name
current_year = datetime.now().year  # Corrección: usar datetime directamente
file_name = f"EZ_{EZname}_{EZid}_Metadata_{current_year}.csv"

# Export DataFrame to CSV
csv = df_weekdays.to_csv(index=False, quoting=1).encode('utf-8')

# Download button with the dynamic file name
st.download_button(
    label="Download CSV",
    data=csv,
    file_name=file_name,
    mime='text/csv',
)
############################### M M T   F I L E S   P R O C E S S I N G #################################

def convert_df_to_csv(df):
    """Convert a DataFrame to CSV binary format for download."""
    output = BytesIO()
    df.to_csv(output, index=False, header=False, encoding='utf-8')
    output.seek(0)
    return output.getvalue()

def process_excel_to_csv(input_file):
    if hasattr(input_file, 'name'):
        filename = input_file.name
    else:
        filename = input_file

    # Detect file format and load the DataFrame
    if filename.endswith('.csv'):
        df = pd.read_csv(input_file)
    elif filename.endswith(('.xls', '.xlsx')):
        df = pd.read_excel(input_file)
    else:
        raise ValueError("Formato de archivo no soportado. Use .xlsx, .xls o .csv")
    
    # Ordenar la columna vehicle_category de A a Z si existe
    if 'vehicle_category' in df.columns:
        df = df.sort_values(by=['vehicle_category'])

    # Convertir valores antes del guion en ciertas columnas
    for col in ['dayFrom_dayTo', 'monthFrom_monthTo']:
        if col in df.columns:
            df[col] = df[col].astype(str).str.split('-').str[0]

    # Assign Restriction_id
    restriction_id = 1
    df.at[0, "Restriction_id"] = restriction_id
    
    for i in range(1, len(df)):
        if (
            df.at[i, "vehicle_category"] != df.at[i - 1, "vehicle_category"] or
            df.at[i, "timeFrom_timeTo"] != df.at[i - 1, "timeFrom_timeTo"] or
            df.at[i, "dateFrom_dateTo"] != df.at[i - 1, "dateFrom_dateTo"]
        ):
            restriction_id += 1
        df.at[i, "Restriction_id"] = restriction_id

    # Values for file name
    envzone_id = df['ENVZONE_ID'].iloc[0] if not df['ENVZONE_ID'].empty else 'Unknown'
    today = datetime.today()
    date_str = f"{today.day}_{today.month}_{today.year}"
    output_filename = f"ADD_EZ_ADDT_RESTRS_{envzone_id}_{date_str}.csv"
    
    # Create file ADD_EZ_ADDT_RESTRS
    addt_df = pd.DataFrame({
        'EZ_ADDT_RESTRS': 'EZ_ADDT_RESTRS',
        'OK': 'OK',
        'ENVZONE_ID': df['ENVZONE_ID'],
        'Restriction_id': df['Restriction_id'],
        'ADDITIONAL': 'ADDITIONAL',
        'EZ_KEY_NAME': df['EZ_KEY_NAME'],
        'EZ_VALUES': df['EZ_VALUES'],
        'NULL':' ',
        'NULL2':' ',
        'NULL3':' ',
        'NULL4':' ',
        'NULL5':' ',
        'N': 'N'
    })
    
    # Ensure column ‘N’ is in position M (13)
    addt_df = addt_df[['EZ_ADDT_RESTRS', 'OK', 'ENVZONE_ID', 'Restriction_id', 
                     'ADDITIONAL', 'EZ_KEY_NAME', 'EZ_VALUES', 
                     'NULL', 'NULL2', 'NULL3', 'NULL4', 'NULL5', 'N']]
    
    # Sort by Restriction_id A to Z
    addt_df = addt_df.sort_values(by=['Restriction_id'])
    
    # Remove duplicates based on Restriction_id
    unique_restrictions = df.drop_duplicates(subset='Restriction_id')

    # Generate names for ADD_EZ_REST_ and ADD_EZ_TIME_RESTR_
    rest_filename = f"ADD_EZ_REST_{envzone_id}_{date_str}.csv"
    time_restr_filename = f"ADD_EZ_TIME_RESTR_{envzone_id}_{date_str}.csv"

    # Create file ADD_EZ_REST_
    rest_df = pd.DataFrame({
        'EZ_RESTR': 'EZ_RESTR',
        'OK': 'OK',
        'ENVZONE_ID': unique_restrictions['ENVZONE_ID'],
        'Restriction_id': unique_restrictions['Restriction_id'].astype(float).astype(int),
        'vehicle_category_id': unique_restrictions['vehicle_category_id'],
        'EZ_KEY_ID': unique_restrictions['EZ_KEY_ID'],
        'LICENSE PLATE': unique_restrictions.apply(lambda row: '' if row['EZ_KEY_ID'] == 'OVERRIDE' else (row['EZ_VALUES'] if row['EZ_KEY_ID'] == 'MAX_TOTAL_WGHT' else 'LICENSE PLATE'), axis=1),
        'NULL':' ',
        'NULL2':' ',
        'NULL3':' ',
        'NULL4':' ',
        'NULL5':' ',
        'N': 'N'
    })

    # Ensure column ‘N’ is in position M (13)
    rest_df = rest_df[['EZ_RESTR', 'OK', 'ENVZONE_ID', 'Restriction_id', 
                       'vehicle_category_id', 'EZ_KEY_ID', 'LICENSE PLATE', 
                       'NULL', 'NULL2', 'NULL3', 'NULL4', 'NULL5', 'N']]

    # Sort by Restriction_id from lowest to highest and remove duplicates
    rest_df = rest_df.drop_duplicates(subset='Restriction_id').sort_values(by='Restriction_id')

    # Create file ADD_EZ_TIME_RESTR
    time_restr_df = pd.DataFrame({
        'EZ_TIME_RESTR': 'EZ_TIME_RESTR',
        'OK': 'OK',
        'ENVZONE_ID': unique_restrictions['ENVZONE_ID'],
        'Restriction_id': unique_restrictions['Restriction_id'].astype(float).astype(int),
        'timeFrom_timeTo': unique_restrictions['timeFrom_timeTo'],
        'dayFrom_dayTo': unique_restrictions['dayFrom_dayTo'],
        'monthFrom_monthTo': unique_restrictions['monthFrom_monthTo'],
        'dateFrom_dateTo': unique_restrictions['dateFrom_dateTo'],
        'NULL':' ',
        'NULL2':' ',
        'NULL3':' ',
        'NULL4':' ',
        'N': 'N'
    })

    # Sort by Restriction_id from lowest to highest and remove duplicates
    time_restr_df = time_restr_df.drop_duplicates(subset='Restriction_id').sort_values(by='Restriction_id')
    
    
    # Conditions for MMT files
    rest_df.loc [rest_df['EZ_KEY_ID'] == 'OVERRIDE', 'NULL2'] = 'COST' 
    rest_df.loc[rest_df['EZ_KEY_ID'] == 'REL_VEH_AGE', 'LICENSE PLATE'] = unique_restrictions.loc[unique_restrictions['EZ_KEY_ID'] == 'REL_VEH_AGE', 'EZ_VALUES'].values
    rest_df.loc[rest_df['EZ_KEY_ID'] == 'ABS_VEH_AGE', 'LICENSE PLATE'] = unique_restrictions.loc[unique_restrictions['EZ_KEY_ID'] == 'ABS_VEH_AGE', 'EZ_VALUES'].values
    addt_df = addt_df[~addt_df['EZ_KEY_NAME'].isin([8, 9, 10, 11, 12])]
    time_restr_df = time_restr_df[~time_restr_df['Restriction_id'].isin(unique_restrictions.loc[unique_restrictions['EZ_KEY_ID'] == 'OVERRIDE', 'Restriction_id'])]
    # Preserve 2-digit format in Excel (e.g. '01, '02)
    time_restr_df['dayFrom_dayTo'] = time_restr_df['dayFrom_dayTo'].apply(lambda x: f"{int(x):02d}" if pd.notnull(x) and str(x).isdigit() else x)
    time_restr_df['monthFrom_monthTo'] = time_restr_df['monthFrom_monthTo'].apply(lambda x: f"{int(x):02d}" if pd.notnull(x) and str(x).isdigit() else x)


    return addt_df, output_filename, rest_df, rest_filename, time_restr_df, time_restr_filename


# MMT Files Processor title
st.title("MMT Files Processor")

uploaded_file = st.file_uploader("Upload Metadata (Remember to always sort your file )", type=["csv", "xlsx", "xls"])

#  Buttons for processing files
if uploaded_file and st.button("Process File"):
    addt_df, addt_filename, rest_df, rest_filename, time_restr_df, time_restr_filename = process_excel_to_csv(uploaded_file)

    st.session_state["addt_df"] = addt_df
    st.session_state["rest_df"] = rest_df
    st.session_state["time_restr_df"] = time_restr_df

    st.session_state["addt_csv"] = convert_df_to_csv(addt_df)
    st.session_state["rest_csv"] = convert_df_to_csv(rest_df)
    st.session_state["time_restr_csv"] = convert_df_to_csv(time_restr_df)

    st.session_state["addt_filename"] = addt_filename
    st.session_state["rest_filename"] = rest_filename
    st.session_state["time_restr_filename"] = time_restr_filename

    st.success("✅ File processed successfully")

# Show tables
if "addt_df" in st.session_state:
    st.write("### 📊 ADD_EZ_ADDT_RESTRS DataFrame:")
    st.dataframe(st.session_state["addt_df"])

    st.write("### 📊 ADD_EZ_REST DataFrame:")
    st.dataframe(st.session_state["rest_df"])

    st.write("### 📊 ADD_EZ_TIME_RESTR DataFrame:")
    st.dataframe(st.session_state["time_restr_df"])



# Download buttons
if "addt_csv" in st.session_state:
    st.write("### 📥 Download files:")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.download_button(
            label="📄 Download ADD_EZ_ADDT_RESTRS",
            data=st.session_state["addt_csv"],
            file_name=st.session_state["addt_filename"],
            mime="text/csv"
        )

    with col2:
        st.download_button(
            label="📄 Download      ADD_EZ_REST",
            data=st.session_state["rest_csv"],
            file_name=st.session_state["rest_filename"],
            mime="text/csv"
        )

    with col3:
        st.download_button(
            label="📄 Download ADD_EZ_TIME_RESTR",
            data=st.session_state["time_restr_csv"],
            file_name=st.session_state["time_restr_filename"],
            mime="text/csv"
        )
