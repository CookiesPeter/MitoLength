import pandas as pd
import numpy as np
from scipy.signal import argrelextrema, find_peaks, filtfilt, peak_widths, butter
from matplotlib import pyplot as plt

#define local minima before peak
def detect_local_minima_before_peaks(signal, peak_indices):
    local_minima = []
    for peak_index in peak_indices:
        before_peak = signal[:peak_index]
        local_min_index = argrelextrema(before_peak,np.less)[0]
        if not local_min_index.any():
            continue
        print(local_min_index)
        local_min_index = local_min_index[-1]
        local_min_value = before_peak[local_min_index]
        local_minima.append((local_min_index, local_min_value))
    return local_minima

df=pd.read_csv('export.csv')

#Drop some useless labels
df.drop(index = df.index[0:3],axis=0,inplace=True)

#set index
df.set_index('TRACK_ID',inplace=True)
df.index = df.index.astype(int) 
df.FRAME= df.FRAME.astype(int)

#Search unique TRACK ID
for id in df.index.unique():
    newdf=df.loc[id,['FRAME','STD_INTENSITY_CH1']].sort_values(by='FRAME',ascending=True)
    x = newdf.STD_INTENSITY_CH1.values.astype(float)
    
    #Screen for tracks with length more than 50 frames
    if len(x) <50:
         continue
    
    #Smoothening the curve by filtfilt
    b, a = butter(8, 0.125,analog=False)
    yy= filtfilt(b,a,x)

    #find peaks
    threshold = float(np.max(yy))*0.75
    peaks,_ = find_peaks(yy,height=300,distance=60,prominence=10)

    #find peak widths
    width = peak_widths(yy,peaks,rel_height=0.8)

    #give up if no peaks identified
    if not peaks.size:
            continue
    
    #Find local maximum with smoothened curve
    local_minima = detect_local_minima_before_peaks(yy, peaks)

    #give up if total frame less than 30
    if np.max(newdf.FRAME.values)<30:
        continue

    #show graph
    x = x.astype(float)
    plt.plot(x) #curve
    for local_min in local_minima:
        index,values = local_min
        plt.plot(index,values,'x')
    plt.plot(peaks,yy[peaks],'o') #peak dots
    plt.plot(yy) #smooth
    plt.hlines(*width[1:], color="C2")
    plt.title('TRACK '+ str(id))
    plt.show()

    #printing it
    id=str(id)
    length=str(len(x))
    rep='TRACK_ID:'+ id + ' This cells divided for ' + str(len(peaks)) +' time(s).' +'\n' + 'The cell splits at frame(s): '
    with open('Results.txt', 'a') as f: 
        f.write(rep)
        for fr_peaks in peaks:
                fr_peaks = ' ' + str(fr_peaks)
                f.write(fr_peaks)
        f.write('\n')
    
    