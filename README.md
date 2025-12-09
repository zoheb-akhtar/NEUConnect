# NEU Connect — CS 3200 Fall 2025 Team Project

NEU Connect is a mentorship and networking platform that connects current Northeastern students with alumni mentors. The system supports role-based functionality across four personas: Student, Alumni, System Administrator, and Data Analyst.

Check out the video demo here: https://youtu.be/Tv12KHTkoKo

## Team members

- Alex Sun
- Brendan Keefe
- David Wu
- Jenyne Pham
- Zoheb Akhtar

## Prerequisites

- Git
- Docker Desktop

## Architecture

- Frontend: Streamlit
- Backend: Flask (REST)
- Database: MySQL
- Deployment: Docker Compose

## Repository Structure

- ./app — Streamlit frontend
- ./api — Flask REST API
- ./database-files — SQL schema + mock data

## User Personas

### Student

- Browse/search alumni
- Send mentorship/connection requests
- Manage student profile

### Alumni

- Review incoming requests
- Accept/reject connections
- Manage availability/profile

### System Administrator

- Review and process applications
- Monitor and resolve reports
- View basic system health/metrics

### Data Analyst

- View engagement summaries
- Analyze connection trends
- Review alumni/company analytics

## Setup Instructions

### Clone the repository

git clone <YOUR_REPO_URL>
cd <YOUR_REPO_FOLDER>

### Create your .env file

- copy api/.env.template
- rename to just .env
- open api/.env
- change MYSQL_ROOT_PASSWORD to your own password

### Start all containers

docker compose up -d --build

### Open the app

- open browser
- http://localhost:8501

## Initialize Database

### Re-running SQL after changes

docker compose down db -v
docker compose up db -d
