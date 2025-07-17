# 🎬 MovieBooking - Cloud Based Online Movie Ticket Booking System

A cloud-based movie booking application developed using Python and SQL. This system offers seamless access for users, managers, and business partners (e.g., theater owners), making the movie ticket booking process fast, secure, and convenient.

## 🌐 Overview

Developed in 2024, this project was designed to streamline movie ticket reservations through an intuitive web interface backed by a cloud-hosted database. It leverages cloud services (e.g., Azure) for hosting and scalability, ensuring real-time performance and accessibility.

## 🚀 Key Features

- 👤 User Login & Registration  
- 🎟️ Browse & Book Movie Tickets  
- 🗓️ Date and Time Slot Selection  
- 💳 Payment Integration (Placeholder)  
- 🏢 Theater Owner Dashboard to manage screenings  
- 🛠️ Manager Panel to control access, settings, and analytics  
- 🌍 Cloud-Hosted SQL Database for scalable data management  
- 📱 Responsive UI with Bootstrap and custom styling  

## 🛠️ Technologies Used

Component          | Technology         
------------------ | -------------------
Backend            | Python (Flask)     
Frontend           | HTML, CSS, JS      
UI Framework       | Bootstrap          
Database           | MySQL (Cloud-hosted)
Deployment         | Azure Cloud        
Scripting          | JavaScript, jQuery 
Date/Time Picker   | picker.js          

## 📁 Folder Structure

MovieBooking/
├── app.py                  # Main Flask application  
├── import mysql.py         # Database connection/setup  
├── DATABASE FILE/          # SQL or DB structure files  
├── templates/              # HTML templates (Flask Jinja)  
├── static/  
│   ├── styles.css  
│   ├── icons/  
│   ├── themes/  
│   ├── themes-source/  
│   ├── js/  
│   └── fonts/  
├── compressed/             # Optional compressed assets  
├── translations/           # Language/locale support  
├── 01 LOGIN DETAILS & PROJECT INFO.txt  
└── README.md  

## ⚙️ Setup Instructions

1. Clone the Repository:
   git clone https://github.com/PavanKumarBaduru/MovieBooking.git  
   cd MovieBooking  

2. Install Dependencies:
   Ensure Python 3 and pip are installed. Run:
   pip install -r requirements.txt  
   (Or manually install: pip install flask mysql-connector-python)

3. Set Up MySQL Database:
   - Run the SQL scripts provided in `DATABASE FILE/`
   - Update database credentials in `import mysql.py` or app config

4. Run the Application:
   python app.py  
   Visit http://localhost:5000 in your browser

## 🧑‍💼 User Roles

- Admin/Manager: Manage movies, screenings, and users  
- User: Browse and book tickets  
- Theater Owner: Upload and manage available shows  

## 📌 To Do

- Add payment gateway integration (e.g., Razorpay, Stripe)  
- Add OTP-based email/mobile verification  
- Enhance admin analytics with charts  
- Dockerize the application for easier deployment  

## 📄 License

This project is for academic and learning purposes. You may modify and use it with appropriate credit.

## 👨‍💻 Author

Pavan Kumar Baduru  
GitHub: https://github.com/PavanKumarBaduru  
