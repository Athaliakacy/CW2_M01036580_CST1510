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

## Week 10 – AI-Powered Multi-Domain Assistants

In Week 10, the platform was extended to integrate **AI-powered assistants** using the Gemini API, with both console-based and Streamlit interfaces. The focus was on building interactive chat assistants for Cybersecurity, Data Science, and IT Operations, integrated with the existing multi-domain platform.

---

### Part 1: Text-Based Gemini Ai (Python)

- **Gemini API Setup**
  - Obtain Gemini API key and purchase minimum credits ($5).  
  - Install the Gemini library:  
    ```bash
    pip install google-generativeai
    ```
  - Create the first API call to test connectivity.

- **Interactive Console Chat**
  - Implement a console-based chat with **conversation history**.  
  - Maintain previous messages for context.  

- **Secure API Key Storage**
  - Store the API key securely using an **`.env` file**.  
  - Load API keys using Python’s `dotenv` library to avoid exposing credentials.

---

### Part 2: Streamlit Integration

- **Secrets Management**
  - Configure API key in `streamlit/secrets.toml` for secure access.  

- **Chat Interface**
  - Build interactive chat using:
    - `st.chat_message()` – display user and assistant messages.  
    - `st.chat_input()` – input field for user messages.  
  - Implement **streaming responses** with `stream=True` for real-time feedback.  

- **Sidebar Controls**
  - Add **Clear Chat** button to reset conversation.  
  - Display **message counter** to track conversation length.

---

### Part 3: Domain-Specific Assistants

- **Specialized System Prompts**
  - Create tailored prompts for:
    - **Cybersecurity** – analyze threats and incidents.  
    - **Data Science** – provide analytics, statistics, and visualization guidance.  
    - **IT Operations** – troubleshoot infrastructure and manage tickets.

- **Integration with Database**
  - Connect AI assistants with Week 8 database:
    - Analyze incidents, IT tickets, and datasets.  
    - Provide AI-guided recommendations based on stored data.


