# Profiler Insight

In today’s data-driven world, understanding the exact location and quality of your stored data is essential. 
Profiler Insight is designed to give you a competitive edge by providing detailed assessments of data quality and composition through its profiling capabilities.

Currently, Profiler Insight supports CSV files. 
I am  actively working on expanding its compatibility to include a broader range of files & database types in the future.

## Getting Started

To get up and running with Profiler Insight, follow these steps:

1. **Install Docker**

   - **Windows**: Download Docker Desktop from the [Docker website](https://docs.docker.com/desktop/windows/install/).

2. **Install Docker Compose**

   - **Windows/Mac**: Docker Desktop includes Docker Compose. Simply download and install Docker Desktop from the [Docker website](https://docs.docker.com/desktop/).

3. **Download the Docker Compose File**

   - Obtain the Docker Compose file from our [GitHub page](https://github.com/SanderBos1/profilerInsight/blob/main/installation/docker-compose.yml) and save it to your desired directory.

4. **Start the Docker Containers**

   - Navigate to the directory where you saved the Docker Compose file and run the following command to start the containers:
     ```bash
     docker compose -f docker-compose.yml up --detach
     ```

With these steps, you will have Profiler Insight up and running, ready to help you gain valuable insights into your data.
