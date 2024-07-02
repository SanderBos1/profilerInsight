# Profiler Insight

In today's data-intensive environments, knowing the exact locations and quality of stored data is crucial. 
Quick assessments of data quality and composition provide a competitive edge in data management. 
This is where the Profiler Insight tool excels—it offers powerful data profiling capabilities.

Currently, Profiler Insight supports PostgreSQL databases and CSV files, with plans to expand compatibility to other database types in the future.

## Getting Started

To begin using Profiler Insight, follow these steps:

1. **Install Docker**

    - **Windows**: Download Docker Desktop from [Docker website](https://docs.docker.com/desktop/windows/install/).

2. **Install Docker Compose**

    - **Windows/Mac**: Docker Desktop includes Docker Compose. Install Docker Desktop from the [Docker website](https://docs.docker.com/desktop/).

3. **Download the Docker Compose file** from the [GitHub page](https://github.com/SanderBos1/profilerInsight/blob/main/installation/docker-compose.yml). Save it to your preferred directory.

4. **Start the Docker Containers:**

   Navigate to the directory where you saved the Docker Compose file and execute the following command:
   ```bash
   docker compose -f docker-compose.yml up --detach