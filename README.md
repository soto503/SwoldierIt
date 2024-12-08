# SwoldierIt Fitness Application

SwoldierIt is a web application designed to provide dynamic workout plans and routines tailored to user preferences.
Users can view and manage workout itineraries and explore various fitness routines.

---

## Features

- User authentication (login and account creation) with hashed passwords using `bcrypt`.
- Personalized workout routines based on splits:
  - **5 Day Split**
  - **PPL (Push, Pull, Legs) Split**
  - **Total Body Split**
- Dynamic data retrieval from a MySQL database.
- Distinction between public and private workout databases.
- Responsive design with intuitive navigation.

---

## Installation and Setup

### Prerequisites

1. **Python** (Version 3.10 or higher).
2. **MySQL** Database Server.
3. Install the required Python packages using `pip` (see below).

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/soto503/SwoldierIt.git
   cd SwoldierIt
   
2. (Recommended) Set up a virtual environment:
   python3 -m venv venv
   source venv/bin/activate
   # On Windows, use `venv\Scripts\activate`
   
4. Install Requirements:
   pip install -r requirements.txt
   
5. Configure the Database:
   Create a MySQL database and update config.py with your database credentials.

6. Run the application:
   python flaskapp.py
   Open the application in your browser at http://127.0.0.1:5000


