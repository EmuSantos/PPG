import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
import os
from io import BytesIO

# Streamlit Config
st.title('PPG APAC 🚙')

# Holidays by country
holidays_by_country = {
    "Philippines": "01012025, 29012025, 01042025, 09042025, 17042025, 18042025, 19042025, 01052025, 12052025, 06062025, 12062025, 21082025, 25082025, 31102025, 01112025, 30112025, 08122025, 24122025, 25122025, 30122025, 31122025", 
    "NO HOLIDAYS":"01012024"
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


##Define dates
default_start = datetime(2025, 1, 1)
default_end = datetime(2025, 12, 31)
startdate = default_start
enddate = default_end

# ________________________________DICCIONARIES_________________________
vehicle_categories = {
    'AUTO': 3,
    'CARPOOL': 16,
    'MOTORCYCLE': 2,
    'THROUGH_TRAFFIC': 15,
    'TAXI': 14,
    'TRUCK': 6,
    'BUS': 13,
    'DELIVERY TRUCK': 5,
    'ALL VEHICLES': 1
}

Map_Veh_Categories = {
    'AUTOMOBILE': 1,
    'CARPOOL': 8,
    'MOTORCYCLE': 1024,
    'THROUGH_TRAFFIC': 128,
    'TAXI': 4,
    'TRUCK': 64,
    'BUS': 2,
    'DELIVERY': 256,
    'ALL_VEHICLE': 2015
}

EZvr_values = {
    'LICENSE PLATE NUMBER': 'LIC_PLATE',
    'OVERRIDE': 'OVERRIDE',
    'MAX TOTAL WEIGHT': 'MAX_TOTAL_WGHT',
    'MIN TOTAL WEIGHT': 'MIN_TOTAL_WGHT',
    'ENVIRONMENTAL BADGE': 'ENV_BADGE',
    'ABSOLUTE VEHICLE AGE': 'ABS_VEH_AGE',
    'RELATIVE VEHICLE AGE': 'REL_VEH_AGE',

}

Ez_Tag = {
    'LicensePlate': 3,
    'LicensePlateEnding': 5,
    'LicensePlateStarting': 7,
    'Date': 1,
    'Max Total Weight': 8,
    'Min Total Weight': 9,
    'Environmental Badge': 10,
    'Absolute Vehicle Age': 11,
    'Relative Vehicle Age': 12,
    'OVERRIDE': 13
}

EzRestriction = {
    'LICENSE PLATE':'LICENSE PLATE',
    'ODD-EVEN':'ODD-EVEN',
    'UVVRP':'UVVRP'
    
}

EZ_to_Map_Categories = {
    'AUTO': 'AUTOMOBILE',
    'CARPOOL': 'CARPOOL',
    'MOTORCYCLE': 'MOTORCYCLE',
    'THROUGH_TRAFFIC': 'THROUGH_TRAFFIC',
    'TAXI': 'TAXI',
    'TRUCK': 'TRUCK',
    'BUS': 'BUS',
    'DELIVERY TRUCK': 'DELIVERY',
    'ALL VEHICLES': 'ALL_VEHICLE'
}

Lan_Code = {
    'ENGLISH':'ENG',
    'KANNADA':'KAN',
    'UK ENGLISH':'UKE',
    'HINDI':'HIN',
    'INDONESIA':'IND',
    'ASSAMESE':'ASM',
    'BENGALI':'BEN',
    'GUJARATI':'GUJ',
    'KANNADA':'KAN',
    'MALAYALAM':'MAL',
    'MARATHI':'MAR',
    'ORIYA':'ORI',
    'PANJABI':'PAN',
    'TAMIL':'TAM',
    'TELUGU':'TEL'
}

Poly_Restr = {
    'TRUCKS ONLY': 1,
    'AUTOS ONLY': 2,
    'AUTOS AND TRUCKS': 3,
    'BUSES ONLY': 4
}

# Corrected dictionary syntax for Badge_Value
Badge_Value = {
    'DEU_GREEN_STICKER': 'DEU_GREEN_STICKER',
    'DEU_RED_STICKER': 'DEU_RED_STICKER',
    'DEU_YELLOW_STICKER': 'DEU_YELLOW_STICKER',
    'AUT_EURO_I_STICKER': 'AUT_EURO_I_STICKER',
    'AUT_EURO_II_STICKER': 'AUT_EURO_II_STICKER',
    'AUT_EURO_III_STICKER': 'AUT_EURO_III_STICKER',
    'AUT_EURO_IV_STICKER': 'AUT_EURO_IV_STICKER',
    'AUT_EURO_V_STICKER': 'AUT_EURO_V_STICKER',
    'AUT_EURO_VI_STICKER': 'AUT_EURO_VI_STICKER',
    'MEX_HOLOGRAMA_0': 'MEX_HOLOGRAMA_0',
    'MEX_HOLOGRAMA_00': 'MEX_HOLOGRAMA_00',
    'MEX_HOLOGRAMA_1': 'MEX_HOLOGRAMA_1',
    'MEX_HOLOGRAMA_2': 'MEX_HOLOGRAMA_2',
    'MEX_HOLOGRAMA_EXEMPT': 'MEX_HOLOGRAMA_EXEMPT',
    'MEX_HOLOGRAMA_FOREIGN': 'MEX_HOLOGRAMA_FOREIGN',
    'FRA_CRITAIR': 'FRA_CRITAIR',
    'FRA_CRITAIR_1': 'FRA_CRITAIR_1',
    'FRA_CRITAIR_2': 'FRA_CRITAIR_2',
    'FRA_CRITAIR_3': 'FRA_CRITAIR_3',
    'FRA_CRITAIR_4': 'FRA_CRITAIR_4',
    'FRA_CRITAIR_5': 'FRA_CRITAIR_5',
    'SPA_CAT_ZERO_STICKER': 'SPA_CAT_ZERO_STICKER',
    'SPA_CAT_ECO_STICKER': 'SPA_CAT_ECO_STICKER',
    'SPA_CAT_B_STICKER': 'SPA_CAT_B_STICKER',
    'SPA_CAT_C_STICKER': 'SPA_CAT_C_STICKER'
}

Country_Code = {
    'AUSTRIA': 9,
    'BELGIUM': 5,
    'BOLIVIA': 506,
    'BRAZIL': 507,
    'BULGARIA': 19,
    'CHILE': 509,
    'COLOMBIA': 510,
    'COSTA RICA': 511,
    'DENMARK': 16,
    'ECUADOR': 515,
    'ENGLAND': 28,
    'FRANCE': 2,
    'GERMANY': 3,
    'GREECE': 27,
    'INDIA': 217,
    'INDONESIA': 218,
    'ITALY': 1,
    'MEXICO': 527,
    'NETHERLANDS': 6,
    'PERU': 532,
    'PHILIPPINES': 237,
    'POLAND': 43,
    'PORTUGAL': 32,
    'RUSSIA': 45,
    'SCOTLAND': 29,
    'SPAIN': 22,
    'SWEDEN': 23
}

EZ_CatFeature = {
    'POLYGONAL FEATURE':'P',
    'LINEAR FEATURE':'L',
    'FEATURE POINT':'F'
}

###########################################################################################################
#                                                                                                         #
#                                          INPUTS & DATA DISPLAY                                          #
#                                                                                                         #
###########################################################################################################

EZname = st.text_input('Zone Name:', placeholder='Write the name of the Environmental Zone')
EZid = st.text_input('Zone ID:', placeholder='Write the id of the Environmental Zone')
selected_categories = st.multiselect('Vehicle Categories:', list(vehicle_categories.keys()))
EZvr_selected = st.selectbox('Vehicle Restriction Value:', list(EZvr_values.keys()))
EZtag_selected = st.selectbox('EzTag:', list(Ez_Tag.keys()))
EzRest = st.selectbox('EzRestriction:', list(EzRestriction.keys()))

if EZvr_values[EZvr_selected] not in ['MAX_TOTAL_WGHT', 'MIN_TOTAL_WGHT']:
    startdate = st.date_input('Start day:', value=default_start)
    enddate = st.date_input('End Day:', value=default_end)
times = st.text_input('Time Range:', '00:00-23:59')
EzDesc = st.text_input('Ez Description:', placeholder='Write a description of the EZ Restriction')
EzLang = st.selectbox('Lang Description:', ['Select a language...'] + list(Lan_Code.keys()))
EzWeb = st.text_input('Web-Site for EZ:', placeholder='Copy URL')

if EZvr_values[EZvr_selected] not in ['MAX_TOTAL_WGHT', 'MIN_TOTAL_WGHT']:
    ezval = {'Monday': st.multiselect('Monday Values:', [1, 2, 3, 4, 5, 6, 7, 8, 9, 0, "ODD", "EVEN", "STICKER"," "]),
        'Tuesday': st.multiselect('Tuesday Values:', [1, 2, 3, 4, 5, 6, 7, 8, 9, 0, "ODD", "EVEN", "STICKER"," "]),
        'Wednesday': st.multiselect('Wednesday Values:', [1, 2, 3, 4, 5, 6, 7, 8, 9, 0, "ODD", "EVEN", "STICKER"," "]),
        'Thursday': st.multiselect('Thursday Values:', [1, 2, 3, 4, 5, 6, 7, 8, 9, 0, "ODD", "EVEN", "STICKER"," "]),
        'Friday': st.multiselect('Friday Values:', [1, 2, 3, 4, 5, 6, 7, 8, 9, 0, "ODD", "EVEN", "STICKER"," "]),
        'Saturday': st.multiselect('Saturday Values:', [1, 2, 3, 4, 5, 6, 7, 8, 9, 0, "ODD", "EVEN", "STICKER"," "]),
        'Sunday': st.multiselect('Sunday Values:', [1, 2, 3, 4, 5, 6, 7, 8, 9, 0, "ODD", "EVEN", "STICKER"," "])
        }
add_new_city = st.checkbox("New City🌐")

# Start/End date to datetime
f1 = startdate
f2 = enddate
    
dayT = (f2 - f1).days
                     
## MAX TOTAL WEIGHT function
if EZvr_values[EZvr_selected] == 'MAX_TOTAL_WGHT':
    day_texts = st.text_input('Enter Max Weight Value:', '')
    selected_days = st.multiselect(
        'Select Days for Truck Restriction:',
        ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    )

    if st.button("Add Truck Information"):
        if selected_days and day_texts:
            # Codificar días seleccionados
            day_codes = [dayy(day) for day in selected_days]
            day_group = ",".join(sorted(day_codes))  # Ejemplo: 01,02,03

            # Obtener meses del rango, ignorando feriados
            valid_dates = [
                single_date for single_date in (
                    startdate + timedelta(n) for n in range((enddate - startdate).days + 1)
                ) if single_date not in holiday_dates
            ]

            if valid_dates:
                first_month = f"{min(valid_dates).month:02d}"
                last_month = f"{max(valid_dates).month:02d}"
                month_group = f"{first_month}-{last_month}"
            else:
                month_group = "null"

            for category in selected_categories:
                VcatID = vehicle_categories.get(category, 'Unknown')

                record = addreg(
                    EZname,
                    EZid,
                    category,
                    VcatID,
                    'Max_Total_Weight',
                    'MAX_TOTAL_WGHT',
                    Ez_Tag[EZtag_selected],
                    EZtag_selected,
                    day_texts,
                    times,
                    day_group,
                    month_group,
                    'null'  # No se usa fecha específica
                )

                if record not in st.session_state.setdefault('records_weekdays', []):
                    st.session_state.records_weekdays.append(record)

            st.success("Grouped restriction added to the DataFrame.")
        else:
            st.error("Please select at least one day and one value.")

## MIN TOTAL WEIGHT function
if EZvr_values[EZvr_selected] == 'MIN_TOTAL_WGHT':
    day_texts = st.text_input('Enter Min Weight Value:', '')
    selected_days = st.multiselect(
        'Select Days for Truck Restriction:',
        ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    )

    if st.button("Add Truck Information"):
        if selected_days and day_texts:
            # Codificar días seleccionados
            day_codes = [dayy(day) for day in selected_days]
            day_group = ",".join(sorted(day_codes))  # Ejemplo: 01,02,03

            # Obtener meses del rango, ignorando feriados
            valid_dates = [
                single_date for single_date in (
                    startdate + timedelta(n) for n in range((enddate - startdate).days + 1)
                ) if single_date not in holiday_dates
            ]

            if valid_dates:
                first_month = f"{min(valid_dates).month:02d}"
                last_month = f"{max(valid_dates).month:02d}"
                month_group = f"{first_month}-{last_month}"
            else:
                month_group = "null"

            for category in selected_categories:
                VcatID = vehicle_categories.get(category, 'Unknown')

                record = addreg(
                    EZname,
                    EZid,
                    category,
                    VcatID,
                    'Min_Total_Weight',
                    'MIN_TOTAL_WGHT',
                    Ez_Tag[EZtag_selected],
                    EZtag_selected,
                    day_texts,
                    times,
                    day_group,
                    month_group,
                    'null'  # No se usa fecha específica
                )

                if record not in st.session_state.setdefault('records_weekdays', []):
                    st.session_state.records_weekdays.append(record)

            st.success("Grouped restriction added to the DataFrame.")
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

# Inicializar estado
if 'restriction_by_day' not in st.session_state:
    st.session_state.restriction_by_day = False

# Checkbox principal
restriction_by_day = st.checkbox("Restriction Day by Day", key="restriction_by_day_checkbox")
st.session_state.restriction_by_day = restriction_by_day

# Checkbox interno para solo días hábiles
only_weekdays = False
if st.session_state.restriction_by_day:
    only_weekdays = st.checkbox("Only Weekdays (Mon-Fri)", key="only_weekdays_checkbox")

# Lógica de entrada por días
if st.session_state.restriction_by_day:
    day_count = (enddate - startdate).days + 1
    dates_by_month = {}

    for n in range(day_count):
        current_date = startdate + timedelta(days=n)

        # Saltar feriados
        if current_date in holiday_dates:
            continue

        # Omitir fines de semana si está activado
        if only_weekdays and current_date.weekday() >= 5:
            continue

        month_name = current_date.strftime('%B %Y')
        dates_by_month.setdefault(month_name, []).append(current_date)

    # Mostrar input semanal por mes
    plates_per_day = {}

    st.write("### Enter plate numbers")

    for month, dates in dates_by_month.items():
        weeks = group_by_consecutive_weeks(dates)

        with st.expander(f"📅 {month}", expanded=False):
            for week_num, week_dates in enumerate(weeks, start=1):
                st.write(f"**Week {week_num}**")

                num_days = len(week_dates)
                cols = st.columns(num_days)

                for i, date in enumerate(week_dates):
                    weekday = date.strftime('%A')
                    plate_input = cols[i].text_area(
                        f"{weekday} - {date.strftime('%d')}",
                        key=f"{month}_{date.strftime('%d')}"
                    )

                    plates = [plate.strip() for plate in plate_input.split(',') if plate.strip()]
                    if plates:
                        plates_per_day[date] = plates
else:
    plates_per_day = {}


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


if 'EZ_KEY_NAME' in df_weekdays.columns:
    df_weekdays.sort_values(by='EZ_KEY_NAME', ascending=True, kind='stable', inplace=True)

if 'dateFrom_dateTo' in df_weekdays.columns:
    df_weekdays.sort_values(by='dateFrom_dateTo', ascending=True, kind='stable', inplace=True)

if 'vehicle_category' in df_weekdays.columns:
    df_weekdays.sort_values(by='vehicle_category', ascending=True, kind='stable', inplace=True )
     

st.write('### EZ MetaData:')
st.dataframe(df_weekdays)

# Generate dynamic file name
#current_year = datetime.now().year  # Corrección: usar datetime directamente
#file_name = f"EZ_{EZname}_{EZid}_Metadata_{current_year}.csv"

# Export DataFrame to CSV
#csv = df_weekdays.to_csv(index=False, quoting=1).encode('utf-8')

# Download button with the dynamic file name
#st.download_button(
#    label="Download CSV",
#    data=csv,
#    file_name=file_name,
#    mime='text/csv',
#)      

########################################################################################################
#                                                                                                      #
#                                            METADATA APAC                                             #
#                                                                                                      #
########################################################################################################

import pandas as pd
import streamlit as st
from io import BytesIO

# Asegura que las variables necesarias estén definidas
if 'EZ_ADDT' not in st.session_state:
    st.session_state.EZ_ADDT = []

if 'EZ_TIME_RESTR' not in st.session_state:
    st.session_state.EZ_TIME_RESTR = []

if 'EZ_RESTR' not in st.session_state:
    st.session_state.EZ_RESTR = []

if 'EZ_VEH_RESTR' not in st.session_state:
    st.session_state.EZ_VEH_RESTR = []

if 'EZ_DESCRIPTION' not in st.session_state:
    st.session_state.EZ_DESCRIPTION = []

if 'EZ_WEBSITE' not in st.session_state:
    st.session_state.EZ_WEBSITE = [] 

if 'EZ_POLYRESTR' not in st.session_state:
    st.session_state.EZ_POLYRESTR = []   

if 'EZ_DATES' not in st.session_state:
    st.session_state.EZ_DATES = []

if 'ENVZONE_UMR' not in st.session_state:
    st.session_state.ENVZONE_UMR = []   

if 'ENVZONE_CHAR' not in st.session_state:
    st.session_state.ENVZONE_CHAR = []    

##Deleted EZ_ADDT if selected MIN o MAX WEIGHT
generate_addt = not (EZvr_selected in ['MAX TOTAL WEIGHT', 'MIN TOTAL WEIGHT'])



# Botón para crear la metadata y generar el archivo
if st.button(" Create APAC Metadata🔵"):

    df = df_weekdays.copy()
    lang = EzLang
    lang_code = Lan_Code[lang]

    # Ordenar para asegurar consistencia en los valores comparados
    df = df.sort_values(by=["vehicle_category", "timeFrom_timeTo", "dateFrom_dateTo"]).reset_index(drop=True)

    # Generar RESTRICTION_ID basados en cambios de grupo
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

    # Guardar df actualizado en session_state (opcional)
    st.session_state.df_restriction_ready = df

    ##__________________EZ_ADDT_UMRDomainComboRecord____________________________

    if generate_addt:
        for _, row in df.iterrows():
            EZ_value_type = "IRREGULAR" if EZtag_selected.upper() == "DATE" else "ADDITIONAL"

            st.session_state.EZ_ADDT.append({
                'ENVZONE(Desc)': EZname,
                'ENVZONE(Val)': EZid,
                'RESTRICTION_ID(Desc)': row["Restriction_id"],
                'RESTRICTION_ID(Val)': ' ',
                'EZ_ADDT_TAG(Desc)': EZ_value_type,
                'EZ_ADDT_TAG(Val)': EZ_value_type,
                'EZ_KEY_NAMES(Desc)': EZtag_selected,
                'EZ_KEY_NAMES(Val)': Ez_Tag[EZtag_selected],
                'EZ_VALUES(Desc)': row["EZ_VALUES"],
                'EZ_VALUES(Val)': row["EZ_VALUES"],
                'LANGCODE(Desc)': 'null',
                'LANGCODE(Val)': ' ',
                'LANGTYPE(Desc)': 'null',
                'LANGTYPE(Val)': ' ',
                'valResult': 'OK'
            })
    

# __________________EZ_TIME_RESTR_UMRDomainComboRecord___________________________

    # Filtrar solo las columnas clave y quitar duplicados
    df_time = df.drop_duplicates(subset=["vehicle_category", "timeFrom_timeTo", "dateFrom_dateTo"]).reset_index(drop=True)

    # Extraer los Restriction_id únicos basados en la combinación clave
    used_restrictions = set()
    for _, row in df_time.iterrows():
        key = (row["vehicle_category"], row["timeFrom_timeTo"], row["dateFrom_dateTo"])
        restriction_id = df.loc[
            (df["vehicle_category"] == key[0]) &
            (df["timeFrom_timeTo"] == key[1]) &
            (df["dateFrom_dateTo"] == key[2]),
            "Restriction_id"
        ].iloc[0]  # Tomamos el primero, porque todos los iguales tienen el mismo

        if restriction_id in used_restrictions:
            continue  # Evitamos duplicados en EZ_TIME_RESTR
        used_restrictions.add(restriction_id)

        st.session_state.EZ_TIME_RESTR.append({
            'Environmental Zone Id(Desc)': EZname,
            'Environmental Zone Id(Val)': EZid,
            'Restriction Id(Desc)': restriction_id,
            'Restriction Id(Val)': ' ',
            'Time From (23:00) - Time To(Desc)': row["timeFrom_timeTo"],
            'Time From (23:00) - Time To(Val)': ' ',
            'Day From - DayTo (01-07)(Desc)': row["dayFrom_dayTo"],
            'Day From - DayTo (01-07)(Val)': ' ',
            'Month From - Month To (1-12)(Desc)': row["monthFrom_monthTo"],
            'Month From - Month To (1-12)(Val)': ' ',
            'Date From (yyyymmdd) - Date to(Desc)': 'null' if EZvr_selected in ['MIN TOTAL WEIGHT', 'MAX TOTAL WEIGHT'] else row['dateFrom_dateTo'],
            'Date From (yyyymmdd) - Date to(Val)': ' ',
            'valResult': 'OK'
        })


    # __________________EZ_RESTR_UMRDomainComboRecord___________________________

    used_restrictions_restr = set()
    for _, row in df_time.iterrows():
        key = (row["vehicle_category"], row["timeFrom_timeTo"], row["dateFrom_dateTo"])
        restriction_id = df.loc[
            (df["vehicle_category"] == key[0]) &
            (df["timeFrom_timeTo"] == key[1]) &
            (df["dateFrom_dateTo"] == key[2]),
            "Restriction_id"
        ].iloc[0]

        if restriction_id in used_restrictions_restr:
            continue
        used_restrictions_restr.add(restriction_id)

        restriction_value_desc = (
            day_texts if EZvr_selected in ['MIN TOTAL WEIGHT', 'MAX TOTAL WEIGHT']
            else EzRest
        )

        st.session_state.EZ_RESTR.append({
            'Environmental Zone Id(Desc)': EZname,
            'Environmental Zone Id(Val)': EZid,
            'Restriction Id(Desc)': restriction_id,
            'Restriction Id(Val)': ' ',
            'Vehicle Category(Desc)': row["vehicle_category"],
            'Vehicle Category(Val)': row["vehicle_category_id"],
            'EZ Vehicle Restrictions(Desc)': EZvr_selected,
            'EZ Vehicle Restrictions(Val)': EZvr_values[EZvr_selected],
            'Restriction Value 1(Desc)': restriction_value_desc,
            'Restriction Value 1(Val)': ' ',
            'Restriction Value 2(Desc)': 'null',
            'Restriction Value 2(Val)': ' ',
            'Override(Desc)': 'null',
            'Override(Val)': ' ',
            'valResult': 'OK'
        })

##__________________EZ_VEH_RESTR_UMRDomainComboRecord____________________________
    
    for vehicle in selected_categories:
        map_desc = EZ_to_Map_Categories.get(vehicle, '')
        map_val = Map_Veh_Categories.get(map_desc, '')
        st.session_state.EZ_VEH_RESTR.append({
                    'Environmental Zone(Desc)': EZname,
                    'Environmental Zone(Val)': EZid,
                    'EZ Vehicle Category(Desc)': vehicle,
                    'EZ Vehicle Category(Val)': vehicle_categories[vehicle],
                    'Map Vehicle Category(Desc)':map_desc,
                    'Map Vehicle Category(Val)':map_val,
                    'valResult': 'OK'
                })
##__________________EZ_DESCRIPTION_UMRDomainComboRecord____________________________
        
    st.session_state.EZ_DESCRIPTION.append({
                    'ENVZONE(Desc)': EZname,	
                    'ENVZONE(Val)':	EZid,
                    'EZ Description(Desc)': EzDesc,	
                    'EZ Description(Val)': ' ',	
                    'EZ Description LANGCODE(Desc)': lang,	
                    'EZ Description LANGCODE(Val)': lang_code,
                    'valResult': 'OK'
                })     
##__________________EZ_WEBSITE_UMRDomainComboRecord____________________________

    st.session_state.EZ_WEBSITE.append({
	                'ENVZONE(Desc)': EZname,
                    'ENVZONE(Val)': EZid,
                    'EZ Website(Desc)': EzWeb,	
                    'EZ Website(Val)':' ',	
                    'EZ Website LANGCODE(Desc)':'null',	
                    'EZ Website LANGCODE(Val)':' ',	
                    'valResult':'OK'
                })

##__________________EZ_DATES_UMRDomainComboRecord____________________________

    st.session_state.EZ_DATES.append({
        'ENVZONE(Desc)': EZname,	
        'ENVZONE(Val)':	EZid,
        'EZVersionDate(Desc)':' ',	
        'EZVersionDate(Val)':' ',
        'EZExtentDate(Desc)':' ',	
        'EZExtentDate(Val)':' ',
        'valResult': 'OK'
    })


##__________________EZ_POLYRESTR_UMRDomainComboRecord____________________________
    # Subclasificación de categorías
    auto_group = {'AUTO', 'CARPOOL', 'MOTORCYCLE', 'THROUGH_TRAFFIC', 'TAXI'}
    truck_group = {'TRUCK', 'DELIVERY TRUCK'}
    bus_group = {'BUS'}
    for vehicle in selected_categories:
        selected_set = set(selected_categories)

        # Determinar tipo de restricción poligonal
        poly_type = None

        if selected_set.issubset(truck_group):
            poly_type = 'TRUCKS ONLY'
        elif selected_set.issubset(auto_group):
            poly_type = 'AUTOS ONLY'
        elif selected_set.issubset(bus_group):
            poly_type = 'BUSES ONLY'
        elif selected_set.issubset(auto_group.union(truck_group, bus_group, {'ALL VEHICLES'})):
            poly_type = 'AUTOS AND TRUCKS'

        # Agregar resultado si se identificó tipo de polígono
    if poly_type:
        st.session_state.EZ_POLYRESTR.append({
                'Environmental Zone(Desc)': EZname,
                'Environmental Zone(Val)': EZid,
                'Polygon Restrictions(Desc)': poly_type,
                'Polygon Restrictions(Val)': Poly_Restr[poly_type],
                'valResult': 'OK'
            })       

unique_veh_restr_df = pd.DataFrame(st.session_state.EZ_VEH_RESTR)
unique_veh_restr_df = unique_veh_restr_df.drop_duplicates(subset=['EZ Vehicle Category(Desc)'])
st.session_state.EZ_VEH_RESTR = unique_veh_restr_df.to_dict(orient='records')

if add_new_city:
    selected_country = st.selectbox("Select Country:", list(Country_Code.keys()))
    selected_category = st.selectbox("Select EZ Category Feature:", list(EZ_CatFeature.keys()))
    add_new_data = st.button('Add New EZ Information')
    # Evitar duplicados por EZid
    exists = any(d['Value'] == EZid for d in st.session_state.ENVZONE_UMR)
    if not exists:
        st.session_state.ENVZONE_UMR.append({
            'Value': EZid,
            'Published Value': EZid,	
            'Description': EZname,	
            'Label': EZname,	
            'Language Code': EzLang,	
            'Published': 'Y',
            'Exonym Language Code': ' ',
            'Exonym Extract Format': ' ',
            'Exonym Name Type': ' ',
            'Exonym Is Exonym Flag': ' ',
            'Exonym Description': ' ',
            'Exonym Published Value': ' ',
            'Trans Language Code': ' ',
            'Trans description': ' ',
            'Transliteration Type': ' '
        })
    
##_______________________ENVZONE_CHAR_UMRDomainComboRecord____________________________
#     
    exists_char = any(d['Environmental Zone(Val)'] == EZid for d in st.session_state.ENVZONE_CHAR) 
    if add_new_data:
        if not exists_char:
            st.session_state.ENVZONE_CHAR.append({
                'Environmental Zone(Desc)': EZname,
                'Environmental Zone(Val)': EZid,
                'Country(Desc)': selected_country,
                'Country(Val)': Country_Code[selected_country],
                'EZ Category(Desc)': selected_category,
                'EZ Category(Val)': EZ_CatFeature[selected_category],
                'valResult': 'OK'
            })



# --- Display DataFrames ---
df_time_restr = pd.DataFrame(st.session_state.EZ_TIME_RESTR)
df_restr = pd.DataFrame(st.session_state.EZ_RESTR)
df_addt = pd.DataFrame(st.session_state.EZ_ADDT)
df_veh_restr = pd.DataFrame(st.session_state.EZ_VEH_RESTR)
df_description = pd.DataFrame(st.session_state.EZ_DESCRIPTION)
df_website = pd.DataFrame(st.session_state.EZ_WEBSITE)
df_polyrestr = pd.DataFrame(st.session_state.EZ_POLYRESTR)
df_dates = pd.DataFrame(st.session_state.EZ_DATES)

st.subheader ("📅EZ_ADDT_RESTRS_UMRDomainComboRe")
st.dataframe(df_addt)

st.subheader("📅EZ_TIME_RESTR_UMRDomainComboRecord")
st.dataframe(df_time_restr)

st.subheader("📅EZ_RESTR_UMRDomainComboRecord")
st.dataframe(df_restr)

st.subheader("📅EZ_VEH_RESTR_UMRDomainComboRecord")
st.dataframe(df_veh_restr)

st.subheader("📅EZ_DESCRIPTION_UMRDomainComboRecord")
st.dataframe(df_description)

st.subheader("📅EZ_WEBSITE_UMRDomainComboRecord")
st.dataframe(df_website)

st.subheader("📅EZ_POLYRESTR_UMRDomainComboRecord")
st.dataframe(df_polyrestr)

st.subheader("📅EZ_DATES_UMRDomainComboRecord")
st.dataframe(df_dates)
 


if add_new_city:
    df_envzone_umr = pd.DataFrame(st.session_state.ENVZONE_UMR)
    st.subheader("📅ENVZONE_UMRDomainValue")
    st.dataframe(df_envzone_umr)

    df_envzone_char = pd.DataFrame(st.session_state.ENVZONE_CHAR)
    st.subheader("📅ENVZONE_CHAR_UMRDomainCombo")
    st.dataframe(df_envzone_char)

# --- Save to Excel as a single file with two sheets ---
from io import BytesIO

# Calcular fecha actual para el nombre del archivo
today_str = datetime.now().strftime("%Y%m%d")
filename = f"{EZname}_METADATA_{today_str}.xlsx"

# Actualizar 'Month From - Month To (1-12)(Desc)' si aplica
if EZvr_selected == 'MIN TOTAL WEIGHT':
    start_month = monthm(startdate)
    end_month = monthm(enddate)
    month_range = f"{start_month}-{end_month}"
    for entry in st.session_state.EZ_TIME_RESTR:
        entry['Month From - Month To (1-12)(Desc)'] = month_range

# Crear archivo Excel en memoria
excel_buffer = BytesIO()
with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
    workbook = writer.book

    def write_sheet_autofit(df, sheet_name):
        df.to_excel(writer, sheet_name=sheet_name, index=False, header=False, startrow=1)

        worksheet = writer.sheets[sheet_name]

        # Escribir encabezados sin formato
        for col_num, column_title in enumerate(df.columns):
            worksheet.write(0, col_num, column_title)

        # Ajustar el ancho de las columnas automáticamente
        for i, col in enumerate(df.columns):
            max_len = max(df[col].astype(str).map(len).max(), len(col)) + 2
            worksheet.set_column(i, i, max_len)
    if generate_addt:
        write_sheet_autofit(df_addt, 'EZ_ADDT_RESTRS_UMRDomainComboRe') 

    write_sheet_autofit(df_time_restr, 'EZ_TIME_RESTR_UMRDomainComboRec')
    write_sheet_autofit(df_restr, 'EZ_RESTR_UMRDomainComboRecord_L')
    write_sheet_autofit(df_veh_restr, 'EZ_VEH_RESTR_UMRDomainComboReco')
    write_sheet_autofit(df_description,'EZ_DESCRIPTION_UMRDomainComboRe')
    write_sheet_autofit(df_website,'EZ_WEBSITE_UMRDomainComboRecord')
    write_sheet_autofit(df_polyrestr,'EZ_POLYRESTR_UMRDomainComboReco')
    write_sheet_autofit(df_dates,'EZ_DATES_UMRDomainComboRecord_L')

    if add_new_city:
        df_envzone_umr = pd.DataFrame(st.session_state.ENVZONE_UMR)
        df_envzone_char = pd.DataFrame(st.session_state.ENVZONE_CHAR)
        write_sheet_autofit(df_envzone_umr, 'ENVZONE_UMRDomainValue_List_')
        write_sheet_autofit(df_envzone_char, 'ENVZONE_CHAR_UMRDomainComboReco')

# Botón de descarga
st.download_button(
    label="Download APAC Metadata Excel File⬇️",
    data=excel_buffer.getvalue(),
    file_name=filename,
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

########################################################################################################
#                                                                                                      #
#                                                MMT FILES                                             #
#                                                                                                      #
########################################################################################################
from io import BytesIO

def convert_df_to_csv(df):
    output = BytesIO()
    df.to_csv(output, index=False, header=False, encoding='utf-8')
    output.seek(0)
    return output.getvalue()

# Inicializar session_state si no existen
for key in ['mmt_addt_df', 'mmt_rest_df', 'mmt_time_restr_df',
            'mmt_addt_csv', 'mmt_rest_csv', 'mmt_time_restr_csv',
            'mmt_addt_filename', 'mmt_rest_filename', 'mmt_time_restr_filename']:
    if key not in st.session_state:
        st.session_state[key] = None

# Si se presiona el botón, genera y guarda en session_state
if st.button('Create MMT Files🗂️'):

    # ---- ADDT ----
    mmt_addt_data = []

    if not df_addt.empty:
        for _, row in df_addt.iterrows():
            mmt_addt_data.append({
                'EZ_ADDT_RESTRS': 'EZ_ADDT_RESTRS',
                'OK': 'OK',
                'ENVZONE_ID': row['ENVZONE(Val)'],
                'Restriction_id': row['RESTRICTION_ID(Desc)'],
                'ADDITIONAL': row['EZ_ADDT_TAG(Desc)'],
                'EZ_KEY_NAME': row['EZ_KEY_NAMES(Val)'],
                'EZ_VALUES': row['EZ_VALUES(Desc)'],
                'NULL': ' ',
                'NULL2': ' ',
                'NULL3': ' ',
                'NULL4': ' ',
                'NULL5': ' ',
                'N': 'N'
            })
        st.session_state["mmt_addt_df"] = pd.DataFrame(mmt_addt_data)[[
            'EZ_ADDT_RESTRS', 'OK', 'ENVZONE_ID', 'Restriction_id',
            'ADDITIONAL', 'EZ_KEY_NAME', 'EZ_VALUES',
            'NULL', 'NULL2', 'NULL3', 'NULL4', 'NULL5', 'N'
        ]]
    else:
        st.session_state["mmt_addt_df"] = pd.DataFrame()  # Para evitar errores si luego se accede

    # ---- REST ----
    mmt_rest_data = []
    for _, row in df_restr.iterrows():
        mmt_rest_data.append({
            'EZ_RESTR': 'EZ_RESTR',
            'OK': 'OK',
            'ENVZONE_ID': row['Environmental Zone Id(Val)'],
            'Restriction_id': row['Restriction Id(Desc)'],
            'vehicle_category_id': row['Vehicle Category(Val)'],
            'EZ_KEY_ID': row['EZ Vehicle Restrictions(Val)'],
            'LICENSE PLATE': row['Restriction Value 1(Desc)'],
            'NULL': ' ',
            'NULL2': ' ',
            'NULL3': ' ',
            'NULL4': ' ',
            'NULL5': ' ',
            'N': 'N'
        })
    st.session_state["mmt_rest_df"] = pd.DataFrame(mmt_rest_data)[[
        'EZ_RESTR', 'OK', 'ENVZONE_ID', 'Restriction_id',
        'vehicle_category_id', 'EZ_KEY_ID', 'LICENSE PLATE',
        'NULL', 'NULL2', 'NULL3', 'NULL4', 'NULL5', 'N'
    ]]

    # ---- TIME_RESTR ----
    mmt_time_restr_data = []
    for _, row in df_time_restr.iterrows():
        mmt_time_restr_data.append({
            'EZ_TIME_RESTR': 'EZ_TIME_RESTR',
            'OK': 'OK',
            'ENVZONE_ID': row['Environmental Zone Id(Val)'],
            'Restriction_id': row['Restriction Id(Desc)'],
            'timeFrom_timeTo': row['Time From (23:00) - Time To(Desc)'],
            'dayFrom_dayTo': row['Day From - DayTo (01-07)(Desc)'],
            'monthFrom_monthTo': row['Month From - Month To (1-12)(Desc)'],
            'dateFrom_dateTo': 'null',
            'NULL': ' ',
            'NULL2': ' ',
            'NULL3': ' ',
            'NULL4': ' ',
            'N': 'N'
        })
    st.session_state["mmt_time_restr_df"] = pd.DataFrame(mmt_time_restr_data)[[
        'EZ_TIME_RESTR', 'OK', 'ENVZONE_ID', 'Restriction_id',
        'timeFrom_timeTo', 'dayFrom_dayTo', 'monthFrom_monthTo',
        'dateFrom_dateTo', 'NULL', 'NULL2', 'NULL3', 'NULL4', 'N'
    ]]

    # ---- CSVs y nombres ----
    st.session_state["mmt_addt_csv"] = convert_df_to_csv(st.session_state["mmt_addt_df"])
    st.session_state["mmt_rest_csv"] = convert_df_to_csv(st.session_state["mmt_rest_df"])
    st.session_state["mmt_time_restr_csv"] = convert_df_to_csv(st.session_state["mmt_time_restr_df"])

    today_str = datetime.now().strftime("%Y%m%d")
    st.session_state["mmt_addt_filename"] = f"ADD_EZ_ADDT_REST_{EZname}_{EZid}_{today_str}.csv"
    st.session_state["mmt_rest_filename"] = f"ADD_EZ_REST_{EZname}_{EZid}_{today_str}.csv"
    st.session_state["mmt_time_restr_filename"] = f"ADD_EZ_TIME_RESTR_{EZname}_{EZid}_{today_str}.csv"

# Mostrar siempre los resultados si existen
if st.session_state["mmt_addt_df"] is not None:
    st.write("### 📊 ADD_EZ_ADDT_RESTRS DataFrame:")
    st.dataframe(st.session_state["mmt_addt_df"])

if st.session_state["mmt_rest_df"] is not None:
    st.write("### 📊 ADD_EZ_REST DataFrame:")
    st.dataframe(st.session_state["mmt_rest_df"])

if st.session_state["mmt_time_restr_df"] is not None:
    st.write("### 📊 ADD_EZ_TIME_RESTR DataFrame:")
    st.dataframe(st.session_state["mmt_time_restr_df"])

# Mostrar siempre los botones si existen los archivos
if st.session_state["mmt_addt_csv"]:
    st.write("### 📥 Download files:")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.download_button("📄 Download ADD_EZ_ADDT_RESTRS",
            data=st.session_state["mmt_addt_csv"],
            file_name=st.session_state["mmt_addt_filename"],
            mime="text/csv")

    with col2:
        st.download_button("📄 Download ADD_EZ_REST",
            data=st.session_state["mmt_rest_csv"],
            file_name=st.session_state["mmt_rest_filename"],
            mime="text/csv")

    with col3:
        st.download_button("📄 Download ADD_EZ_TIME_RESTR",
            data=st.session_state["mmt_time_restr_csv"],
            file_name=st.session_state["mmt_time_restr_filename"],
            mime="text/csv")
