
# Profiler Insight

## Overview

Profiler Insight is an open-source tool that helps data stewards and data analysts gain easy insights into the quality of their data. Through data profiling, users can assess data quality, prioritize cleansing actions, and perform impact analyses. Improving data quality at the source leads to better data throughout all operational processes, ultimately resulting in lower operational costs and more efficient workflows.

## Why Profiler Insight?

Current data profiling tools often provide only superficial insights and typically focus on evaluating data quality at the end of the data lifecycle. Profiler Insight offers deeper and more actionable information from the beginning of the data lifecycle, allowing issues to be addressed and resolved at the source.

## Installation

1. **Install Docker**
   - **Windows/Mac:** Docker Desktop includes Docker Compose functionality. Download Docker Desktop from the [Docker website](https://docs.docker.com/desktop/).

2. **Download the Docker Compose File**
   - Download the Docker Compose file from the [GitHub page](https://github.com/SanderBos1/profilerInsight/blob/main/installation/docker-compose.yml) and save it to your computer in a desired directory.

3. **Start the Docker Containers**
   - Navigate to the directory where you saved the Docker Compose file and execute the following command:
      docker compose -f docker-compose.yml up –detach

## Basic Configuration

Create a `.env` file in the root directory of the project. In this file, specify the database connection and Flask environment configuration. Here is an example of what this file might look like:

```env
SECRET_KEY="default"
ENCRYPTION_KEY="default"

DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=profilerDB
DATABASE_USER=postgres
DATABASE_PASSWORD=test
```

### Explanation of Variables:
- **SECRET_KEY and ENCRYPTION_KEY:** These keys are used to secure the frontend. It is highly recommended to change these values and keep them confidential.
- **Database settings (DATABASE_HOST, DATABASE_PORT, DATABASE_NAME, DATABASE_USER, DATABASE_PASSWORD):** These variables only need to be modified if you intend to use a different database than the default Docker database provided.

## User Guide

### Getting Started

1. **Access the Web Interface:**
   - Open your web browser and go to [http://localhost:8080](http://localhost:8080) to access the Profiler Insight interface.

# User Manual


## Accessing the Web Interface
- Open your web browser and go to [http://localhost:8080](http://localhost:8080) to open the Profiler Insight interface.

## Performing Data Profiling on Files (XLSX & CSV)

1. **Navigate to File Profiler:**
   - Click on "File Profiler" in the left menu.

2. **Add Data Source:**
   - Select "Upload" and click on "Choose File". Choose the desired `.xlsx` or `.csv` file from your local storage.
   - Click on "Submit" to load the data.

3. **Select File:**
   - Use the dropdown menu under "File Profiler" to choose the file you want to analyze.

4. **Analyze Data:**
   - Start the analysis by clicking on one of the displayed columns.

---

## Postgres Database

1. **Add a Connection:**
   - Go to “connections”.
   - Choose “PostgreSQL”.
   - Fill in all the values as desired and press “submit”.

2. **Choose a Table:**
   - Go to “Database Profiler”.
   - Select the appropriate table in “choose table to profile”.
   - If no table appears, the information entered in step 1 may be incorrect.

3. **Choose a Column:**
   - Click on one of the displayed columns to view your data.

## Notes:

- Ensure that you change the `SECRET_KEY` and `ENCRYPTION_KEY` before deploying the application to production.
- The default database configuration is set up for local testing. For production use, you may need to adjust the database settings to fit your own infrastructure.
