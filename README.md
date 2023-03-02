# Project: PMU Data Streamer

### Overview

Built a full project (back – frontend) that simulates physical electrical equipment called “PMU” - Phasor Measurement Units. 

This project consists of a PMU simulator written in python that generated random synchrophasors (measurements of current and voltage with a GPS tag) according to the IEEE C37.118.2 standard and streamed it to an IP address using UDP protocol. 

This work was designed to test servers that receive big data of electrical measurements. The project had a web interface for users, available to configure all the parameters. 

The project meant an improvement for the customers (server’s owner) because they no longer depended on physical equipment that generates the labeled measurements. 


### Program workflow:

1. The user enters the website and configures the requirements for the synchrophasor (amplitude, phase, frequency, frames per second), and configures an IP address in which he/she will receive the simulated data. 

2. The python program generates simulated synchrophasor introducing amplitude, phase, and frequency noise, and generating a timestamp for each of them.

3. The program sends via UDP the Configuration Frame (CF) to the destination server and then starts to send the Data Frames (DF).


### Testing

The PMU Data Streamer was tested using PMU Connection Tester (https://github.com/GridProtectionAlliance/PMUConnectionTester) as a receiving server.


## Screenshots

    
### Main page of the project:
    
  ![](https://github.com/DaDeCar/PMU-Data_Streamer/blob/74bb5a05e0f81c459a29f1781ee5f544423ced3d/images/web%20home.jpg)
    
    
### Configuration Form with all signal parameters:
    
  ![](https://github.com/DaDeCar/PMU-Data_Streamer/blob/74bb5a05e0f81c459a29f1781ee5f544423ced3d/images/web%20streamer.jpg)
  
### Screenshot of the Configuration frame:
     Hexa data frame which configurates PMU COnnection Tester program 
    
  ![](https://github.com/DaDeCar/PMU-Data_Streamer/blob/74bb5a05e0f81c459a29f1781ee5f544423ced3d/images/CF.jpg)  
  
### Screenshot of the Data frame:
    Hexa data frame sended 10-50 or 100 times/s which simulates the digitalized synchrophasor 
    
  ![](https://github.com/DaDeCar/PMU-Data_Streamer/blob/74bb5a05e0f81c459a29f1781ee5f544423ced3d/images/DF.jpg)  
    
    
    
    
    
    
    
