# -*- coding: utf-8 -*-
"""
Created on Tue Dec 14 13:20:44 2021

@author: ldominguez
"""

import socket
import pandas as pd

def udp_send(UDP_IP = "127.0.0.1",UDP_PORT = 5005,MESSAGE = b"Hello, World!"):

      
    print("UDP target IP: %s" % UDP_IP)
    print("UDP target port: %s" % UDP_PORT)
    print("message: %s" % MESSAGE)
    
    # Crea el objeto socket
    sock = socket.socket(socket.AF_INET, # Internet
                          socket.SOCK_DGRAM) # UDP
    
    sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
    
    sock.close()
    
    

def udp_receive(UDP_IP = "127.0.0.1",UDP_PORT = 5005):
    
    list_messages=[]
    headers = ['TimeStamp', 'Flag', 'Phase1', 'V1', 'Phase2', 'V2', 'Phase3', 
               'V3', 'Freq', 'dFreq/dt', 'SOC']
    dataset_pmu = pd.DataFrame(columns=headers)
    
    # Crea el objeto socket
    sock = socket.socket(socket.AF_INET, # Internet
                           socket.SOCK_DGRAM) # UDP
    # Le asignamos direccion al socket, que consiste en IP+PORT (Este proceso 
    # se llama "binding")
    sock.bind((UDP_IP, UDP_PORT))
    
    while True:
        data, addr = sock.recvfrom(2048) # buffer size is 1024 bytes
        print("received message: %s" % data)
        list_messages.append(data)
         
    return list_messages

# %%

# Usar dos consolas, una para recibir y una para enviar
list_ts=udp_receive(UDP_IP = "127.0.0.1",UDP_PORT = 5005)
udp_send(UDP_IP = "127.0.0.1",UDP_PORT = 5005,MESSAGE = b"Hello, World!")
print(data)
