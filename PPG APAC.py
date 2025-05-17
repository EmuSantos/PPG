import streamlit as st
import pandas as pd
from datetime import datetime

st.title('APAC EZ Generator 🚗')
st.markdown("[AMEA Zone](https://n38haaq3fgxptdjm4nqv6t.streamlit.app/) 🚀", unsafe_allow_html=True)
# --- Session State Initialization ---
if 'EZ_TIME_RESTR' not in st.session_state:
    st.session_state.EZ_TIME_RESTR = []
if 'EZ_RESTR' not in st.session_state:
    st.session_state.EZ_RESTR = []
if 'EZ_VEH_RESTR' not in st.session_state:
    st.session_state.EZ_VEH_RESTR = []
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

# --- Inputs ---
EZname = st.text_input('Zone Name:', '')
EZid = st.text_input('Zone ID:', '')
selected_categories = st.multiselect('Vehicle Categories:', list(vehicle_categories.keys()))
EZvr_selected = st.selectbox('Vehicle Restriction Value:', list(EZvr_values.keys()))
EZtag_selected = st.selectbox('EzTag:', list(Ez_Tag.keys()))
ezval_selected = st.selectbox('Restriction Value Type:', list(Ezval))
startdate = st.date_input('Start day:', datetime(2025, 1, 1))
enddate = st.date_input('End Day:', datetime(2025, 12, 31))
times = st.text_input('Time Range:', '00:00-23:59')
selected_days = st.multiselect('Select Days Restriction:', ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])

if EZvr_selected == 'MIN TOTAL WEIGHT':
    min_weight = st.text_input('Enter Min Weigth Value:', '')
else:
    min_weight = ''

if st.button("Generate Data"):
    day_codes = [dayy(day) for day in selected_days]
    start_month = monthm(startdate)
    end_month = monthm(enddate)
    month_range = f"{start_month}-{end_month}"

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

unique_veh_restr_df = pd.DataFrame(st.session_state.EZ_VEH_RESTR)
unique_veh_restr_df = unique_veh_restr_df.drop_duplicates(subset=['EZ Vehicle Category(Desc)'])
st.session_state.EZ_VEH_RESTR = unique_veh_restr_df.to_dict(orient='records')

# --- Display DataFrames ---
df_time_restr = pd.DataFrame(st.session_state.EZ_TIME_RESTR)
df_restr = pd.DataFrame(st.session_state.EZ_RESTR)
df_veh_restr = pd.DataFrame(st.session_state.EZ_VEH_RESTR)


st.subheader("EZ_TIME_RESTR_UMRDomainCombo")
st.dataframe(df_time_restr)

st.subheader("EZ_RESTR_UMRDomainComboRecord")
st.dataframe(df_restr)

st.subheader("EZ_VEH_RESTR_UMRDomainComboReco")
st.dataframe(df_veh_restr)

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

# Botón de descarga
st.download_button(
    label="Download EZ Metadata Excel File",
    data=excel_buffer.getvalue(),
    file_name=filename,
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
