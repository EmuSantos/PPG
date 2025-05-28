import streamlit as st
import pandas as pd
from datetime import datetime

st.title('PPG APAC 🚙')


# --- Session State Initialization ---
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
if 'restriction_id_counter' not in st.session_state:
    st.session_state.restriction_id_counter = 1

# --- Utility Functions ---
def monthm(varmonth):
    return varmonth.strftime('%m')

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

# --- Static Dictionaries ---
vehicle_categories = {
    'AUTO': 3,
    'CARPOOL': 16,
    'MOTO': 2,
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
    'RELATIVE VEHICLE AGE': 'REL_VEH_AGE'
}

Ez_Tag = {
    'LicensePlate': 3,
    'LicensePlateEnding': 5,
    'LicensePlateStarting': 7,
    'Max Total Weight': 8,
    'Min Total Weight': 9,
    'Environmental Badge': 10,
    'Absolute Vehicle Age': 11,
    'Relative Vehicle Age': 12,
    'OVERRIDE': 13
}

Ezval = {
    'ODD', 
    'EVEN', 
    'UVVRP'}

EZ_to_Map_Categories = {
    'AUTO': 'AUTOMOBILE',
    'CARPOOL': 'CARPOOL',
    'MOTO': 'MOTORCYCLE',
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

Badge_Value = {
	'DEU_GREEN_STICKER'
	'DEU_RED_STICKER'
	'DEU_YELLOW_STICKER'
	'AUT_EURO_I_STICKER'
	'AUT_EURO_II_STICKER'
	'AUT_EURO_III_STICKER'
	'AUT_EURO_IV_STICKER'
	'AUT_EURO_V_STICKER'
	'AUT_EURO_VI_STICKER'
	'MEX_HOLOGRAMA_0'
	'MEX_HOLOGRAMA_00'
	'MEX_HOLOGRAMA_1'
	'MEX_HOLOGRAMA_2'
	'MEX_HOLOGRAMA_EXEMPT'
	'MEX_HOLOGRAMA_FOREIGN'
	'FRA_CRITAIR'
	'FRA_CRITAIR_1'
	'FRA_CRITAIR_2'
	'FRA_CRITAIR_3'
	'FRA_CRITAIR_4'
	'FRA_CRITAIR_5'
	'SPA_CAT_ZERO_STICKER'
	'SPA_CAT_ECO_STICKER'
	'SPA_CAT_B_STICKER'
	'SPA_CAT_C_STICKER' }

Country_Code = {
	'AUSTRIA':	9,
	'BELGIUM':	5,
	'BOLIVIA':	506,
	'BRAZIL':	507,
	'BULGARIA':	19,
	'CHILE':	509,
	'COLOMBIA':	510,
	'COSTA RICA':	511,
	'DENMARK':	16,
	'ECUADOR':	515,
	'ENGLAND':	28,
	'FRANCE':	2,
	'GERMANY':	3,
	'GREECE':	27,
	'INDIA':	217,
	'INDONESIA':	218,
	'ITALY':	1,
	'MEXICO':	527,
	'NETHERLANDS':	6,
	'PERU':		532,
	'PHILIPPINES':	237,
	'POLAND':	43,
	'PORTUGAL':	32,
	'RUSSIA':	45,
	'SCOTLAND':	29,
	'SPAIN':	22,
	'SWEDEN':	23 
}

EZ_CatFeature = {
	'POLYGONAL FEATURE':'P',
	'LINEAR FEATURE':'L',
	'FEATURE POINT':'F'
}

# --- Inputs ---
EZname = st.text_input('Zone Name:', placeholder='Type EZ Name')
EZid = st.text_input('Zone ID:', placeholder='Type EZ ID')
selected_categories = st.multiselect('Vehicle Categories:', list(vehicle_categories.keys()))
EZvr_selected = st.selectbox('Vehicle Restriction Value:', list(EZvr_values.keys()))
EZtag_selected = st.selectbox('EzTag:', list(Ez_Tag.keys()))
ezval_selected = st.selectbox('Restriction Value Type:', list(Ezval))
startdate = st.date_input('Start day:', datetime(2025, 1, 1))
enddate = st.date_input('End Day:', datetime(2025, 12, 31))
times = st.text_input('Time Range:', '00:00-23:59')
selected_days = st.multiselect('Select Days Restriction:', ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
EzDesc = st.text_input('Ez Description:', placeholder='Write a description of the EZ Restriction')
EzLang =st.selectbox('Lang Description:',['Select a language...'] + list(Lan_Code.keys()))
EzWeb =st.text_input ('Web-Site for EZ:',placeholder='Copy URL')




if EZvr_selected == 'MIN TOTAL WEIGHT':
    min_weight = st.text_input('Enter Min Weigth Value:', '')
else:
    min_weight = ''

if st.button("Generate Data"):
    day_codes = [dayy(day) for day in selected_days]
    start_month = monthm(startdate)
    end_month = monthm(enddate)
    month_range = f"{start_month}-{end_month}"
    lang = EzLang
    lang_code = Lan_Code[lang]
    
    if ezval_selected == 'UVVRP':
        for day_code in day_codes:
            for vehicle in selected_categories:
                map_desc = EZ_to_Map_Categories.get(vehicle, '')
                map_val = Map_Veh_Categories.get(map_desc, '')
                
                st.session_state.EZ_TIME_RESTR.append({
                    'Environmental Zone Id(Desc)': EZname,
                    'Environmental Zone Id(Val)': EZid,
                    'Restriction Id(Desc)': st.session_state.restriction_id_counter,
                    'Restriction Id(Val)':' ',
                    'Time From (23:00) - Time To(Desc)': times,
                    'Time From (23:00) - Time To(Val)':' ',
                    'Day From - DayTo (01-07)(Desc)': day_code,
                    'Day From - DayTo (01-07)(Val)':' ',
                    'Month From - Month To (1-12)(Desc)': 'null',
                    'Month From - Month To (1-12)(Val)':' ',
                    'Date From (yyyymmdd) - Date to(Desc)': 'null',
                    'Date From (yyyymmdd) - Date to(Val)':' ',
                    'valResult': 'OK'
                })

                st.session_state.EZ_RESTR.append({
                    'Environmental Zone Id(Desc)': EZname,
                    'Environmental Zone Id(Val)': EZid,
                    'Restriction Id(Desc)': st.session_state.restriction_id_counter,
                    'Restriction Id(Val)':' ',
                    'Vehicle Category(Desc)': vehicle,
                    'Vehicle Category(Val)': vehicle_categories[vehicle],
                    'EZ Vehicle Restrictions(Desc)': EZvr_selected,
                    'EZ Vehicle Restrictions(Val)': EZvr_values[EZvr_selected],
                    'Restriction Value 1(Desc)': ezval_selected,
                    'Restriction Value 1(Val)':' ',
                    'Restriction Value 2(Desc)': 'null',
                    'Restriction Value 2(Val)':' ',
                    'Override(Desc)': 'null',
                    'Override(Val)':' ',
                    'valResult': 'OK'
                })

                st.session_state.EZ_VEH_RESTR.append({
                    'Environmental Zone(Desc)': EZname,
                    'Environmental Zone(Val)': EZid,
                    'EZ Vehicle Category(Desc)': vehicle,
                    'EZ Vehicle Category(Val)': vehicle_categories[vehicle],
                    'Map Vehicle Category(Desc)': map_desc,
                    'Map Vehicle Category(Val)': map_val,
                    'valResult': 'OK'
                })

                

                st.session_state.restriction_id_counter += 1

    else:
        day_code_str = ', '.join(day_codes)
        for vehicle in selected_categories:
            # Solo asignar el mes si la restricción es MIN TOTAL WEIGHT, de lo contrario dejar 'null'
            month_value = month_range if EZvr_selected == 'MIN TOTAL WEIGHT' else 'null'
            map_desc = EZ_to_Map_Categories.get(vehicle, '')
            map_val = Map_Veh_Categories.get(map_desc, '')
            
            st.session_state.EZ_TIME_RESTR.append({
                'Environmental Zone Id(Desc)': EZname,
                'Environmental Zone Id(Val)': EZid,
                'Restriction Id(Desc)': st.session_state.restriction_id_counter,
                'Restriction Id(Val)':' ',
                'Time From (23:00) - Time To(Desc)': times,
                'Time From (23:00) - Time To(Val)':' ',
                'Day From - DayTo (01-07)(Desc)': day_code_str,
                'Day From - DayTo (01-07)(Val)':' ',
                'Month From - Month To (1-12)(Desc)': month_value,
                'Month From - Month To (1-12)(Val)':' ',
                'Date From (yyyymmdd) - Date to(Desc)': 'null',
                'Date From (yyyymmdd) - Date to(Val)':' ',
                'valResult': 'OK'
            })

            st.session_state.EZ_RESTR.append({
                'Environmental Zone Id(Desc)': EZname,
                'Environmental Zone Id(Val)': EZid,
                'Restriction Id(Desc)': st.session_state.restriction_id_counter,
                'Restriction Id(Val)':' ',
                'Vehicle Category(Desc)': vehicle,
                'Vehicle Category(Val)': vehicle_categories[vehicle],
                'EZ Vehicle Restrictions(Desc)': EZvr_selected,
                'EZ Vehicle Restrictions(Val)': EZvr_values[EZvr_selected],
                'Restriction Value 1(Desc)': min_weight if EZvr_selected == 'MIN TOTAL WEIGHT' else ezval_selected,
                'Restriction Value 1(Val)':' ',
                'Restriction Value 2(Desc)': 'null',
                'Restriction Value 2(Val)':' ',
                'Override(Desc)': 'null',
                'Override(Val)':' ',
                'valResult': 'OK'
            })
            st.session_state.EZ_VEH_RESTR.append({
                    'Environmental Zone(Desc)': EZname,
                    'Environmental Zone(Val)': EZid,
                    'EZ Vehicle Category(Desc)': vehicle,
                    'EZ Vehicle Category(Val)': vehicle_categories[vehicle],
                    'Map Vehicle Category(Desc)':map_desc,
                    'Map Vehicle Category(Val)':map_val,
                    'valResult': 'OK'
                })

            st.session_state.restriction_id_counter += 1

##__________________EZ_DESCRIPTION_UMRDomainComboRecord_________________________

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
    auto_group = {'AUTO', 'CARPOOL', 'MOTO', 'THROUGH_TRAFFIC', 'TAXI'}
    truck_group = {'TRUCK', 'DELIVERY TRUCK'}
    bus_group = {'BUS'}

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

##__________________________ENVZONE_UMRDomainValue____________________________

add_new_city = st.checkbox("New EZ City")


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


if add_new_city:
    df_envzone_umr = pd.DataFrame(st.session_state.ENVZONE_UMR)
    st.subheader("ENVZONE_UMRDomainValue")
    st.dataframe(df_envzone_umr)

    df_envzone_char = pd.DataFrame(st.session_state.ENVZONE_CHAR)
    st.subheader("ENVZONE_CHAR_UMRDomainCombo")
    st.dataframe(df_envzone_char)

 

# --- Display DataFrames ---
df_time_restr = pd.DataFrame(st.session_state.EZ_TIME_RESTR)
df_restr = pd.DataFrame(st.session_state.EZ_RESTR)
df_veh_restr = pd.DataFrame(st.session_state.EZ_VEH_RESTR)
df_description = pd.DataFrame(st.session_state.EZ_DESCRIPTION)
df_website = pd.DataFrame(st.session_state.EZ_WEBSITE)
df_polyrestr = pd.DataFrame(st.session_state.EZ_POLYRESTR)
df_dates = pd.DataFrame(st.session_state.EZ_DATES)

st.subheader("EZ_TIME_RESTR_UMRDomainComboRecord")
st.dataframe(df_time_restr)

st.subheader("EZ_RESTR_UMRDomainComboRecord")
st.dataframe(df_restr)

st.subheader("EZ_VEH_RESTR_UMRDomainComboRecord")
st.dataframe(df_veh_restr)

st.subheader("EZ_DESCRIPTION_UMRDomainComboRecord")
st.dataframe(df_description)

st.subheader("EZ_WEBSITE_UMRDomainComboRecord")
st.dataframe(df_website)

st.subheader("EZ_POLYRESTR_UMRDomainComboRecord")
st.dataframe(df_polyrestr)

st.subheader("EZ_DATES_UMRDomainComboRecord")
st.dataframe(df_dates)

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
    label="Download EZ Metadata Excel File",
    data=excel_buffer.getvalue(),
    file_name=filename,
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
