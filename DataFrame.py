# -*- coding: utf-8 -*-
"""
Created on Fri Feb 18 16:38:45 2022

@author: ldominguez
"""

import math
import crc_ccitt
import utils
import numpy as np
import angles


class DataFrame:
    def __init__(self):
        
        # 1-Config frame2 V1
        self.sync ='AA01'
        # 2-tamaño del frame 
        self.framesize = '0000'
        # 3-id del PMU (x def: 3001)
        self.idcode = '0BB9'
        # 4-unix time del momento
        self.soc = '00000000'
        # 5-flag+fracsec del soc 
        self.fracsec = '00000000'
        # 6-Continuation index for fragmented frames
        self.stat= '0000'
        
        # 7-V1
        self.mag1= '426F7125'
        # 8-PHA1
        self.pha1='3FFF8BA9'
        # 9-MAG2
        self.mag2= '426F9A77'
        # 10-PHA2
        self.pha2='BDC61CE3'
        # 11-MAG3
        self.mag3= '426F7208'
        # 12-PHA3
        self.pha3='C00C311D'
        # 13- FREQ
        self.freq='4248065C'
        # 14- ROCOF 
        self.rocof='3DB10795'
        
        # 15- chequeo con redundancias CRC-CCITT
        self.chk='0000'
        # Aqui se guarda el Hexstring final, antes de convertir a bytes.
        self.hexstring=None
           
    
    def create(self, timestamp, amp1, amp2, amp3,phase1, phase2,phase3,frequency,rocof):
        '''
        Parameters
        ----------
        Recibe los valores de 1 sincrofasor de la funcion "create_1s_df"
        y arma un paquete de datos con ese sincrofasor.
        
        Returns
        -------
        byte_frame : frame listo para enviar por UDP en Type=Bytes
        '''
        
        #Carga de los valores del sincrofasor
        #AMPLITUDE
        mag1=utils.float_to_hex(amp1)
        mag1_sep=mag1.split(sep='x')
        self.mag1=mag1_sep[1]
        
        mag2=utils.float_to_hex(amp2)
        mag2_sep=mag2.split(sep='x')
        self.mag2=mag2_sep[1]
        
        mag3=utils.float_to_hex(amp3)
        mag3_sep=mag3.split(sep='x')
        self.mag3=mag3_sep[1]
        
        #PHASE
        #Hay que normalizar el angulo para que se encuentre entre -pi y pi
        phase1n=angles.normalize(phase1, lower=-180, upper=180, b=False)
        #De grados a radianes
        phase1r=np.deg2rad(phase1n)
        #transformamos float a hexa string
        Pha1=utils.float_to_hex(phase1r)
        #Le sacamos el '0x'
        Pha1_sep=Pha1.split(sep='x')
        #nos quedamos con el hexstring sin el '0x'
        self.pha1=Pha1_sep[1]
        
        phase2n=angles.normalize(phase2, lower=-180, upper=180, b=False)
        phase2r=np.deg2rad(phase2n)
        Pha2=utils.float_to_hex(phase2r)
        Pha2_sep=Pha2.split(sep='x')
        self.pha2=Pha2_sep[1]
        
        phase3n=angles.normalize(phase3, lower=-180, upper=180, b=False)
        phase3r=np.deg2rad(phase3n)
        Pha3=utils.float_to_hex(phase3r)
        Pha3_sep=Pha3.split(sep='x')
        self.pha3=Pha3_sep[1]
        
        #FREQ
        freq=utils.float_to_hex(frequency)
        freq_sep=freq.split(sep='x')
        self.freq=freq_sep[1]
        
        #dFREQ/dt(ROCOF)
        rcf=utils.float_to_hex(rocof)
        rcf_sep=rcf.split(sep='x')
        if rcf_sep[1]=='0':
            self.rocof='00000000'
        else:
            self.rocof=rcf_sep[1]
     
        
        # TIMESTAMP (unix) - Hay que armar SOC + FRACSEC
        # SOC
        # separamos parte entera y decimal del timestamp
        parte_dec, parte_ent = math.modf(timestamp)
        # parte entera va al soc, primero convertimos a hexadecimal
        parte_ent2hex=hex(int(parte_ent))
        # decimal a hex sin el "0x"
        soc_hexlist=parte_ent2hex.split('x')
        # Se actualiza el campo del objeto
        self.soc=soc_hexlist[1]
        
        # FRACSEC
        fracs=round(parte_dec*1e6)
        parte_dec2hex=hex(int(fracs))
        fracsec_hexlist=parte_dec2hex.split('x')
        #Aca hay que distinguir el fracsec=0 (el inicial) ya que sino
        #arma un paquete con menos bits del requerido. Hay que asegurar 4 bytes
        if fracsec_hexlist[1]=='0':
            self.fracsec='00000000'
        else:
            self.fracsec='000'+fracsec_hexlist[1]
         
        #armamos palabra completa en formato hexa, sin el crc 
        hex_frame=(self.sync+self.framesize+self.idcode+ self.soc+ self.fracsec +
                   self.stat + self.mag1+self.pha1+ self.mag2+
                   self.pha2+self.mag3+self.pha3+
                   self.freq+ self.rocof)
        
        #Calculamos longitud del frame (se le suma long=2 debido al crc que se añadira luego)
        lon_frame=int(2+(len(hex_frame)/2))
        lon_hex_frame=hex(lon_frame)
        lon_sep=lon_hex_frame.split(sep='x')
        self.framesize='00'+lon_sep[1]
        hex_frame=(self.sync+self.framesize+self.idcode+ self.soc+ self.fracsec +
                   self.stat + self.mag1+self.pha1+ self.mag2+
                   self.pha2+self.mag3+self.pha3+
                   self.freq+ self.rocof)
        
        #CHECKSUM
        #creamos la funcion crc16
        crc16=crc_ccitt.init_crc16()
        #obtenemos codigo crc
        hex_checksum=crc_ccitt.crc_ittt16(hex_frame,crc16)
        # decimal a hex sin el "0x"
        crc_hex=hex_checksum.split(sep='x')
        self.chk=crc_hex[1]
        #incorporamos codigo crc como atributo al objeto DataFrame
        hex_frame+=self.chk
        byte_frame=bytes.fromhex(hex_frame)
        self.hexstring=hex_frame
        
        return byte_frame
       

    def create_1s_df(self,signal,j):
        '''
        La funcion toma una señal electrica de 3 canales y una tasa de reporte 
        por segundo de sincrofasores, y recurriendo a la funcion "create" arma
        los dataframes para enviar por udp, ya listos.
        
        Parameters
        ----------
        signal :señal de 3 canales con la que se armaran los sincrofasores
        j : tasa de paquetes por segundo (fps) con el que se reportan los sincrofasores.

        Returns
        -------
        df : data frame codificado en bytes listo para ser enviado por UDP.

        '''
        
        temp_reg=signal.dataset_pmu.loc[j]['TimeStamp':'dFreq/dt']
        df=self.create(temp_reg['TimeStamp'],temp_reg['V1'],temp_reg['V2'],temp_reg['V3'],temp_reg['Phase1'],temp_reg['Phase2'],temp_reg['Phase3'], temp_reg['Freq'],temp_reg['dFreq/dt'])
       
        return df
        
       
        
#%%
# data_frame=DataFrame()
# frequency=50
# amplitude=(140,120,120) 
# phase=(0.01,120,240)
# # Ruido aleatorio
# freq_noise=(0.2,0.2,0.2) 
# amp_noise=(3,3,3)
# phase_noise=(1,1,1)
# # paquetes por segundo
# frames_p_sec=10
# # Creacion de la señal
# signal = sinewave.ThreePhaseSineWave(frequency, amplitude, phase, freq_noise,
#                             amp_noise, phase_noise, frames_p_sec)
# j=0
# paquete2=data_frame.create_1s_df(signal, j)

        # #actualizamos longitud del frame
        # long_frame=len(hexa+self.chk)
        # #long_final=long_frame.split(sep='x')
        # self.framesize='00'+crc_final[1]