###!/usr/bin/env python3

"""
EZ Metadata Generator
---------------------

This application automatically generates structured metadata in CSV or Excel format 
for environmental restriction zones, based on vehicle categories, applicable days, 
assigned values, schedules, and types of restrictions.

It streamlines the creation of files compatible with traffic management or 
environmental control systems by standardizing the information according to EZ system requirements.

Developed by: Emi Santos  
Creation date: July 2025
"""

import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
import os
from io import BytesIO

# Streamlit Config
st.title('EZ Metadata Creator - APAC 🚙')


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
    'MAX TOTAL WEIGHT': 'MAX_TOTAL_WGHT',
    'MIN TOTAL WEIGHT': 'MIN_TOTAL_WGHT'

}

Ez_Tag = {
    'LicensePlate': 3,
    'LicensePlateEnding': 5,
    'LicensePlateStarting': 7,
    'Date': 1,
    'Max Total Weight': 8,
    'Min Total Weight': 9
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
    'INDONESIAN':'IND',
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
    'LINEAR FEATURE':'L'
}



if 'records_weekdays' not in st.session_state:
    st.session_state.records_weekdays = []

if 'df_processed_for_display' not in st.session_state:
    st.session_state.df_processed_for_display = []

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

if EZvr_values[EZvr_selected] not in ['MAX_TOTAL_WGHT', 'MIN_TOTAL_WGHT']:
    EzRest = st.selectbox('EzRestriction:', list(EzRestriction.keys()))
else:
    EzRest= 'LISENCE PLATE'

    if EzRest != 'UVVRP' and EZvr_values[EZvr_selected] not in ['MAX_TOTAL_WGHT', 'MIN_TOTAL_WGHT']:
        EzValDays = st.multiselect(
            'Days to Apply Restriction:',
            ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        )

        EzValValues = st.multiselect('Restriction Values:', [1, 2, 3, 4, 5, 6, 7, 8, 9, 0, "ODD", "EVEN", "STICKER", "WEIGHT", " "])
        
    else:
        EzValDays = []
        EzValValues = []

if EZvr_values[EZvr_selected] not in ['MAX_TOTAL_WGHT', 'MIN_TOTAL_WGHT']:
    startdate = st.date_input('Start day:', value=default_start)
    enddate = st.date_input('End Day:', value=default_end)
times = st.text_input('Time Range:', '00:00-23:59')
EzDesc = st.text_input('Ez Description:', placeholder='Write a description of the EZ Restriction')
EzLang = st.selectbox('Lang Description:', ['Select a language...'] + list(Lan_Code.keys()))
    
EzWeb = st.text_input('Web-Site for EZ:', placeholder='Copy URL')

# New split inputs
# Hide EzValDays if UVVRP or MAX/MIN WEIGHT is selected

if EzRest != 'UVVRP':
    EzValDays = st.multiselect(
        'Days to Apply Restriction:',
        ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    )
    if EZvr_values[EZvr_selected] not in ['MAX_TOTAL_WGHT', 'MIN_TOTAL_WGHT']:
        EzValValues = st.multiselect('Restriction Values:', [1, 2, 3, 4, 5, 6, 7, 8, 9, 0, "ODD", "EVEN", "STICKER", "WEIGHT", " "])
        
else:
    EzValValues = []
    EzValDays =[]

if  EzRest == 'UVVRP':
    st.markdown("### 🔢 UVVRP Daily Restriction Values")
    ezval = {
        'Monday': st.multiselect('Monday Values:', [1, 2, 3, 4, 5, 6, 7, 8, 9, 0, "ODD", "EVEN", "STICKER", " "]),
        'Tuesday': st.multiselect('Tuesday Values:', [1, 2, 3, 4, 5, 6, 7, 8, 9, 0, "ODD", "EVEN", "STICKER", " "]),
        'Wednesday': st.multiselect('Wednesday Values:', [1, 2, 3, 4, 5, 6, 7, 8, 9, 0, "ODD", "EVEN", "STICKER", " "]),
        'Thursday': st.multiselect('Thursday Values:', [1, 2, 3, 4, 5, 6, 7, 8, 9, 0, "ODD", "EVEN", "STICKER", " "]),
        'Friday': st.multiselect('Friday Values:', [1, 2, 3, 4, 5, 6, 7, 8, 9, 0, "ODD", "EVEN", "STICKER", " "]),
        'Saturday': st.multiselect('Saturday Values:', [1, 2, 3, 4, 5, 6, 7, 8, 9, 0, "ODD", "EVEN", "STICKER", " "]),
        'Sunday': st.multiselect('Sunday Values:', [1, 2, 3, 4, 5, 6, 7, 8, 9, 0, "ODD", "EVEN", "STICKER", " "])
    }

if EZvr_values[EZvr_selected] in ['MAX_TOTAL_WGHT', 'MIN_TOTAL_WGHT']:
    EzValValues = "WEIGHT"

add_new_city = st.checkbox("New City🌐")
# Start/End date to datetime
f1 = startdate
f2 = enddate



# Map day name to code
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



if EZvr_selected == 'MIN TOTAL WEIGHT':
    min_weight = st.text_input('Enter Min Weight Value:', ' ')
else:
    min_weight = ' '

if EZvr_selected == 'MAX TOTAL WEIGHT':
    max_weight = st.text_input('Enter Max Weight Value:', ' ')
else:
    max_weight = ' '

def generate_records_batch():
    records = []

    # Ensure that selected categories exist
    if not selected_categories:
        return []

    selected_day_codes = [dayy(day) for day in EzValDays]
    all_days_str = ', '.join(sorted(selected_day_codes))

        # Special case for MIN and MAX WEIGHT
    if EZvr_values[EZvr_selected] == 'MIN_TOTAL_WGHT' and min_weight.strip():
        for category in selected_categories:
            record = addreg(
                EZname, EZid,
                category,
                vehicle_categories.get(category, ''),
                EZvr_values[EZvr_selected],
                Ez_Tag[EZtag_selected],
                EZtag_selected,
                EZtag_selected,
                str(min_weight.strip()),
                times,
                all_days_str,
                monthm(f1) + '-' + monthm(f2),
                f1.strftime('%Y%m%d')
            )
            records.append(record)
        return records  # 🔴 Stop Here

    elif EZvr_values[EZvr_selected] == 'MAX_TOTAL_WGHT' and max_weight.strip():
        for category in selected_categories:
            record = addreg(
                EZname, EZid,
                category,
                vehicle_categories.get(category, ''),
                EZvr_values[EZvr_selected],
                Ez_Tag[EZtag_selected],
                EZtag_selected,
                EZtag_selected,
                str(max_weight.strip()),
                times,
                all_days_str,
                monthm(f1) + '-' + monthm(f2),
                f1.strftime('%Y%m%d')
            )
            records.append(record)
        return records  # 🔴 Stop Here
    
        # Special case for UVVRP
    if EzRest == 'UVVRP' and ezval:
        for day, values in ezval.items():
            for val in values:
                for category in selected_categories:
                    record = addreg(
                        EZname, EZid,
                        category,
                        vehicle_categories.get(category, ''),
                        EZvr_values[EZvr_selected],
                        Ez_Tag[EZtag_selected],
                        EZtag_selected,
                        EZtag_selected,
                        str(val),
                        times,
                        dayy(day),
                        monthm(f1) + '-' + monthm(f2),
                        f1.strftime('%Y%m%d')
                    )
                    records.append(record)
        return records  #Important so that it does not continue with the rest of the logic
    
    else:
        # Regular values: 1-9, ODD, EVEN, STICKER, etc.
        total_days = len(EzValDays)
        total_vals = len(EzValValues)

        if total_days == 0 or total_vals == 0:
            return []

        special_vals = ['ODD', 'EVEN']
        normal_vals = [v for v in EzValValues if v not in special_vals]
        special_selected = [v for v in EzValValues if v in special_vals]

        if normal_vals:
            repeated_days = (EzValDays * ((len(normal_vals) // total_days) + 1))[:len(normal_vals)]
            paired = zip(normal_vals, repeated_days)

            for ez_value, day in paired:
                for category in selected_categories:
                    record = addreg(
                        EZname, EZid,
                        category,
                        vehicle_categories.get(category, ''),
                        EZvr_values[EZvr_selected],
                        Ez_Tag[EZtag_selected],
                        EZtag_selected,
                        EZtag_selected,
                        str(ez_value),
                        times,
                        dayy(day),
                        monthm(f1) + '-' + monthm(f2),
                        f1.strftime('%Y%m%d')
                    )
                    records.append(record)

        for ez_value in special_selected:
            for category in selected_categories:
                record = addreg(
                    EZname, EZid,
                    category,
                    vehicle_categories.get(category, ''),
                    EZvr_values[EZvr_selected],
                    Ez_Tag[EZtag_selected],
                    EZtag_selected,
                    EZtag_selected,
                    str(ez_value),
                    times,
                    all_days_str,
                    monthm(f1) + '-' + monthm(f2),
                    f1.strftime('%Y%m%d')
                )
                records.append(record)

    return records

generate_addt = not (EZvr_selected in ['MAX TOTAL WEIGHT', 'MIN TOTAL WEIGHT'])

if st.button('Generate Records▶️'):
    new_records = generate_records_batch()
    st.session_state.records_weekdays.extend(new_records)
    st.success(f'{len(new_records)} new records generated! Total records: {len(st.session_state.records_weekdays)}')

    df_weekdays = pd.DataFrame(st.session_state.records_weekdays)

    if not df_weekdays.empty:
        ez_key_order = [
            'Date', 'LicensePlate', 'LicensePlateEnding', 'LicensePlateStarting',
            'Max Total Weight', 'Min Total Weight', 'Environmental Badge',
            'Absolute Vehicle Age', 'Relative Vehicle Age', 'OVERRIDE'
        ]
        if 'EZ_KEY_NAME' in df_weekdays.columns:
            df_weekdays['EZ_KEY_NAME'] = pd.Categorical(df_weekdays['EZ_KEY_NAME'], categories=ez_key_order, ordered=True)

        df_weekdays['vehicle_category_rank'] = df_weekdays['vehicle_category'].apply(lambda x: (0, x) if x == 'AUTO' else (1, x))
        df_weekdays = df_weekdays.sort_values(by=['vehicle_category_rank', 'EZ_KEY_NAME', 'dateFrom_dateTo'])
        df_weekdays = df_weekdays.drop(columns='vehicle_category_rank')

        if 'EZ_KEY_ID' in df_weekdays.columns:
            for key_id in [10, 11, 12]:
                mask = df_weekdays['EZ_KEY_ID'] == key_id
                df_weekdays.loc[mask, 'dateFrom_dateTo'] = df_weekdays.loc[mask, 'dateFrom_dateTo'].str[:8]

        st.session_state.df_processed_for_display = df_weekdays

if 'df_processed_for_display' not in st.session_state:
    st.session_state.df_processed_for_display = []

df_weekdays = pd.DataFrame(st.session_state.records_weekdays)

# CSV export if there are records
if 'records_weekdays' in st.session_state and st.session_state.records_weekdays:
    df_weekdays = pd.DataFrame(st.session_state.records_weekdays)
    file_name = f"EZ_{EZname}_{EZid}_Metadata_{datetime.now().year}.csv"
    csv = df_weekdays.to_csv(index=False, quoting=1).encode('utf-8')

if 'EZ_KEY_NAME' in df_weekdays.columns:
    df_weekdays.sort_values(by='EZ_KEY_NAME', ascending=True, kind='stable', inplace=True)

if 'dateFrom_dateTo' in df_weekdays.columns:
    df_weekdays.sort_values(by='dateFrom_dateTo', ascending=True, kind='stable', inplace=True)

if 'vehicle_category' in df_weekdays.columns:
    df_weekdays.sort_values(by='vehicle_category', ascending=True, kind='stable', inplace=True )
     

# Display message and DataFrame
st.write('## Previous Data Display :')
st.write('Ensure that all data is complete and correct before processing the APAC Metadata.')
st.dataframe(df_weekdays)


########################################################################################################
#                                                                                                      #
#                                            METADATA APAC                                             #
#                                                                                                      #
########################################################################################################

import pandas as pd
import streamlit as st
from io import BytesIO

## Ensure that the necessary variables are defined
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

if 'Restriction_ODDEVEN' not in st.session_state:
    st.session_state.Restriction_ODDEVEN = 1

if st.button(" Create APAC Metadata🔵"):
    df = df_weekdays.copy()
    lang = EzLang
    lang_code = Lan_Code[lang]
    
    df = df.sort_values(by=["vehicle_category", "timeFrom_timeTo", "dayFrom_dayTo"]).reset_index(drop=True)
    
    # Asignar Restriction_id
    restriction_id = 1
    df.at[0, "Restriction_id"] = restriction_id
    for i in range(1, len(df)):
        same_group = (
            df.at[i, "vehicle_category"] == df.at[i - 1, "vehicle_category"] and
            df.at[i, "timeFrom_timeTo"] == df.at[i - 1, "timeFrom_timeTo"] and
            df.at[i, "dayFrom_dayTo"] == df.at[i - 1, "dayFrom_dayTo"]
        )
        if not same_group:
            restriction_id += 1
        df.at[i, "Restriction_id"] = restriction_id

    st.session_state.df_restriction_ready = df

    # __________________EZ_ADDT_UMRDomainComboRecord____________________________
    if generate_addt:
        restriction_id_normal = 1 
        if EzRest == 'ODD-EVEN':
            df = df.sort_values(by=["EZ_ADDT_TAG"], ascending=False).reset_index(drop=True)
        for _, row in df.iterrows():
                EZ_value_type = "IRREGULAR" if str(row["EZ_ADDT_TAG"]).strip().upper() == "DATE" else "ADDITIONAL"
                used_restriction_id = restriction_id_normal if EzRest == 'ODD-EVEN' else row["Restriction_id"]
                
                st.session_state.EZ_ADDT.append({
                    'ENVZONE(Desc)': EZname,
                    'ENVZONE(Val)': EZid,
                    'RESTRICTION_ID(Desc)': used_restriction_id,
                    'RESTRICTION_ID(Val)': ' ',
                    'EZ_ADDT_TAG(Desc)': EZ_value_type,
                    'EZ_ADDT_TAG(Val)': EZ_value_type,
                    'EZ_KEY_NAMES(Desc)': row["EZ_KEY_NAME"],
                    'EZ_KEY_NAMES(Val)': row["EZ_KEY_ID"],
                    'EZ_VALUES(Desc)': row["EZ_VALUES"],
                    'EZ_VALUES(Val)': row["EZ_VALUES"],
                    'LANGCODE(Desc)': 'null',
                    'LANGCODE(Val)': ' ',
                    'LANGTYPE(Desc)': 'null',
                    'LANGTYPE(Val)': ' ',
                    'valResult': 'OK'
                })
                restriction_id_normal += 1

    # __________________EZ_RESTR_UMRDomainComboRecord___________________________
    restriction_id_normal = 1

    if EzRest == 'UVVRP':
        #  Get unique categories from the DataFrame
        df_vehicle_unique = df[['vehicle_category', 'vehicle_category_id']].drop_duplicates()

        for _, row in df_vehicle_unique.iterrows():
            vehicle_desc = row["vehicle_category"]
            vehicle_val = row["vehicle_category_id"]

            for day_name, values in ezval.items():
                if not values:
                    continue  # Skip days without values

                st.session_state.EZ_RESTR.append({
                    'Environmental Zone Id(Desc)': EZname,
                    'Environmental Zone Id(Val)': EZid,
                    'Restriction Id(Desc)': restriction_id_normal,
                    'Restriction Id(Val)': ' ',
                    'Vehicle Category(Desc)': vehicle_desc,
                    'Vehicle Category(Val)': vehicle_val,
                    'EZ Vehicle Restrictions(Desc)': EZvr_selected,
                    'EZ Vehicle Restrictions(Val)': EZvr_values[EZvr_selected],
                    'Restriction Value 1(Desc)': "UVVRP",
                    'Restriction Value 1(Val)': ' ',
                    'Restriction Value 2(Desc)': 'null',
                    'Restriction Value 2(Val)': ' ',
                    'Override(Desc)': 'null',
                    'Override(Val)': ' ',
                    'valResult': 'OK'
                })
                restriction_id_normal += 1

    else:
        for _, row in df.iterrows():
            restriction_value = row['EZ_VALUES']
            if EZvr_selected == 'MAX TOTAL WEIGHT':
                restriction_value = max_weight
            elif EZvr_selected == 'MIN TOTAL WEIGHT':
                restriction_value = min_weight

            st.session_state.EZ_RESTR.append({
                'Environmental Zone Id(Desc)': EZname,
                'Environmental Zone Id(Val)': EZid,
                'Restriction Id(Desc)': restriction_id_normal,
                'Restriction Id(Val)': ' ',
                'Vehicle Category(Desc)': row["vehicle_category"],
                'Vehicle Category(Val)': row["vehicle_category_id"],
                'EZ Vehicle Restrictions(Desc)': EZvr_selected,
                'EZ Vehicle Restrictions(Val)': EZvr_values[EZvr_selected],
                'Restriction Value 1(Desc)': restriction_value,
                'Restriction Value 1(Val)': ' ',
                'Restriction Value 2(Desc)': 'null',
                'Restriction Value 2(Val)': ' ',
                'Override(Desc)': 'null',
                'Override(Val)': ' ',
                'valResult': 'OK'
            })
            restriction_id_normal += 1

   # __________________EZ_TIME_RESTR_UMRDomainComboRecord___________________________
    restriction_id_normal = 1

    if EzRest == 'UVVRP':
        # Get unique categories from the DataFrame
        df_vehicle_unique = df[['vehicle_category', 'vehicle_category_id']].drop_duplicates()

        for day_name, values in ezval.items():
            if not values:
                continue  # Only days with defined values

            day_code = dayy(day_name)

            for _, row in df_vehicle_unique.iterrows():
                vehicle_desc = row["vehicle_category"]
                vehicle_val = row["vehicle_category_id"]

                st.session_state.EZ_TIME_RESTR.append({
                    'Environmental Zone Id(Desc)': EZname,
                    'Environmental Zone Id(Val)': EZid,
                    'Restriction Id(Desc)': restriction_id_normal,
                    'Restriction Id(Val)': ' ',
                    'Time From (23:00) - Time To(Desc)': times,
                    'Time From (23:00) - Time To(Val)': ' ',
                    'Day From - DayTo (01-07)(Desc)': day_code,
                    'Day From - DayTo (01-07)(Val)': ' ',
                    'Month From - Month To (1-12)(Desc)': 'null',
                    'Month From - Month To (1-12)(Val)': ' ',
                    'Date From (yyyymmdd) - Date to(Desc)': 'null',
                    'Date From (yyyymmdd) - Date to(Val)': ' ',
                    'valResult': 'OK'
                })
                restriction_id_normal += 1

    else:
        for _, row in df.iterrows():
            month_val = row["monthFrom_monthTo"] if EzRest != 'UVVRP' else 'null'

            st.session_state.EZ_TIME_RESTR.append({
                'Environmental Zone Id(Desc)': EZname,
                'Environmental Zone Id(Val)': EZid,
                'Restriction Id(Desc)': restriction_id_normal,
                'Restriction Id(Val)': ' ',
                'Time From (23:00) - Time To(Desc)': row["timeFrom_timeTo"],
                'Time From (23:00) - Time To(Val)': ' ',
                'Day From - DayTo (01-07)(Desc)': row["dayFrom_dayTo"],
                'Day From - DayTo (01-07)(Val)': ' ',
                'Month From - Month To (1-12)(Desc)': month_val,
                'Month From - Month To (1-12)(Val)': ' ',
                'Date From (yyyymmdd) - Date to(Desc)': 'null',
                'Date From (yyyymmdd) - Date to(Val)': ' ',
                'valResult': 'OK'
            })
            restriction_id_normal += 1

      
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
    #  Category subclassification
    auto_group = {'AUTO', 'CARPOOL', 'MOTORCYCLE', 'THROUGH_TRAFFIC', 'TAXI'}
    truck_group = {'TRUCK', 'DELIVERY TRUCK'}
    bus_group = {'BUS'}
    for vehicle in selected_categories:
        selected_set = set(selected_categories)

        # Determine type of polygonal restriction
        poly_type = None

        if selected_set.issubset(truck_group):
            poly_type = 'TRUCKS ONLY'
        elif selected_set.issubset(auto_group):
            poly_type = 'AUTOS ONLY'
        elif selected_set.issubset(bus_group):
            poly_type = 'BUSES ONLY'
        elif selected_set.issubset(auto_group.union(truck_group, bus_group, {'ALL VEHICLES'})):
            poly_type = 'AUTOS AND TRUCKS'

        # Add result if polygon type was identified
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
    add_new_data = st.button('Add New City Information')
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
df_addt = pd.DataFrame(st.session_state.EZ_ADDT)
df_restr = pd.DataFrame(st.session_state.EZ_RESTR)
df_time_restr = pd.DataFrame(st.session_state.EZ_TIME_RESTR)
df_veh_restr = pd.DataFrame(st.session_state.EZ_VEH_RESTR)
df_description = pd.DataFrame(st.session_state.EZ_DESCRIPTION)
df_website = pd.DataFrame(st.session_state.EZ_WEBSITE)
df_polyrestr = pd.DataFrame(st.session_state.EZ_POLYRESTR)
df_dates = pd.DataFrame(st.session_state.EZ_DATES)

st.subheader("📅EZ_ADDT_RESTRS_UMRDomainComboRercord")
df_addt = st.data_editor(df_addt, num_rows="dynamic", key="editor_addt")

st.subheader("📅EZ_RESTR_UMRDomainComboRecord")
df_restr = st.data_editor(df_restr, num_rows="dynamic", key="editor_restr")

st.subheader("📅EZ_TIME_RESTR_UMRDomainComboRecord")
df_time_restr = st.data_editor(df_time_restr, num_rows="dynamic", key="editor_time_restr")

st.subheader("📅EZ_VEH_RESTR_UMRDomainComboRecord")
df_veh_restr = st.data_editor(df_veh_restr, num_rows="dynamic", key="editor_veh_restr")

st.subheader("📅EZ_DESCRIPTION_UMRDomainComboRecord")
df_description = st.data_editor(df_description, num_rows="dynamic", key="editor_description")

st.subheader("📅EZ_WEBSITE_UMRDomainComboRecord")
df_website = st.data_editor(df_website, num_rows="dynamic", key="editor_website")

st.subheader("📅EZ_POLYRESTR_UMRDomainComboRecord")
df_polyrestr = st.data_editor(df_polyrestr, num_rows="dynamic", key="editor_polyrestr")

st.subheader("📅EZ_DATES_UMRDomainComboRecord")
df_dates = st.data_editor(df_dates, num_rows="dynamic", key="editor_dates")

if add_new_city:
    df_envzone_umr = pd.DataFrame(st.session_state.ENVZONE_UMR)
    st.subheader("📅ENVZONE_UMRDomainValue")
    df_envzone_umr = st.data_editor(df_envzone_umr, num_rows="dynamic", key="editor_envzone_umr")

    df_envzone_char = pd.DataFrame(st.session_state.ENVZONE_CHAR)
    st.subheader("📅ENVZONE_CHAR_UMRDomainCombo")
    df_envzone_char = st.data_editor(df_envzone_char, num_rows="dynamic", key="editor_envzone_char")

# --- Save to Excel as a single file with two sheets ---
from io import BytesIO

# Calculate current date for file name
today_str = datetime.now().strftime("%Y%m%d")
filename = f"{EZname}_METADATA_{today_str}.xlsx"

#  Update ‘Month From - Month To (1-12)(Desc)’ if applicable
if EZvr_selected == 'MIN TOTAL WEIGHT':
    start_month = monthm(startdate)
    end_month = monthm(enddate)
    month_range = f"{start_month}-{end_month}"
    for entry in st.session_state.EZ_TIME_RESTR:
        entry['Month From - Month To (1-12)(Desc)'] = month_range

# Create Excel file in memory
excel_buffer = BytesIO()
with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
    workbook = writer.book

    def write_sheet_autofit(df, sheet_name):
        df.to_excel(writer, sheet_name=sheet_name, index=False, header=False, startrow=1)

        worksheet = writer.sheets[sheet_name]

        #  Write unformatted headers
        for col_num, column_title in enumerate(df.columns):
            worksheet.write(0, col_num, column_title)

        # Adjust column width automatically
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

# Download button
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
import pandas as pd
from datetime import datetime
import streamlit as st


st.write("### 📤 MMT Files Processor")

# ---------- FUNCTIONS ----------
def convert_df_to_csv(df):
    output = BytesIO()
    df.to_csv(output, index=False, header=False, encoding='utf-8')
    output.seek(0)
    return output.getvalue()

def load_required_sheets(file):
    try:
        xl = pd.ExcelFile(file)
        sheets = xl.sheet_names
        required = ['EZ_RESTR_UMRDomainComboRecord_L', 'EZ_TIME_RESTR_UMRDomainComboRec']
        optional = 'EZ_ADDT_RESTRS_UMRDomainComboRe'
        missing = [s for s in required if s not in sheets]
        if missing:
            raise ValueError(f"❌ The required sheets are missing (REST-TIME): {', '.join(missing)}")
        df_restr = xl.parse('EZ_RESTR_UMRDomainComboRecord_L')
        df_time = xl.parse('EZ_TIME_RESTR_UMRDomainComboRec')
        df_addt = xl.parse(optional) if optional in sheets else pd.DataFrame()
        return df_addt, df_restr, df_time
    except Exception as e:
        raise ValueError(f"Error processing the file: {e}")

# ---------- INITIALIZE ----------
for key in ['mmt_addt_df', 'mmt_rest_df', 'mmt_time_restr_df',
            'mmt_addt_csv', 'mmt_rest_csv', 'mmt_time_restr_csv',
            'mmt_addt_filename', 'mmt_rest_filename', 'mmt_time_restr_filename']:
    if key not in st.session_state:
        st.session_state[key] = None

# ---------- BUTTON: USE PREVIOUS DATA ----------
if st.button('Use Previous Data 🧩'):
    if 'df_addt' in locals() and 'df_restr' in locals() and 'df_time_restr' in locals() and 'df_weekdays' in locals():
        df_addt_use = df_addt
        df_restr_use = df_restr
        df_time_use = df_time_restr
        df_weekdays_use = df_weekdays
    else:
        st.warning("⚠️ No data has been generated within the application yet.")
        st.stop()

    # Extract EZname and EZid
    EZname_unique = df_restr_use['Environmental Zone Id(Desc)'].dropna().unique()
    EZid_unique = df_restr_use['Environmental Zone Id(Val)'].dropna().unique()
    EZname = str(EZname_unique[0])
    EZid = str(EZid_unique[0])
    if len(EZname_unique) > 1 or len(EZid_unique) > 1:
        st.warning("⚠️ Multiple values for EZname or EZid were found. The first one will be used.")

    # Process ADDT
    mmt_addt_data = []
    if not df_addt_use.empty:
        for _, row in df_addt_use.iterrows():
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
        st.session_state["mmt_addt_df"] = pd.DataFrame(mmt_addt_data)

    # Process REST
    mmt_rest_data = []
    min_len = min(len(df_restr_use), len(df_weekdays_use))
    df_restr_trim = df_restr_use.head(min_len)
    df_trim = df_weekdays_use.head(min_len)
    for (_, row), (_, row2) in zip(df_restr_trim.iterrows(), df_trim.iterrows()):
        is_override = row2.get('EZ_VR_VALUES') == 'OVERRIDE'
        mmt_rest_data.append({
            'EZ_RESTR': 'EZ_RESTR',
            'OK': 'OK',
            'ENVZONE_ID': row['Environmental Zone Id(Val)'],
            'Restriction_id': row['Restriction Id(Desc)'],
            'vehicle_category_id': row['Vehicle Category(Val)'],
            'EZ_KEY_ID': row['EZ Vehicle Restrictions(Val)'],
            'LICENSE PLATE': ' ' if is_override else row2['EZ_VALUES'],
            'NULL': ' ', 
            'NULL2': row2['EZ_VALUES'] if is_override else ' ', 
            'NULL3': ' ', 
            'NULL4': ' ', 
            'NULL5': ' ', 
            'N': 'N'
        })
    st.session_state["mmt_rest_df"] = pd.DataFrame(mmt_rest_data)

    # Process TIME_RESTR
    mmt_time_restr_data = []
    for _, row in df_time_use.iterrows():
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
    st.session_state["mmt_time_restr_df"] = pd.DataFrame(mmt_time_restr_data)

    # Save CSVs and filenames
    today_str = datetime.now().strftime("%Y%m%d")
    st.session_state["mmt_addt_csv"] = convert_df_to_csv(st.session_state.get("mmt_addt_df", pd.DataFrame()))
    st.session_state["mmt_rest_csv"] = convert_df_to_csv(st.session_state["mmt_rest_df"])
    st.session_state["mmt_time_restr_csv"] = convert_df_to_csv(st.session_state["mmt_time_restr_df"])
    st.session_state["mmt_addt_filename"] = f"ADD_EZ_ADDT_REST_{EZname}_{EZid}_{today_str}.csv"
    st.session_state["mmt_rest_filename"] = f"ADD_EZ_REST_{EZname}_{EZid}_{today_str}.csv"
    st.session_state["mmt_time_restr_filename"] = f"ADD_EZ_TIME_RESTR_{EZname}_{EZid}_{today_str}.csv"

# ---------- UPLOAD EXTERNAL FILE ----------
uploaded_file = st.file_uploader("📎 Upload external Excel File (.xlsx)", type=['xlsx'])

# ---------- SHOW TABLES AND DOWNLOAD ----------
if st.session_state["mmt_addt_df"] is not None:
    st.write("### 📊 ADD_EZ_ADDT_RESTRS DataFrame:")
    st.dataframe(st.session_state["mmt_addt_df"])

if st.session_state["mmt_rest_df"] is not None:
    st.write("### 📊 ADD_EZ_REST DataFrame:")
    st.dataframe(st.session_state["mmt_rest_df"])

if st.session_state["mmt_time_restr_df"] is not None:
    st.write("### 📊 ADD_EZ_TIME_RESTR DataFrame:")
    st.dataframe(st.session_state["mmt_time_restr_df"])

if st.session_state["mmt_rest_csv"]:
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
