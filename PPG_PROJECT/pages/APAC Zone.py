import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
import os
from io import BytesIO


st.title('PPG APAC 🚙')

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
        'EZ_KEY_NAME': EZtag,
        'EZ_ADDT_TAG': EZkeyname,
        'EZ_VALUES': EZval,
        'timeFrom_timeTo': timeft,
        'dayFrom_dayTo': dayft,
        'monthFrom_monthTo': monthft,
        'dateFrom_dateTo': f'{dateft}-{dateft}'
    }

# Convert month to 'MM' format (two digits)
def monthm(varmonth):
    # Ensure varmonth is a datetime object before formatting
    if isinstance(varmonth, datetime):
        return varmonth.strftime('%m')
    else:
        # Handle cases where varmonth might be a date object
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
    'MOTORCYCLE': 'MOTORCYCLE', # Changed from 'MOTO' to 'MOTORCYCLE' for consistency
    'THROUGH_TRAFFIC': 'THROUGH_TRAFFIC',
    'TAXI': 'TAXI',
    'TRUCK': 'TRUCK',
    'BUS': 'BUS',
    'DELIVERY TRUCK': 'DELIVERY',
    'ALL VEHICLES': 'ALL_VEHICLE'
}

Lan_Code = {
    'BULGARIAN':'BUL',
    'CATALAN':'CAT',
    'DANISH':'DAN',
    'DUTCH':'DUT',
    'ENGLISH':'ENG',
    'FRENCH':'FRE',
    'GERMAN':'GER',
    'ITALIAN':'ITA',
    'KANNADA':'KAN',
    'POLISH':'POL',
    'PORTUGUESE':'POR',
    'RUSSIAN':'RUS',
    'SPANISH':'SPA',
    'SWEDISH':'SWE',
    'UK ENGLISH':'UKE'
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

if 'records_weekdays' not in st.session_state:
    st.session_state.records_weekdays = []

###########################################################
#                                                         #
#                 INPUTS & DATA DISPLAY                   #
#                                                         #
###########################################################

EZname = st.text_input('Zone Name:', placeholder='Write the name of the Environmental Zone')
EZid = st.text_input('Zone ID:', placeholder='Write the id of the Environmental Zone')
selected_categories = st.multiselect('Vehicle Categories:', list(vehicle_categories.keys()))
EZvr_selected = st.selectbox('Vehicle Restriction Value:', list(EZvr_values.keys()))
EZtag_selected = st.selectbox('EzTag:', list(Ez_Tag.keys()))
EzRest = st.selectbox('EzRestriction:', list(EzRestriction.keys()))
startdate = st.date_input('Start day:', datetime(2025, 1, 1))
enddate = st.date_input('End Day:', datetime(2025, 12, 31))
times = st.text_input('Time Range:', '00:00-23:59')
EzDesc = st.text_input('Ez Description:', placeholder='Write a description of the EZ Restriction')
EzLang = st.selectbox('Lang Description:', ['Select a language...'] + list(Lan_Code.keys()))
EzWeb = st.text_input('Web-Site for EZ:', placeholder='Copy URL')
# Nuevos inputs divididos
EzValDays = st.multiselect('Days to Apply Restriction:', ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
EzValValues = st.multiselect('Restriction Values:', [1, 2, 3, 4, 5, 6, 7, 8, 9, 0, "ODD", "EVEN", "STICKER", "WEIGHT"])
add_new_city = st.checkbox("New City🌐")
# Start/End date to datetime
f1 = startdate
f2 = enddate


# Mapea nombre de día a código
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

# Generador de registros con lógica nueva
def generate_records_batch():
    records = []

    total_days = len(EzValDays)
    total_vals = len(EzValValues)

    if total_days == 0 or total_vals == 0:
        return []

    # Preparar mapeo de días seleccionados
    selected_day_codes = [dayy(day) for day in EzValDays]
    all_days_str = ', '.join(sorted(selected_day_codes))

    # Filtrar los valores especiales y los normales
    special_vals = ['ODD', 'EVEN','WEIGHT']
    normal_vals = [v for v in EzValValues if v not in special_vals]
    special_selected = [v for v in EzValValues if v in special_vals]

    # Procesar valores normales (uno a uno)
    if normal_vals:
        # Repetimos los días si hay más valores
        repeated_days = (EzValDays * ((len(normal_vals) // total_days) + 1))[:len(normal_vals)]
        paired = zip(normal_vals, repeated_days)

        for ez_value, day in paired:
            for category in selected_categories:
                vehicle_category_name = category
                vehicle_category_id = vehicle_categories.get(category, '')

                EZvr_value = EZvr_values[EZvr_selected]
                EZkeyid_value = Ez_Tag[EZtag_selected]
                EZkeyname = EZtag_selected
                timeft = times
                monthft = monthm(f1) + '-' + monthm(f2)
                dateft = f1.strftime('%Y%m%d')

                EZval = str(ez_value)
                day_code = dayy(day)

                record = addreg(
                    EZname, EZid,
                    vehicle_category_name,
                    vehicle_category_id,
                    EZvr_value, EZkeyid_value,
                    EZtag_selected, EZkeyname,
                    EZval, timeft, day_code,
                    monthft, dateft
                )
                records.append(record)

    # Procesar valores especiales (ODD, EVEN)
    for ez_value in special_selected:
        for category in selected_categories:
            vehicle_category_name = category
            vehicle_category_id = vehicle_categories.get(category, '')

            EZvr_value = EZvr_values[EZvr_selected]
            EZkeyid_value = Ez_Tag[EZtag_selected]
            EZkeyname = EZtag_selected
            timeft = times
            monthft = monthm(f1) + '-' + monthm(f2)
            dateft = f1.strftime('%Y%m%d')

            EZval = str(ez_value)

            record = addreg(
                EZname, EZid,
                vehicle_category_name,
                vehicle_category_id,
                EZvr_value, EZkeyid_value,
                EZtag_selected, EZkeyname,
                EZval, timeft, all_days_str,  # aquí agrupamos los días
                monthft, dateft
            )
            records.append(record)

    return records


if EZvr_selected == 'MIN TOTAL WEIGHT':
    min_weight = st.text_input('Enter Min Weight Value:', ' ')
else:
    min_weight = ' '
  

if EZvr_selected == 'MAX TOTAL WEIGHT':
    max_weight = st.text_input('Enter Max Weight Value:', ' ')
else:
    max_weight = ' '      

generate_addt = not (EZvr_selected in ['MAX TOTAL WEIGHT', 'MIN TOTAL WEIGHT'])



# Botón para generar registros
if st.button('Generate Records▶️'):
    new_records = generate_records_batch()
    # Append new records to the existing list in session state
    st.session_state.records_weekdays.extend(new_records)
    st.success(f'{len(new_records)} new records generated! Total records: {len(st.session_state.records_weekdays)}')

    # Create DataFrame from the accumulated records
    df = pd.DataFrame(st.session_state.records_weekdays)

    # Display and process the combined DataFrame
    if not df.empty:
        # Define the desired order for EZ_KEY_NAME
        ez_key_order = [
            'Date', 'LicensePlate', 'LicensePlateEnding', 'LicensePlateStarting',
            'Max Total Weight', 'Min Total Weight', 'Environmental Badge',
            'Absolute Vehicle Age', 'Relative Vehicle Age', 'OVERRIDE'
        ]
        if 'EZ_KEY_NAME' in df.columns:
            df['EZ_KEY_NAME'] = pd.Categorical(df['EZ_KEY_NAME'], categories=ez_key_order, ordered=True)

        df['vehicle_category_rank'] = df['vehicle_category'].apply(lambda x: (0, x) if x == 'AUTO' else (1, x))
        df = df.sort_values(by=['vehicle_category_rank', 'EZ_KEY_NAME', 'dateFrom_dateTo'])
        df = df.drop(columns='vehicle_category_rank')

        if 'EZ_KEY_ID' in df.columns:
            df.loc[df['EZ_KEY_ID'] == 10, 'dateFrom_dateTo'] = df.loc[df['EZ_KEY_ID'] == 10, 'dateFrom_dateTo'].str[:8]
            df.loc[df['EZ_KEY_ID'] == 11, 'dateFrom_dateTo'] = df.loc[df['EZ_KEY_ID'] == 11, 'dateFrom_dateTo'].str[:8]
            df.loc[df['EZ_KEY_ID'] == 12, 'dateFrom_dateTo'] = df.loc[df['EZ_KEY_ID'] == 12, 'dateFrom_dateTo'].str[:8]

    st.session_state.df_processed_for_display = df

    # Descargar como Excel 
    towrite = BytesIO()
    st.session_state.df_processed_for_display.to_excel(towrite, index=False, sheet_name='EZ_RESTRICTIONS')
    towrite.seek(0)
    st.download_button(
        label="Download Excel File",
        data=towrite,
        file_name=f'{EZname}_EZ_Restrictions.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )


if 'df_processed_for_display' not in st.session_state:
    st.session_state.df_processed_for_display = []
df_order =pd.DataFrame(st.session_state.df_processed_for_display)

# Display the processed DataFrame if it exists in session_state
if "df_processed_for_display" in st.session_state:
    st.write('## Previous Data Display :')
    st.write('Ensure that all data is complete and correct before processing the APAC Metadata.')
    st.dataframe(st.session_state.df_processed_for_display)

# Generate dynamic file name for the CSV export
current_year = datetime.now().year
if 'records_weekdays' in st.session_state and st.session_state.records_weekdays:
    df_weekdays_export = pd.DataFrame(st.session_state.records_weekdays)
    file_name = f"EZ_{EZname}_{EZid}_Metadata_{current_year}.csv"
    csv = df_weekdays_export.to_csv(index=False, quoting=1).encode('utf-8')
    

###########################################################
#                                                         #
#                    METADATA APAC                        #
#                                                         #
###########################################################

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


# Botón para crear la metadata y generar el archivo
if st.button(" Create APAC Metadata🔵"):

    # Generar DataFrame base (ya deberías tener df_weekdays generado antes de esto)
    df = df_order.copy()
    lang = EzLang
    lang_code = Lan_Code[lang]
    restriction_counter = 0
##__________________EZ_ADDT_UMRDomainComboRecord____________________________
        
    if generate_addt:    
        for i, row in enumerate(df.iterrows()):
                index, data = row
                # Calcular Restriction_id: cada dos registros, avanza en 1
                restriction_id = (i // 2) + 1

                EZ_value_type = "IRREGULAR" if EZtag_selected.upper() == "DATE" else "ADDITIONAL"

                st.session_state.EZ_ADDT.append({
                    'ENVZONE(Desc)': EZname,
                    'ENVZONE(Val)': EZid,
                    'RESTRICTION_ID(Desc)':'ADD MANUALLY',
                    'RESTRICTION_ID(Val)': ' ',
                    'EZ_ADDT_TAG(Desc)': EZ_value_type,
                    'EZ_ADDT_TAG(Val)': EZ_value_type,
                    'EZ_KEY_NAMES(Desc)': EZtag_selected,
                    'EZ_KEY_NAMES(Val)': Ez_Tag[EZtag_selected],
                    'EZ_VALUES(Desc)': data["EZ_VALUES"],
                    'EZ_VALUES(Val)': data["EZ_VALUES"],
                    'LANGCODE(Desc)': 'null',
                    'LANGCODE(Val)': ' ',
                    'LANGTYPE(Desc)': 'null',
                    'LANGTYPE(Val)': ' ',
                    'valResult': 'OK'
                })

    

##__________________EZ_TIME_RESTR_UMRDomainComboRecord____________________________
    df_time = df.drop_duplicates(subset=['timeFrom_timeTo', 'dayFrom_dayTo', 'vehicle_category']).reset_index(drop=True)
    for i, row in df_time.iterrows():
        new_restriction_id = i + 1
        st.session_state.EZ_TIME_RESTR.append({
            'Environmental Zone Id(Desc)': EZname,
            'Environmental Zone Id(Val)': EZid,
            'Restriction Id(Desc)': new_restriction_id,
            'Restriction Id(Val)': ' ',
            'Time From (23:00) - Time To(Desc)': row["timeFrom_timeTo"],
            'Time From (23:00) - Time To(Val)': ' ',
            'Day From - DayTo (01-07)(Desc)': row["dayFrom_dayTo"],
            'Day From - DayTo (01-07)(Val)': ' ',
            'Month From - Month To (1-12)(Desc)': row["monthFrom_monthTo"] if EZvr_selected == 'MIN TOTAL WEIGHT' or 'MAX TOTAL WEIGHT' else 'null',
            'Month From - Month To (1-12)(Val)': ' ',
            'Date From (yyyymmdd) - Date to(Desc)': 'null',
            'Date From (yyyymmdd) - Date to(Val)': ' ',
            'valResult': 'OK'
        })

##__________________EZ_RESTR_UMRDomainComboRecord____________________________
    df_restr = df.drop_duplicates(subset=['timeFrom_timeTo', 'dayFrom_dayTo', 'vehicle_category']).reset_index(drop=True)
    for i, row in df_restr.iterrows():
        new_restriction_id = i + 1
        if EZvr_selected in 'MIN TOTAL WEIGHT':
            restriction_value_desc = min_weight

        elif EZvr_selected in 'MAX TOTAL WEIGHT':
            restriction_value_desc = max_weight    
        else:
            restriction_value_desc = EzRest

        st.session_state.EZ_RESTR.append({
            'Environmental Zone Id(Desc)': EZname,
            'Environmental Zone Id(Val)': EZid,
            'Restriction Id(Desc)': new_restriction_id,
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

###########################################################
#                                                         #
#                       MMT FILES                         #
#                                                         #
###########################################################
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
