# ✈️ Flight IQ
### Web-Based Flight Telemetry Analysis Toolbox & Flight Path Navigator

Flight IQ is a web-based flight telemetry analysis and visualization application built with Python. It combines telemetry comparison, statistical analysis, interactive visualizations, and flight trajectory simulation in a unified dashboard.

The application provides two primary modules:

- **Telemetry Comparison Analyzer:** Compares standard baseline flight data with recorded telemetry data to identify differences in selected parameters.
- **Flight Trajectory Navigator:** Calculates geographical distances and bearings between departure and destination coordinates and visualizes a simulated flight trajectory on a 3D globe.

The application features a futuristic aviation-inspired dashboard with interactive charts, flight metrics, and navigation visualizations.

> **Disclaimer:** Flight IQ is an educational and demonstration project. It uses synthetic/mock telemetry data and simplified mathematical models. It is not certified aviation software and must not be used for real-world flight operations, aircraft control, navigation decisions, or safety-critical applications.

---

## 📸 Application Preview

### Telemetry Analysis Dashboard

![Flight Telemetry Analysis Dashboard](analyzer_preview.png)

### Flight Path Navigator

![Flight Path Navigator](navigator_preview.png)

---

## ✨ Features

### 1. Telemetry Comparison Analyzer

The telemetry analysis module allows users to compare standard baseline telemetry data against recorded flight data.

**Features include:**

- Upload standard baseline data in CSV format.
- Upload recorded flight telemetry in CSV format.
- Generate synthetic demonstration datasets when uploaded files are not provided.
- Select multiple telemetry parameters for comparison.
- Calculate and display average values for selected parameters.
- Calculate differences between baseline and recorded averages.
- Visualize telemetry trends using interactive charts.
- Display pitch and roll indicators.
- Present a cockpit-inspired interface with status indicators and event-feed styling.

**Supported example parameters:**

- Pitch
- Roll
- Yaw
- Airspeed
- Altitude
- Time

The analyzer expects compatible column names and corresponding numeric data in the uploaded datasets.

### 2. Flight Trajectory Navigator

The flight navigation module provides a visual representation of a simulated route between two geographical coordinates.

**Features include:**

- Enter departure latitude and longitude.
- Enter destination latitude and longitude.
- Specify initial altitude and target cruise speed.
- Calculate approximate geographical distance using the Haversine formula.
- Calculate the initial bearing between two geographical points.
- Generate a simplified flight altitude profile.
- Calculate intermediate geographical waypoints.
- Display calculated navigation data in a table.
- Visualize the simulated trajectory on a 3D spherical Earth model.
- Animate the simulated aircraft's movement along the route.

### 3. Interactive Dashboard

- Aviation-inspired dark interface.
- Neon-blue visual styling.
- Interactive Plotly charts.
- Flight telemetry metrics and indicators.
- Navigation between the two application modules.
- Demonstration login screen.

**Note:** Some displayed cockpit indicators and system-status values are illustrative UI elements rather than live measurements from an aircraft.

---

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application logic and calculations |
| Streamlit | Web application framework and interactive interface |
| Pandas | Data loading, tabular processing, and analysis |
| NumPy | Numerical calculations and mathematical operations |
| Plotly | Interactive charts and 3D trajectory visualization |
| Docker | Containerization |
| Docker Compose | Container configuration and execution |

---

## 📁 Project Structure

```text
flight-IQ/
│
├── app.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
│
├── logo.png
├── analyzer_preview.png
├── navigator_preview.png
│
├── standard dataset sample.csv
├── recorded dataset sample.csv
│
└── README.md
```

The file structure above represents the expected organization of the project. Some files may be absent if they have not been added to the repository.

---

## ⚙️ Installation and Setup

### Prerequisites

Install the following:

- Python 3.10 or a compatible Python version.
- pip, Python's package installer.

Docker is optional if you prefer to run the application directly using Python.

### Step 1: Clone the repository

```bash
git clone https://github.com/barathhmm2004/flight-IQ.git
```

### Step 2: Navigate to the project directory

```bash
cd flight-IQ
```

### Step 3: Create a virtual environment

```bash
python -m venv .venv
```

### Step 4: Activate the virtual environment

**Windows:**

```bash
.venv\Scripts\activate
```

**Linux/macOS:**

```bash
source .venv/bin/activate
```

### Step 5: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 6: Run the application

```bash
streamlit run app.py
```

Streamlit will display a local URL in the terminal, usually:

```text
http://localhost:8501
```

Open that address in your browser.

---

## 🐳 Running with Docker

If Docker and Docker Compose are installed, you can use the provided configuration.

From the project directory, run:

```bash
docker compose up --build
```

The supplied Compose configuration maps port `8502` on the host to port `8501` in the container.

Open:

```text
http://localhost:8502
```

To stop the container, press `Ctrl+C`. If the container is still running in the background, use:

```bash
docker compose down
```

---

## 📊 Sample Dataset Format

The telemetry analyzer accepts CSV files containing compatible numeric telemetry parameters.

Example structure:

```csv
Time_sec,Pitch_deg,Yaw_deg,Roll_deg,Airspeed_knots,Altitude_ft
0,1.5,0.0,0.1,420,35000
1,1.6,0.2,0.3,421,35010
2,1.4,0.4,-0.1,419,35020
```

The example above is illustrative. Your actual uploaded CSV files may use different values and column names.

For meaningful comparisons, the baseline and recorded datasets should contain corresponding telemetry parameters with compatible units.

If a parameter is missing from the baseline dataset, the application may be unable to calculate its baseline difference.

---

## 🧮 Mathematical Concepts Used

### Haversine Formula

The Haversine formula calculates the approximate great-circle distance between two points on a spherical Earth using their latitudes and longitudes.

It is used to estimate the distance between departure and destination coordinates.

### Initial Bearing

The initial bearing calculation estimates the compass direction from the departure point toward the destination point.

### Telemetry Statistics

The analyzer calculates average values for selected parameters and displays differences between the baseline and recorded datasets.

### 3D Coordinate Transformation

Geographical coordinates are converted into three-dimensional Cartesian coordinates to visualize the flight trajectory on a spherical Earth model.

---

## 🔐 Authentication and Security

The current application includes a demonstration login interface.

The authentication mechanism is intended for demonstration purposes and should not be considered production-grade security.

Do not reuse demonstration credentials for real accounts or services.

Before deploying the application publicly, replace the hardcoded credentials with an appropriate authentication mechanism and review the application's access controls.

---

## 🧪 Data and Simulation Disclaimer

Flight IQ uses synthetic/mock telemetry data created for demonstration and educational purposes.

The displayed flight metrics, navigation paths, system indicators, and simulation outputs are not live aircraft telemetry.

The application uses simplified calculations and assumptions. Its outputs have not been validated or certified for aviation use.

This project is intended for software development, data visualization, numerical analysis, and educational experimentation.

**Do not use Flight IQ for real-world aircraft navigation, flight planning, aircraft control, or safety-critical decisions.**

---

## 🚧 Limitations

- Telemetry comparisons depend on compatible dataset structures and column names.
- The current statistical comparison focuses on average values and visual trends.
- The trajectory navigator uses simplified geographical and altitude-profile calculations.
- The simulated trajectory does not account for real-world aviation constraints such as air traffic restrictions, aircraft performance limits, weather, or certified flight-planning requirements.
- Some cockpit indicators and system-status displays use illustrative values.
- Authentication requires further development before production deployment.

---

## 🔮 Future Enhancements

Potential future improvements include:

- Support for additional telemetry file formats.
- Improved validation of uploaded datasets.
- More statistical comparison metrics.
- Automated anomaly and deviation detection.
- Exportable analysis reports.
- Improved route and waypoint visualization.
- More robust authentication and authorization.
- Automated testing and deployment.
- Additional data validation and error handling.

---

## 👨‍💻 Author

**Barath M M**

Computer Science and Design Engineering Graduate  
University of Mysore

[LinkedIn Profile](https://www.linkedin.com/in/barath-mm-66a839303)

---

## 📄 License

No license has been specified yet.

Unless a license is added, others should not assume they have permission to reuse, modify, or redistribute the project's code.

---

**Flight IQ — Exploring flight telemetry through data analysis and interactive visualization.**
