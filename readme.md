# Profiler Insight

With the growth of data storage and creation it is increasingly important to know which data is stored where.
In addition to this, quick checks on data quality or overall data composition can give you an advantaged when creating your data.
This is why the Profiler Insight tool is made. It aims to help the user with data profiling. 
Current functionality is limited to postgres databases and csv files but I aim to extend this to other kind of databases.
The installation guide is defined below:

# Getting Started

If you want to use Profiler Insight you have to go to the folowing steps:

1. ### Install Docker

2. ### install Docker Compose

3. ### Download the docker-compose file from the github page:

Download the Docker Compose file from  [link](https://github.com/SanderBos1/Time_series_analyser/blob/main/docker-compose.yml)
Save it in your created directory


4. ### Start the Docker Containers:

Execute the following command in the created directory to start the Docker containers:
docker compose -f docker-compose.yml up --detach

