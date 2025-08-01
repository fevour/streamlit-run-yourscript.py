import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime
import os
import sys

# Add backend to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")

# Page configuration
st.set_page_config(
    page_title="AI-Powered Healthcare Operations Dashboard",
    page_icon="🏥",
    layout="wide"
)

st.title("🏥 AI-Powered Healthcare Operations Dashboard")
st.markdown("**Manipal Hospitals - Inside Operations Centric**")

# Sample data for demonstration
sample_patients = [
    {"id": "PAT_001", "name": "Patient_001", "age": 65, "gender": "Male", "department": "Cardiology", "critical_alerts": 2},
    {"id": "PAT_002", "name": "Patient_002", "age": 42, "gender": "Female", "department": "Emergency", "critical_alerts": 1},
    {"id": "PAT_003", "name": "Patient_003", "age": 58, "gender": "Male", "department": "Internal Medicine", "critical_alerts": 0},
    {"id": "PAT_004", "name": "Patient_004", "age": 73, "gender": "Female", "department": "Neurology", "critical_alerts": 3},
    {"id": "PAT_005", "name": "Patient_005", "age": 29, "gender": "Male", "department": "Orthopedics", "critical_alerts": 0},
]

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Choose a page", [
    "Dashboard Overview", 
    "Patient Management", 
    "Smart Notes Generator", 
    "Critical Alerts"
])

if page == "Dashboard Overview":
    st.header("📊 Dashboard Overview")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Patients", len(sample_patients))
    with col2:
        total_alerts = sum(p['critical_alerts'] for p in sample_patients)
        st.metric("Critical Alerts", total_alerts)
    with col3:
        st.metric("Today's Appointments", 8)
    with col4:
        st.metric("Active Departments", 5)
    
    # Department distribution
    st.subheader("Patient Distribution by Department")
    dept_data = {}
    for patient in sample_patients:
        dept = patient['department']
        dept_data[dept] = dept_data.get(dept, 0) + 1
    
    df = pd.DataFrame(list(dept_data.items()), columns=['Department', 'Count'])
    st.bar_chart(df.set_index('Department'))
    
    # Critical alerts
    st.subheader("⚠️ Recent Critical Alerts")
    critical_patients = [p for p in sample_patients if p['critical_alerts'] > 0]
    for patient in critical_patients:
        st.error(f"**{patient['name']}** - {patient['department']}: {patient['critical_alerts']} critical alerts")

elif page == "Patient Management":
    st.header("👥 Patient Management")
    
    # Search
    search_term = st.text_input("Search patients by name or ID")
    
    # Display patients
    for patient in sample_patients:
        if not search_term or search_term.lower() in patient['name'].lower() or search_term.lower() in patient['id'].lower():
            with st.expander(f"{patient['name']} - {patient['department']} (ID: {patient['id']})"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Age:** {patient['age']}")
                    st.write(f"**Gender:** {patient['gender']}")
                with col2:
                    if patient['critical_alerts'] > 0:
                        st.error(f"**Critical Alerts:** {patient['critical_alerts']}")
                    else:
                        st.success("**No Critical Alerts**")

elif page == "Smart Notes Generator":
    st.header("📝 Smart Notes Generator")
    st.markdown("**AI-powered clinical note generation**")
    
    # Patient selection
    patient_names = [f"{p['name']} ({p['id']})" for p in sample_patients]
    selected_patient = st.selectbox("Select Patient", patient_names)
    note_type = st.selectbox("Note Type", ["Progress Note", "Discharge Summary"])
    
    if st.button("Generate Smart Note", type="primary"):
        if selected_patient:
            # Find selected patient
            patient_id = selected_patient.split("(")[1].split(")")[0]
            patient = next(p for p in sample_patients if p['id'] == patient_id)
            
            # Generate note
            current_date = datetime.now().strftime('%Y-%m-%d')
            
            if note_type == "Progress Note":
                note_content = f"""PROGRESS NOTE
Patient: {patient['name']} (Age: {patient['age']}, {patient['gender']})
Department: {patient['department']}
Date: {current_date}

ASSESSMENT:
Patient continues treatment in {patient['department']}. 
{'⚠️ CRITICAL ALERTS: Urgent attention required for abnormal lab values.' if patient['critical_alerts'] > 0 else 'No critical alerts at this time.'}

PLAN:
- Continue current treatment protocol
- Monitor vital signs and lab values
- Follow-up as scheduled
- Patient education on condition management

NEXT STEPS:
Follow-up appointment scheduled for next week.
"""
            else:  # Discharge Summary
                note_content = f"""DISCHARGE SUMMARY
Patient: {patient['name']} (Age: {patient['age']}, {patient['gender']})
Discharge Date: {current_date}

HOSPITAL COURSE:
Patient was admitted to {patient['department']} for treatment.
{'Critical values were monitored and addressed.' if patient['critical_alerts'] > 0 else 'Hospital stay was uncomplicated.'}

DISCHARGE CONDITION:
Stable and improved

DISCHARGE INSTRUCTIONS:
- Take medications as prescribed
- Follow-up with primary care physician
- Return if symptoms worsen
"""
            
            st.success("Note generated successfully!")
            st.text_area("Generated Note", note_content, height=400)

elif page == "Critical Alerts":
    st.header("🚨 Critical Alerts Management")
    
    # Sample critical alerts
    alerts = [
        {"patient": "Patient_001", "test": "WBC", "value": 15.2, "normal": "4.0-11.0 K/uL", "time": "08:30:00"},
        {"patient": "Patient_002", "test": "Glucose", "value": 250, "normal": "70-100 mg/dL", "time": "10:00:00"},
        {"patient": "Patient_004", "test": "BP", "value": "180/95", "normal": "120/80 mmHg", "time": "11:20:00"},
    ]
    
    if alerts:
        st.warning(f"Found {len(alerts)} critical alerts requiring attention!")
        
        # Display alerts
        for alert in alerts:
            st.error(f"**{alert['patient']}** - {alert['test']}: {alert['value']} (Normal: {alert['normal']}) - {alert['time']}")
        
        # Alert summary chart
        st.subheader("Alert Summary by Test Type")
        test_counts = {}
        for alert in alerts:
            test = alert['test']
            test_counts[test] = test_counts.get(test, 0) + 1
        
        df = pd.DataFrame(list(test_counts.items()), columns=['Test Type', 'Count'])
        st.bar_chart(df.set_index('Test Type'))
    else:
        st.success("🎉 No critical alerts at this time!")

# Footer
st.markdown("---")
st.markdown("**Compliance:** HIPAA Compliant | All patient data is anonymized")
