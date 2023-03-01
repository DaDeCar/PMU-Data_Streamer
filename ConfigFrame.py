# -*- coding: utf-8 -*-
"""
Created on Fri Feb 18 12:53:17 2022

@author: ldominguez
"""

from datetime import datetime
import math
import crc_ccitt


class configFrame:
    def __init__(self):
        
        # 1-Config frame2 V1
        self.sync ='AA31'
        # 2-tamaño del frame 
        self.framesize = '0000'
        # 3-id del PMU (x def: 3001)
        self.idcode = '0BB9'
        # 4-unix time del momento
        self.soc = '00000000'
        # 5-flag+fracsec del soc 
        self.fracsec = '00000000'
        # 6-resolucion del fracsec (x def: 1e6 microseg)
        self.time_base= '000F4240'
        # 7-num de PMUs incluidos en frame
        self.num_pmu='0001'
        # 8-nombre de la estacion (x def: "stationA")
        self.stn='73746174696F6E204120202020202020'
        # 9- no olvidar que aca se repite "idcode"
        self.idcode2='0BB9'
        # 10- formato de la medicion (rect/polar y float/int16)
        self.format='000F'
        # 11- numero de fasores (x def: 3)
        self.phnmr='0003'
        # 12- Numero de valores analogicos (x def: 0)
        self.annmr='0000'
        # 13- Numero de palabras digitales (x def: 0)
        self.dgnmr='0000'
        # 14- nombre de fasores y canales en ASCII (3 canales en 16 bytes)
        self.chnam='564120202020202020202020202020205642202020202020202020202020202056432020202020202020202020202020'
        # 15- factor de conversion x cada canal (solo usar para formato int16, no para floating)
        self.phunit='000000000000000000000000'
        # 16- factor de conversion x cada canal analogico (solo usar para formato int16, no para floating)
        # OJO porque aca el PMU CT toma 5º bit para definir si es 50 hz o 60 hz
        # no esta usando el campo 18, sino éste.
        self.anunit='00011111'
        # 17- factor de conversion x cada digital (solo usar para formato int16, no para floating)
        self.digunit='00000000'
        # 18- frecuencia nominal (0: 60 hz / 1: 50hz)
        self.fnom='0001'
        # 19- Se incrementa cada vez que cambia la configuracion del PMU (x def: 0)
        self.cfgcnt='0000'
        # 20- tasa de transmision de fasores (x def: 10/sec)
        self.data_rate='000F'
        # 21- chequeo con redundancias CRC-CCITT
        self.chk='0000'
           
    
    def create(self):
        
        # obtenemos timestamp (unix) de tiempo utc
        ts = datetime.utcnow().timestamp()
        # separamos parte entera y decimal del timestamp
        parte_dec, parte_ent = math.modf(ts)
        # parte entera va al soc, primero convertimos a hexadecimal
        # decimal a hex sin el "0x"
        parte_ent2hex=hex(int(parte_ent))
        soc_hexlist=parte_ent2hex.split('x')
        self.soc=soc_hexlist[1]
        
        # generacion del crc
        # armamos palabra completa en formato hexa, sin el crc 
        hex_frame=(self.sync+self.framesize+self.idcode+ self.soc+ self.fracsec +
                self.time_base + self.num_pmu+ self.stn+self.idcode2+self.format+
                self.phnmr+ self.annmr+ self.dgnmr+self.chnam+self.phunit+
                self.anunit+self.digunit+self.fnom+self.cfgcnt+self.data_rate)
        # Calculamos longitud del frame (se le suma long=2 debido al crc que se 
        # añadira luego)
        lon_frame=int(2+(len(hex_frame)/2))
        lon_hex_frame=hex(lon_frame)
        lon_sep=lon_hex_frame.split(sep='x')
        self.framesize='00'+lon_sep[1]
        hex_frame=(self.sync+self.framesize+self.idcode+ self.soc+ self.fracsec +
                self.time_base + self.num_pmu+ self.stn+self.idcode2+self.format+
                self.phnmr+ self.annmr+ self.dgnmr+self.chnam+self.phunit+
                self.anunit+self.digunit+self.fnom+self.cfgcnt+self.data_rate)
        
        #CHECKSUM
        #creamos la funcion crc16
        crc16=crc_ccitt.init_crc16()
        #obtenemos codigo crc
        hex_checksum=crc_ccitt.crc_ittt16(hex_frame,crc16)
        #incorporamos codigo crc como atributo al objeto configFrame
        crc_hex=hex_checksum.split(sep='x')
        self.chk=crc_hex[1]
        hex_frame+=self.chk
        byte_frame=bytes.fromhex(hex_frame)
             
        return byte_frame
      
        
#%%
# config_frame=configFrame()
# paquete2,checksum2=config_frame.create()