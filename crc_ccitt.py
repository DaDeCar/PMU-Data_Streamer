# -*- coding: utf-8 -*-
"""
Created on Mon Jan 10 17:09:12 2022

@author: ldominguez
"""
import crcmod



def init_crc16():
    '''
    Function factory that returns a new function for calculating CRCs using 
    a specified CRC algorithm.
    Parameters:	
    
        poly – The generator polynomial to use in calculating the CRC. The value is specified as a Python 
            integer or long integer. The bits in this integer are the coefficients of the polynomial. 
            The only polynomials allowed are those that generate 8, 16, 24, 32, or 64 bit CRCs.
        initCrc – Initial value used to start the CRC calculation. 
        rev – A flag that selects a bit reversed algorithm when True. Defaults to True because the 
            bit reversed algorithms are more efficient.
        xorOut – Final value to XOR with the calculated CRC value. Used by some CRC algorithms. 
            Defaults to zero.
    
    Returns:	
    CRC calculation function
    Return type:	
    
    function
    
    The function that is returned is as follows:
    
    .crc_function(data[, crc=initCrc])
    
    Parameters:	
    
        data (byte string) – Data for which to calculate the CRC.
        crc – Initial CRC value.
    
    Returns:	
        
    Calculated CRC value.
    Return type:integer
    '''
    
    crc16 = crcmod.mkCrcFun(0x11021, rev=False, initCrc=0xFFFF, xorOut=0x0000)
    
    return crc16

def crc_ittt16(hex_complete,crc16):
    '''
    Toma una palabra hexadecimal y entrega la codificacion CRC 16 bits, en un integer.
    
    Hay que ingresar tambien la funcion "crc16". Ver funcion "init_crc16()"
    
    El ciclo for va tomando de a dos bytes (16 bits) de la palabra hexa original,
    lo transforma en decimal y arma una lista "dec" que una vez completa, será 
    codificada una sola vez, obteniendose el codigo crc.
    '''
    
    i=0
    #se inicializan listas "s" y "dec"
    s=[]
    dec=[]
    for j in hex_complete:
        s.append(j)
        i+=1
        #si la lista "s" ya cargó dos bytes, se pasa a la lista auxiliar "hex_word"
        #la cual luego es convertida a decimal, y luego anexada a la lista "dec"
        #
        if i%2==0:
            hex_word=s[i-2]+s[i-1]
            i=0
            s.clear()
            #a traves del comando "int (hex_word,16") se convierte a decimal de 16 bits
            dec.append(int(hex_word,16))
    
    return (hex(crc16(bytearray((dec)))))


#%%
#prueba
hex_complete='73746174696F6E2041'
crc16=init_crc16()
crc=crc_ittt16(hex_complete,crc16)


#%%
#ejemplos de ingreso de datos

   # #ingresando en ASCII
   # print(hex (crc16(b'123456')))
   # out:0x2EF4
   # #ingresando en decimal
   # print(hex(crc16(bytearray((49, 50, 51, 52,53,54)))))
   # out:0x2EF4
   
   
   # #ingresando en ASCII
   # print(hex (crc16(b'station A')))
   # out:0x8b3f
   # #ingresando en decimal
   # print(hex(crc16(bytearray((115,116,97, 116, 105 ,111, 110, 32, 65)))))
   # out:0x8b3f