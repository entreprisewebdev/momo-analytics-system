# MoMo Analytics System

## About the Team

We are **EMS Systems**, a team of Software Engineering students passionate about using technology to solve real-world problems. We work together to build practical, accessible, and user-centered solutions that respond to people’s needs and make everyday experiences better.

## Project Description

The **MoMo Analytics System** is a full-stack application designed to process and analyze Mobile Money (MoMo) SMS transaction data provided in XML format. The system will extract, clean, normalize, and categorize transaction data before storing it in a relational database. The processed data will then be used to provide a frontend dashboard for analyzing and visualizing transaction information.

## Team Members

* **Isingizwe Mukama Elohim Malaïka**
* **Erica Sheja**
* **Ishimwe Samuel**

## System Architecture

The planned system will follow this workflow:

**MoMo XML Data → XML Parser → Data Cleaning & Normalization → Transaction Categorization → Database → API → Frontend Dashboard**

The architecture will allow the system to process raw transaction data and transform it into useful information that can be explored through the dashboard.

### Architecture Diagram

[View our System Architecture](PASTE-DRAWIO-OR-MIRO-LINK-HERE)

The architecture diagram is also available in the repository:

## Scrum Board

We use a Scrum board to organize our work, track progress, and collaborate throughout the development process.

[View our Scrum Board](PASTE-SCRUM-BOARD-LINK-HERE)

Our board contains the following stages:

* **To Do** – Tasks that have not yet been started
* **In Progress** – Tasks currently being worked on
* **Done** – Completed tasks

## Project Structure

momo-analytics-system
.
├── README.md
├── .env.example
├── requirements.txt
├── index.html
├── web/
│   ├── styles.css
│   ├── chart_handler.js
│   └── assets/
├── data/
│   ├── raw/
│   ├── processed/
│   └── logs/
│       └── dead_letter/
├── etl/
│   ├── __init__.py
│   ├── config.py
│   ├── parse_xml.py
│   ├── clean_normalize.py
│   ├── categorize.py
│   ├── load_db.py
│   └── run.py
├── api/
│   ├── __init__.py
│   ├── app.py
│   ├── db.py
│   └── schemas.py
├── scripts/
└── tests/
    ├── test_parse_xml.py
    ├── test_clean_normalize.py
    └── test_categorize.py
```

## Planned Features

* Parse MoMo SMS transaction data from XML.
* Clean and normalize transaction information.
* Categorize different types of transactions.
* Store structured transaction data in a relational database.
* Provide API endpoints for accessing transactions and analytics.
* Display transaction data through an interactive dashboard.
* Visualize transaction trends and summaries using charts and tables.
* Handle invalid or unparsed data through logging and a dead-letter system.

## Technologies

The project is planned to use:

* **Python** – ETL and backend processing
* **SQLite** – Relational database
* **FastAPI** – Backend API
* **HTML, CSS & JavaScript** – Frontend
* **Git & GitHub** – Version control and collaboration
* **Draw.io / Miro** – System architecture
* **GitHub Projects / Scrum Board** – Project management

## Collaboration

We use Git and GitHub to collaborate as a team. Each team member will work on assigned tasks using feature branches and submit changes for review before merging them into the main branch.

## Project Status

**Current Phase:** Week 1 – Project Setup and Planning

During this phase, we are setting up the shared repository, defining the system architecture, organizing the project structure, and creating our Scrum board.
