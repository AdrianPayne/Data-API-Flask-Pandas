# playbrush
## Description
From two .csv files (the first file contains offline brushing data of all participants in a
toothbrushing study while the second one allocates the participants into groups), the tasks
is to extract information for each participant (identified by their PlaybrushID) and provide meaningful
information that can be communicated to the user via a newsletter.

## WEB APP
### AWS url
http://3.17.77.92:32768/

### Local deploy
>docker-compose build && docker-compose up 

url: localhost:5000

### Web documentation
Only one resource 
>'/'

#### Method GET
Form with two csv file inputs:
+ rawdata
+ groups

Post submit button

#### Method POST
Print user and group week statistical data tables

### Design considerations
As web app requirements are simple and short, these tools has been used:
+ Back: Flask
+ Front: Jinja2 templates (provided by Flask)
+ Docker to encapsulate and install the requirements
+ GitHub actions to automate deployment in AWS ECR/ECS services (EC2 instance). Deployed with each new release!

### Next steps
+ CSS style
+ Plot figures
+ Test suit!!!!!

## DATA TASKS
#### Example of input & output
    -INPUT-
    RAWDATA
    PlaybrushID,TimestampUTC,UpTime,DownTime,LeftTime,RightTime,NoneTime,
    PB2500017115,Mon Sep 18 2017 08:03:18 GMT+0100 (BST),6.6,0.1,0.3,0.3,5.7,
    PB2500017115,Mon Sep 18 2017 08:06:32 GMT+0100 (BST),0,3.8,1.8,0,1.4,
    ...
    
    GROUPDATA
    group,PBID
    D,PB2500036964
    D,PB2500036963
    ...
    
    -OUTPUT-
    # Task 1 - User Information
    group, PBID, mon, tue, wed, thu, fri, sat, sun, total-brushes, twice-brushes, avg-brush-time
    
    # Task 2 - Group Dynamics
    group, total-brushes, avg-brushes, avg-brush-time, score-performance

### Results
    Task 1
    group,PBID,mon,tue,wed,thu,fri,sat,sun,total-brushes,twice-brushes,avg-brush-time
    A,PB2500008778,0,0,1,1,0,0,1,3,0,37.05
    A,PB2500009123,0,1,1,1,1,1,1,6,0,50.88
    A,PB2500009543,0,0,1,1,0,1,0,3,0,44.67
    A,PB2500010644,0,0,1,1,1,0,1,4,0,55.75
    A,PB2500013900,1,0,0,0,0,0,0,1,0,35.10
    A,PB2500014533,1,0,0,0,0,0,0,1,0,45.20
    A,PB2500015032,0,2,2,0,0,0,0,4,2,33.32
    A,PB2500015176,0,0,0,0,0,2,1,3,1,21.39
    A,PB2500016085,0,0,0,0,1,0,0,1,0,28.70
    A,PB2500016302,0,0,0,1,2,1,2,6,2,48.16
    A,PB2500016413,0,1,0,0,0,1,1,3,0,83.37
    A,PB2500017260,1,1,0,0,0,0,0,2,1,60.10
    A,PB2500029113,0,2,1,0,1,0,0,4,1,25.87
    A,PB2500029403,1,0,0,0,0,0,0,1,0,24.00
    A,PB2500029467,0,0,0,0,1,2,0,3,1,31.31
    A,PB2500029535,0,0,0,0,0,0,1,1,0,35.00
    A,PB2500030275,0,0,0,0,0,0,1,1,0,43.05
    A,PB2500034769,0,0,0,2,0,0,0,2,2,53.50
    A,PB2500034873,1,0,2,1,1,0,1,6,1,83.46
    A,PB2500035145,0,1,1,0,1,1,2,6,1,83.53
    A,PB2500036593,0,0,0,0,0,0,1,1,0,30.05
    B,PB2500008735,0,0,0,0,1,0,0,1,0,35.05
    B,PB2500008867,0,0,0,1,0,1,0,2,1,27.02
    B,PB2500009228,0,0,0,2,0,0,0,2,2,38.62
    B,PB2500009352,0,0,0,0,0,1,0,1,0,94.05
    B,PB2500009374,0,0,1,1,1,1,0,4,0,32.27
    B,PB2500009705,0,0,0,0,0,1,1,2,1,59.03
    B,PB2500009814,1,0,0,0,0,0,0,1,0,22.00
    B,PB2500010542,0,0,0,0,1,1,1,3,0,100.77
    B,PB2500010629,0,0,0,0,2,1,2,5,2,81.66
    B,PB2500014851,0,0,1,0,0,0,0,1,0,28.05
    B,PB2500017115,1,1,0,1,1,0,0,4,0,64.35
    B,PB2500029003,0,0,0,1,0,0,0,1,0,45.05
    B,PB2500029118,0,1,2,2,2,2,2,11,5,79.42
    B,PB2500029572,0,0,0,0,1,0,1,2,1,30.52
    B,PB2500029755,0,0,0,0,1,0,0,1,0,64.05
    B,PB2500034402,0,0,0,0,0,0,1,1,0,24.00
    B,PB2500035239,1,2,1,1,0,0,1,6,1,122.92
    B,PB2500035308,0,0,0,1,1,1,0,3,0,36.72
    B,PB2500035330,0,0,0,0,0,1,0,1,0,20.95
    B,PB2500035411,0,0,0,1,2,1,1,5,1,60.34
    B,PB2500036585,0,0,0,0,1,1,0,2,1,28.52
    B,PB2500036671,0,0,0,1,0,1,0,2,1,71.95
    C,PB2500008196,0,0,0,1,1,2,1,5,1,55.38
    C,PB2500008248,0,0,0,2,2,2,2,8,4,56.02
    C,PB2500008549,0,1,2,1,1,1,2,8,2,44.53
    C,PB2500008951,2,2,1,2,2,1,2,12,5,59.80
    C,PB2500008956,0,0,0,1,2,1,2,6,2,108.62
    C,PB2500009101,0,2,2,2,1,1,1,9,3,67.06
    C,PB2500009201,0,1,2,2,2,2,2,11,5,128.25
    C,PB2500009375,0,0,0,0,0,2,2,4,2,77.49
    C,PB2500010328,0,0,2,2,1,1,1,7,2,39.66
    C,PB2500010630,0,1,0,2,1,2,0,6,2,38.60
    C,PB2500014415,0,0,0,1,1,1,0,3,0,52.02
    C,PB2500014442,0,0,0,2,1,1,2,6,2,73.16
    C,PB2500014740,0,0,0,2,2,2,2,8,4,95.82
    C,PB2500016077,0,2,0,0,1,2,0,5,2,27.53
    C,PB2500016479,0,0,0,1,1,0,1,3,0,48.35
    C,PB2500029848,0,0,0,0,1,2,2,5,2,88.74
    C,PB2500034762,0,0,0,0,0,2,2,4,2,113.04
    C,PB2500034890,0,0,0,1,2,2,2,7,3,52.03
    C,PB2500034972,0,1,2,2,2,2,1,10,4,122.95
    C,PB2500035170,0,1,2,2,1,1,2,9,3,77.76
    C,PB2500036366,0,0,0,0,0,0,1,1,0,89.00
    C,PB2500036703,0,0,0,1,2,2,2,7,3,55.78
    C,PB2500036788,2,2,2,2,2,1,2,13,6,88.24
    D,PB2500008565,1,2,2,1,2,2,1,11,4,78.99
    D,PB2500009146,0,2,2,2,2,0,0,8,4,130.01
    D,PB2500009220,0,0,0,1,1,0,0,2,1,42.05
    D,PB2500009446,0,0,0,0,1,2,2,5,2,114.91
    D,PB2500009709,0,0,0,2,1,2,2,7,3,73.78
    D,PB2500010636,0,0,0,1,0,0,0,1,0,24.05
    D,PB2500014435,0,1,2,0,0,2,2,7,3,33.16
    D,PB2500014494,0,2,2,2,2,1,2,11,5,83.89
    D,PB2500014596,0,0,0,0,1,1,1,3,0,48.02
    D,PB2500014762,0,0,0,0,1,2,1,4,1,137.70
    D,PB2500016490,0,2,0,1,1,1,1,6,1,56.82
    D,PB2500017485,0,0,0,0,1,2,2,5,2,73.93
    D,PB2500029001,0,0,0,1,1,2,2,6,2,52.42
    D,PB2500029510,2,0,1,0,0,0,0,3,1,26.75
    D,PB2500029526,0,0,0,0,1,2,1,4,1,86.71
    D,PB2500030280,0,1,2,0,2,2,1,8,3,52.90
    D,PB2500034756,0,0,0,0,0,1,2,3,1,133.88
    D,PB2500034872,1,1,2,1,1,2,1,9,2,64.79
    D,PB2500035119,0,0,1,1,1,0,2,5,1,56.94
    D,PB2500035317,0,0,0,2,2,1,1,6,2,83.39
    D,PB2500035373,1,2,2,2,2,2,2,13,6,49.35
    D,PB2500035479,0,0,0,2,1,2,1,6,2,64.34
    D,PB2500036660,0,1,2,2,2,2,2,11,5,103.23
    D,PB2500036764,0,0,0,0,1,0,0,1,0,64.05
    D,PB2500036963,0,2,1,2,2,1,1,9,3,25.69
    D,PB2500036964,0,0,0,0,2,2,2,6,3,119.88

---

    Task 2
    group,total-brushes,avg-brush-time,avg-brushes,score-performance
    C,157,72.17,6.83,492.61
    D,160,72.37,6.15,445.35
    B,61,53.06,2.77,147.12
    A,62,45.40,2.95,134.05


### Execute in local
+ Create a virtual environment 
    > python3 -m venv /path/to/new/virtual/env
+ Install project dependencies 
    >pip install -r playbrush_api/requirements.txt
+ Execute task.py
    >python3 data_tasks.py

### Design considerations
+ Python 3.7.7
+ Use of Pandas and Numpy libraries because include cleaning, transforming, manipulating and analyzing data 
efficient methods
+ Use of FP (avoiding POO) to make the code easier to read (jupyter notebook style) and not affecting performance
+  For question:
    >Which group performed the best?
    + The option that does not penalize for the number of members within each group has been selected, the result of multiplying the brushing averages and time per brushing per user
