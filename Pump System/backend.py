# @COPYRIGHT ADAM RADEK MARTINEZ 2022
# CONTACT: adam.radek.martinez@gmail.com 

import pandas as pd
import numpy as np
import ipywidgets as widgets
from ipywidgets import interact, interactive, fixed, interact_manual
from IPython.display import display
import os
import sys
import serial
import math
import time

######################## PORT ########################
PORT = '/dev/cu.usbserial-AU04OXNK'
######################################################

####################################################################################
####################################################################################
# ----- CREATE COMMAND FUNCTIONS ----- # 
####################################################################################
####################################################################################


def hex2complement(number, ty = 4):
    if ty == 4:
        hexadecimal_result = format(number, "03X")
        return hexadecimal_result.zfill(4)
    elif ty == 2: 
        hexadecimal_result = format(number, "02X")
        return hexadecimal_result.zfill(1)

def XOR(command):
    a = command[1:]
    curr = int(a[0], 16)
    for i in range(1, len(a)):
        curr = curr ^ int(a[i], 16)
    return hex2complement(curr, 2)

def modifier(command): 
    for i in range(1, len(command)): 
        if command[i] == 'E8':
            command.insert(i+1, '00')
        if command[i] == 'E9': 
            command[i] = 'E8'
            command.insert(i+1, '01')
    return command

def get_RS(speed , pump = None, direct = None):
    
    # converting information to appropriate hexidecimal
    hex_speed = hex2complement(int(speed*10)) # is a string
    hex_pump = hex2complement(int(pump), 2) # is a string
    
    hex_direct = None # is a string 
    if direct == False: hex_direct = hex2complement(1,2)
    else: hex_direct = hex2complement(0, 2)
    
    # constructing the command
    command = ['E9', hex_pump, '06', '57', '4A', hex_speed[0:2], hex_speed[2:4], '01', hex_direct]
    new_command = modifier(command)
    xor = XOR(new_command)
    new_command.insert(len(new_command), xor)
    
    # converting the list to hexidecimals that can be outputted 
    final = bytes(int(x, base=16) for x in new_command)
    
    return final

####################################################################################
####################################################################################
# ----- GUI COMMANDS ----- # 
####################################################################################
####################################################################################

w_1 = widgets.FloatSlider(
    value=80,
    min=0,
    max=150.0,
    step=0.1,
    description='Set speed:',
    disabled=False,
    continuous_update=False,
    orientation='horizontal',
    readout=True,
    readout_format='.1f',
)
w_2 = widgets.Text(
    value='1',
    placeholder='Type something',
    description='Pump:',
    disabled=False
)

button_run = widgets.Button(description="Run!")
button_stop = widgets.Button(description="Stop!")
output = widgets.Output()

def on_button_clicked_run(b):
    with output:
        output.clear_output()
        print("Pump running")
        
        ser = serial.Serial(
            port= PORT,
            baudrate=9600,
            parity=serial.PARITY_EVEN,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS
        )
        
        ser.isOpen()
        
        out = get_RS(w_1.value , w_2.value, w_3.value)
        ser.write(out)
        
        ser.close()
        
def on_button_clicked_stop(b):
    with output:
        output.clear_output()
        print("Pump stopped")
        ser = serial.Serial(
            port= PORT,
            baudrate=9600,
            parity=serial.PARITY_EVEN,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS
        )
        
        ser.isOpen()
        ser.write(b'\xE9\x01\x06\x57\x4A\x01\xF4\x00\x00\xEF')
        ser.close()

w_3 = widgets.Checkbox(
    value=False,
    description='Counterwise direction',
    disabled=False
)
