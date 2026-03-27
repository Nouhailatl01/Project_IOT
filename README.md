# 🌡️ Smart Cold Chain Monitoring System
📌 Project Overview

Project Overview

This project aims to develop an intelligent monitoring system for medical refrigerators that automates temperature surveillance and alerts based on critical thresholds. The system is controlled by an ESP8266 microcontroller and provides real-time monitoring via a web dashboard.

🚀 Features

- Automated Temperature Monitoring: Continuously monitors refrigerator temperature 24/7 without manual intervention
- Instant Email Alerts: Sends immediate notifications when temperature goes out of bounds (2°C - 8°C)
- Automatic Escalation: Progressively alerts multiple operators if no action is taken
- Real-time Dashboard: Web-based interface for monitoring and control
- MQTT Communication: Lightweight IoT protocol for reliable data transmission
- Multi-operator Support: Allows team coordination with automatic responsibility escalation
- Complete Audit Trail: Records all incidents for medical compliance and traceability

🛠️ Technologies Used

Hardware: ESP8266, DHT11 Sensor, Temperature/Humidity Sensor, MQTT Broker
Backend: Django (Python), REST API, PostgreSQL
Frontend: React, HTML, CSS, JavaScript, Chart.js
Cloud Services: PythonAnywhere (Hosting & Deployment)

 Project Structure

📁 Smart-Cold-Chain/
 ├── 📂 DHT/                 # Main Django app
 ├── 📂 projet/              # Django configuration
 ├── 📂 templates/           # HTML & web interface
 ├── 📂 static/              # CSS, JavaScript, images
 ├── 📂 hardware/            # ESP8266 firmware & sensors
 ├── 📂 docs/                # Documentation
 ├── 📂 scripts/             # Utility scripts
 ├── 📂 tests/               # Test suite
 ├── 📜 README.md            # Project documentation

👥 Team Members

Nouhaila Touil

👥 Team Responsibilities

Role	Tasks
Sensor Setup & MQTT	ESP8266 configuration, data transmission
Backend Development	Django API, Escalation Logic, Email Alerts
Database Management	PostgreSQL Schema, Data Management
Frontend Development	React Dashboard, Real-time Updates, UI/UX Design
Testing & Debugging	Unit Tests, Integration Tests, System Validation
DevOps & Deployment	PythonAnywhere Setup, Production Configuration

🚀 How to Set Up the Project

Hardware Setup: Connect ESP8266 with DHT11 sensor and power supply.
Backend Setup: Install dependencies with `pip install -r requirements.txt` and run migrations.
Database Configuration: Initialize database with `python manage.py migrate`.
Web Dashboard: Start development server with `python manage.py runserver`.
MQTT Configuration: Set up MQTT broker and configure connection in Django settings.
Production Deployment: Deploy on PythonAnywhere with environment variables configured.

📌 Future Enhancements

- Mobile application for operator alerts
- Machine learning for predictive maintenance
- Multi-location support for laboratory networks
- Advanced analytics with trend analysis and reporting
- SMS notifications in addition to email alerts
- Integration with hospital management systems
- Weather-based optimization for monitoring schedules
- Redundancy and backup systems for critical failures

🎭 Interactive Demonstration Techniques

Real-time Simulations: Simulate temperature deviations to observe alert triggers and escalation chain.
Live Monitoring: Watch dashboard updates as incidents are detected and processed.
Alert Testing: Trigger test alerts to verify email delivery and notification timing.
Audit Trail Verification: Show complete incident history and operator actions.
Performance Visualization: Display response times and escalation metrics in real-time.
Anomaly Detection: Demonstrate system identification and response to critical deviations.

📞 Contact

For questions or contributions, feel free to contact:

**Author:** Nouhaila Touil
**Email:** nouhaila.touil.23@ump.ac.ma
**University:** Université Mohammed Premier (UMP)

---

**Version 1.0 | Status: Production Ready**
