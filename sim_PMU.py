# -*- coding: utf-8 -*-
"""
Created on Fri Feb 18 13:29:12 2022

@author: ldominguez
"""

import socket
import ConfigFrame, DataFrame
import time
import sinewave
import signal
from utils import transmision_handler


if __name__ == '__main__':
    
    #UDP
    # Inicializacion
    UDP_IP = "127.0.0.1"
    UDP_des_PORT = 4713
    UDP_source_PORT=49174
    # Crea el objeto socket
    sock = socket.socket(socket.AF_INET, # Internet
                           socket.SOCK_DGRAM) # UDP
    # Para finalizar transmision por consola o teclado
    signal.signal(signal.SIGINT, transmision_handler)
    
    #CONFIGURATION FRAME
    #Creacion de Configuration Frame
    cf=ConfigFrame.configFrame()
    try:
        cf_message=cf.create()
    #Si se produce algun error en la creacion del CF, vuelve a intentar
    except (ValueError):
        cf_message=cf.create()
    
    print("UDP target IP: %s" % UDP_IP)
    print("UDP target port: %s" % UDP_des_PORT)
    
    # Envio del Configuration Frame
    sock.sendto(cf_message, (UDP_IP, UDP_des_PORT))
    print("Configuration Frame Enviado")
    time.sleep(1)
    
    #DATA FRAME
    #Creacion de Data Frame
    df=DataFrame.DataFrame()
    #Carga de parametros de los sincrofasores
    frequency=50
    amplitude=(140,120,100) 
    phase=(120,0.01,240)
    # Ruido aleatorio
    freq_noise=(0.2,0.2,0.2) 
    amp_noise=(3,3,3)
    phase_noise=(5,5,5)
    # paquetes por segundo
    fps=10
    #Latencia para el envio de los sincrofasores
    if fps==30:
        ts=(1/fps)*0.8
    if fps==50:
        ts=(1/fps)*0.65
    else:
        ts=1/fps
        
        
    print("Enviando DataFrames")
    while True:
        #Envio de paquetes
        for index in range (fps):
            try:
                # Creacion de los señal de tres canales
                signal = sinewave.ThreePhaseSineWave(frequency, amplitude, phase, freq_noise,
                                                     amp_noise, phase_noise, fps)
                #Creacion de los sincrofasores, a partir de la señal de tres canales
                df_message=df.create_1s_df(signal,index)
                # Envio de los sincrofasores
                sock.sendto(df_message, (UDP_IP, UDP_des_PORT))
                time.sleep(ts)
            
            except(ValueError):
                continue
           
           

    

