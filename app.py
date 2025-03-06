import cv2
import numpy as np
import face_recognition
import pandas as pd
import os
from datetime import datetime
import streamlit as st
from io import BytesIO

# Function to load student images
def load_student_images(path):
    student_images = []
    student_names = []
    image_list = os.listdir(path)

    for img_name in image_list:
        img_path = os.path.join(path, img_name)
        img = cv2.imread(img_path)
        if img is None:
            st.warning(f"Could not load {img_name}. Skipping...")
            continue

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encodings = face_recognition.face_encodings(img)
        
        if len(encodings) > 0:
            student_images.append(encodings[0])
            student_names.append(os.path.splitext(img_name)[0])  # Remove file extension
            st.success(f"Encoded face for {img_name}")
        else:
            st.warning(f"No face detected in {img_name}. Skipping...")

    return student_images, student_names

# Streamlit App
st.set_page_config(page_title="🎓 Student Attendance System", layout="centered")
st.title("🎓 Student Attendance System")
st.write("This application uses facial recognition to mark student attendance in real-time.")

# Initialize session state
if 'student_images' not in st.session_state:
    st.session_state.student_images = []
if 'student_names' not in st.session_state:
    st.session_state.student_names = []
if 'attendance_records' not in st.session_state:
    st.session_state.attendance_records = []
if 'recognized_names' not in st.session_state:
    st.session_state.recognized_names = []

# Sidebar for settings
st.sidebar.header("Settings")

# Load student list from Excel
student_df = pd.read_excel("student_list.xlsx")
student_dict = student_df.set_index("Name")[['CID', 'UID']].to_dict(orient='index')

# Automatically load student images
path = 'images'
if os.path.exists(path):
    if not st.session_state.student_images:  # Load only once
        st.session_state.student_images, st.session_state.student_names = load_student_images(path)
        st.success(f"Loaded {len(st.session_state.student_images)} student faces: {', '.join(st.session_state.student_names)}")
else:
    st.error(f"The folder '{path}' does not exist. Please create it and add student images.")

# Initialize webcam
st.subheader("Live Webcam Feed")
st.write("Scanning faces for attendance...")

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    st.error("Could not access webcam.")
else:
    # Placeholder for webcam feed
    webcam_placeholder = st.empty()

    stop_button = st.button("Stop Webcam")

    while not stop_button:
        success, frame = cap.read()
        if not success:
            st.error("Could not read frame from webcam.")
            break

        # Resize frame for faster processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        small_frame_rgb = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        # Detect face locations using CNN
        face_locations = face_recognition.face_locations(small_frame_rgb, model="cnn")  # Using CNN model
        face_encodings = face_recognition.face_encodings(small_frame_rgb, face_locations)

        for face_encoding, face_loc in zip(face_encodings, face_locations):
            matches = face_recognition.compare_faces(st.session_state.student_images, face_encoding)
            face_distances = face_recognition.face_distance(st.session_state.student_images, face_encoding)
            
            if len(face_distances) > 0:
                best_match_index = np.argmin(face_distances)

                if matches[best_match_index]:
                    name = st.session_state.student_names[best_match_index]
                    
                    # Fetch UID and CID from student list
                    if name in student_dict:
                        uid = student_dict[name]['UID']
                        cid = student_dict[name]['CID']
                        st.success(f"Recognized: {name} | Attendance Marked for UID: {uid}, CID: {cid}")
                    else:
                        st.warning(f"No UID/CID found for {name}. Skipping...")
                        continue
                    
                    # Mark attendance
                    if name not in st.session_state.recognized_names:
                        st.session_state.recognized_names.append(name)
                        st.session_state.attendance_records.append({
                            "Name": name,
                            "UID": uid,
                            "CID": cid,
                            "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        })

                    # Draw rectangle and label
                    y1, x2, y2, x1 = [i * 4 for i in face_loc]  # Scale back up
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, name, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        # Show webcam output
        webcam_placeholder.image(frame, channels="BGR", use_column_width=True)

        if stop_button:
            break

    cap.release()
    st.write("Webcam closed.")

# Provide a download button for attendance records
if st.session_state.attendance_records:
    df = pd.DataFrame(st.session_state.attendance_records)
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Attendance')
        writer.close()
    output.seek(0)

    st.download_button(
        label="Download Attendance Report",
        data=output,
        file_name="attendance_report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    st.subheader("Attendance List")
    st.dataframe(df)
else:
    st.warning("No attendance records found.")