import streamlit as st
import pandas as pd
import os

# Function to load the CSV file
def load_csv(file_path):
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    return pd.DataFrame()

# Function to save data to CSV
def save_to_csv(data, file_path):
    existing_data = load_csv(file_path)
    updated_data = pd.concat([existing_data, data], ignore_index=True)
    updated_data.drop_duplicates(subset=['Matric Number'], keep='last', inplace=True)
    updated_data.to_csv(file_path, index=False)

# Set page config
st.set_page_config(page_title="MGS 500 Serial Number Lookup", layout="centered")

# Main app
st.title("MGS 500 Serial Number Lookup")

# Load the CSV files
serial_data = load_csv("data/serial_numbers.csv")
registered_data = load_csv("data/registered_students.csv")

# Create form
with st.form("student_form"):
    name = st.text_input("Enter your name")
    matric_number = st.text_input("Enter your matric number (6 digits)")
    submitted = st.form_submit_button("Submit")
    st.write(serial_data["MATRIC NUMBER"].values)

if submitted:
    if len(matric_number) != 6 or not matric_number.isdigit():
        st.error("Please enter a valid 6-digit matric number.")
    else:
        # Check if matric number exists in the CSV
        if matric_number in serial_data["SERIAL NUMBER"].values:
            serial_number = serial_data[serial_data["MATRIC NUMBER"] == matric_number]["SERIAL NUMBER"].values[0]
            st.markdown(f"<h1 style='text-align: center;'>Your Serial Number is:</h1>", unsafe_allow_html=True)
            st.markdown(f"<h1 style='text-align: center; font-size: 48px;'>{serial_number}</h1>", unsafe_allow_html=True)
            
            # Save to registered students CSV
            new_data = pd.DataFrame({"Name": [name], "Matric Number": [matric_number], "Serial Number": [serial_number]})
            save_to_csv(new_data, "registered_students.csv")
            
            st.success("Your information has been recorded.")
        else:
            st.error("Details not yet registered. Please contact the course rep.")
