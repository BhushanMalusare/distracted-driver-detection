# Driver Monitoring System

This project uses MediaPipe to detect hand and face landmarks and alert the driver if they are using their mobile phone while driving.

<a href=""><img src="distracted_driver_without_phone.png" width="40%" alt="Image 1"></a>
<a href=""><img src="distracted_driver_with_phone.png" width="40%" alt="Image 2"></a>

## Setup

### 1. Create a Virtual Environment

Open a terminal and run the following command to create a virtual environment:

- `python -m venv venv`

### 2. Activate the Virtual Environment

Activate the virtual environment:

- `venv\Scripts\activate` (on Windows)
- `source venv/bin/activate` (on macOS/Linux)

### 3. Install Required Libraries

Install the required libraries by running:

- `pip install -r requirements.txt`

### 4. Run the Application

Run the streamlit application:

- `streamlit run streamlit_app.py`

By pressing on `Start`, it will start detecting the distracted driver in realtime.

If you want to stop the live streaming, press `End` button