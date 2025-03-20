🚦 Pico y Placa Generator 2 (PPG2)
Environmental Zone Project – Here Technologies (2025)
Author: Emi Santos T – SDS2
Last Updated: 19 March 2025

📄 Description
Pico y Placa Generator (PPG2) is a Python-based tool designed to automate the creation of metadata for vehicle restriction zones, commonly known as "Pico y Placa". This tool simplifies the process by providing a graphical interface through Streamlit, allowing users to easily configure and generate restriction records without modifying the code.

The tool exports the final data as a CSV file, which can be integrated into external systems for vehicle control and monitoring.

🚀 Features
✅ User-friendly interface: Built with Streamlit for easy interaction.
✅ Flexible restriction settings: Configure vehicle categories, date ranges, and restriction values.
✅ Truck-specific restrictions: Option to add weight-based restrictions only when needed.
✅ Holiday handling: Exclude holidays from the restriction periods.
✅ Data export: Export the generated metadata to CSV format.
✅ Duplicate prevention: Ensures no duplicate records are generated.
✅ Open-source: Easily customizable for specific needs.

🔧 Installation
1️⃣ Prerequisites
Make sure you have the following installed:

Python 3.x
Streamlit
Pandas
2️⃣ Installation Steps
1 - Clone or download the repository:
git clone <repository_url>
cd Pico_y_Placa_Generator
Create a virtual environment (optional but recommended):
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate      # Windows
Install the required dependencies:
pip install -r requirements.txt
▶️ Usage
  Run the application:
    streamlit run app.py
  Configure the settings:
    Enter the zone name and zone ID.
    Select vehicle categories and specify restriction values.
    Define the date range and time periods.
    Optionally, add truck weight restrictions with the "Add Truck Information" button.
    Press "Generar DataFrame" to create the restriction records.
  Export the data:
    Review the generated DataFrame in the interface.
    Download the metadata as a CSV file.
    
  ⚙️ Configuration Options

✅ Vehicle Categories
  AUTO: Cars
  CARPOOL: Shared vehicles
  MOTORCYCLE: Motorcycles
  THROUGH_TRAFFIC: Transit vehicles
  TAXI: Taxis
  TRUCK: Trucks (supports weight-based restrictions)
  BUS: Buses

🛑 Restriction Values
License Plate Number: Restriction by plate digits.
Max_Total_Weight: Restriction by truck weight.
Override: Custom exceptions or overrides.

📆 Holidays
Enter holidays in DDMMYYYY format.
The generator automatically excludes holidays from the restriction period.

🛠️ Customization
You can modify the code to include additional restriction types, validation rules, or custom export formats by editing the Python script.
🐞 Troubleshooting
  🔥 Common Issues
  Duplicate records: Ensure you press "Add Truck Information" only once for the selected date range.
  Streamlit errors: If you encounter issues, try clearing the Streamlit cache:
    streamlit cache clear
  Incorrect date formatting: Make sure to use DDMMYYYY format for holidays and proper date selection for the restriction periods.

📝 License
This project is open-source and can be freely used and modified.
If you use or extend this project, please provide attribution to Emi Santos Tinoco – SDS1 and Here Technologies.
