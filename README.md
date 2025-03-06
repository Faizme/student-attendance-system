# Student Attendance System

A facial recognition-based **Student Attendance System** built with **Streamlit, OpenCV, and Face Recognition**. This application detects student faces in real-time, marks attendance, and allows users to download the attendance report as an Excel file.

## 🚀 Features
- 📷 **Real-time Face Recognition** using OpenCV and Face Recognition.
- 📊 **Automated Attendance Marking** with student details.
- 💾 **Downloadable Attendance Report** in Excel format.
- 🖥️ **Simple & Interactive UI** using Streamlit.

## 📂 Folder Structure
```
Attendance_System
|   app.py
|   student_list.xlsx
|
\---images
        Ajal Josh.jpg
        Allan Thomas.jpg
        Gautham V V.jpg
        Mohammed Faiz.jpg
        Mohammed Zaid Fareed.jpg
```

## 🛠️ Installation
### 1️⃣ Clone the Repository
```bash
git clone https://github.com/yourusername/student-attendance-system.git
cd student-attendance-system
```

### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Run the Application
```bash
streamlit run app.py
```

## 📜 Usage
1. Add student images to the `images/` folder.
2. Ensure `student_list.xlsx` contains student details (Name, CID, UID).
3. Run the app and allow webcam access.
4. Recognized students will be marked as **present**.
5. Click **Download Attendance Report** to get the Excel file.

## 🤖 Technologies Used
- Python 🐍
- OpenCV 🎥
- Face Recognition 🤖
- Pandas 📊
- Streamlit ⚡

---

💡 *Feel free to contribute or raise issues!* 😊

