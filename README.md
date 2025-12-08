# CW2_M01036580_CST1510
# Week 7: Secure Authentication System
Student Name: [Athalia Kacy Mbwambo]
Student ID: [M01036580]
Course: CST1510 -CW2 - Multi-Domain Intelligence Platform
## Project Description
A command-line authentication system implementing secure password hashing
This system allows users to register accounts and log in with proper pass
## Features
- Secure password hashing using bcrypt with automatic salt generation
- User registration with duplicate username prevention
- User login with password verification
- Input validation for usernames and passwords
- File-based user data persistence
## Technical Implementation
- Hashing Algorithm: bcrypt with automatic salting
Data Storage: Plain text file (`users.txt`) with comma-separated values
- Password Security: One-way hashing, no plaintext storage
- Validation: Username (3-20 alphanumeric characters), Password (6-50 characters)
## Week8: Data Pipeline & CRUD (SQL)
## What this contains
- Database layer (`app/data/`)
- Business logic for migration & auth (`app/services/user_service.py`)
- CSV data files in `DATA/`
- SQLite DB created at `DATA/intelligence_platform.db`

## Quick start
1. Create and activate a virtual environment.
2. `pip install -r requirements.txt`
3. Initialize DB:
   `python main.py init`
4. Migrate Week 7 users and CSVs:
   `python main.py migrate`
5. (Optional) Run Streamlit UI in later weeks.

## Notes
- `DATA/users.txt` expected format: `username:password` per line.
- CSVs should have columns as described in the assignment.
- ## Week 9 – Multi-Domain Platform Features

In Week 9, we focused on building the **core platform** using Streamlit, integrating interactive components, session management, and secure login features.

### Key Features

1. **Core Streamlit Functions**
   - `st.text_input()`, `st.button()`, `st.form()`
   - `st.dataframe()`, `st.metric()`, `st.line_chart()`

2. **Session State Management**
   - Initialize variables and persist data across reruns.
   - Manage user session data and chat history.

3. **Authentication & Security**
   - Login and registration flows.
   - Role-based access control for pages and features.
   - Password hashing for secure user data storage.

4. **Multipage Navigation**
   - Implemented using `st.switch_page()` and a `pages/` folder structure.
   - Seamless navigation between dashboards, analytics, and admin tools.

5. **CRUD & Database Integration**
   - Create, Read, Update, Delete operations using forms and database manager.
   - Dynamic data updates reflected in the interface.

6. **Domain Visualizations**
   - Cybersecurity, Data Science, and IT Operations dashboards.
   - Metrics, charts, and tables to visualize KPIs and trends.
   - Delta metrics to highlight changes over time.

---

## Week 10 – Enhancements and Domain Intelligence

In Week 10, the platform was extended with **advanced domain intelligence features**, including AI integration, enhanced visualizations, and real-time analytics.

### Key Enhancements

1. **AI-Powered Domain Assistance**
   - Integrated language models for domain-specific recommendations.
   - Chat interface for Cybersecurity, Data Science, and IT Operations.

2. **Enhanced Visualizations**
   - Interactive charts with filters and domain-specific metrics.
   - Real-time data insights using `st.line_chart()` and `st.bar_chart()`.

3. **Advanced CRUD Operations**
   - Connected forms to database tables.
   - Added record validation, error handling, and dynamic updates.

4. **Role-Based Dashboards**
   - Admin users can manage all domain data.
   - Standard users access only their own records and analytics.

5. **Session Persistence & State Management**
   - User interactions, chat history, and data selections maintained across reruns.
   - Improved multi-page navigation with consistent session state.

---
