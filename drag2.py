# -*- coding: utf-8 -*-
"""
        MSP Drag Calculations 
        Author: Raoul Mazumdar
        RMIT University
        May 2020
               
"""
import numpy as np
import matplotlib.pyplot as plt


import pandas as pd
df=pd.read_csv('hotmodel.csv', sep=',',header=None)
roex = np.flip( df.values[:,0] )
altx = np.flip(df.values[:,1] )


key = ['-','--',':','-.']


#A_list  = [0.1,12]
Cdx =  [1.0,2.0,2.2,5]
alt_list = [200,300,400,500]

Cd  = 2.67  # Drag Coefficient
A   = 0.15  # Area Normal to Flight (M**2)
roe = 1e-12 # Drag at altitude
alt = 400  # Km - starting altitude
GM  = 3.986005e14 # GM constant, units m^3 / s^2
m   = 10 # Mass of satellite in kg



check = []
for ii in range(len(Cdx)):
    alt = alt_list[ii]
    ri = 6378.14*1000 + alt*1000.0
    vi = np.sqrt(GM/ri)
    pi = np.sqrt( 4*(np.pi**2)*(ri**3) / GM)
    Time = 0.0
    t0   = []
    h0   = []
    v0   = []
    Cd = Cdx[ii]
    Cd = 2.2
    #A  = A_list[ii]
    for i in range(500000):
        #
        hi = (ri - 6378.14*1000) / 1000
        roe = np.interp(hi,altx,roex) 
        #
        dr = (-2 * np.pi * Cd * A * roe * (ri**2)) / m
        dp = -6 * (np.pi**2) * Cd * A * roe * (ri**2) / (m*vi)
        dv = np.pi * Cd * A * roe * ri * vi / m
        #
        ri += dr
        vi += dv
        pi += dp
        if ri < (6378.14*1000 + 10*1000):
            break 
        Time += pi 
        v0  .append(   vi/1000     )
        h0  .append( (ri - 6378.14*1000) / 1000)
        t0  .append( Time/(86400) )
        print(i)    
        #print('Alt:',ri,'Vel:',vi,'Period:',pi)
    plt.plot(t0,h0, linestyle = key[ii] ,label='%s'%(alt), color ='k')
    check.append(h0)
    
plt.ylabel('Altitude [km]')
plt.xlabel('Time [X]')
plt.legend()
plt.show()    
