import pandas as pd
import numpy as np
from scipy.signal import argrelextrema, find_peaks, filtfilt, peak_widths, butter
from matplotlib import pyplot as plt
import csv

#define local minima before peak
def detect_local_minima_before_peaks(signal, peak_indices):
    local_minima = []
    for peak_index in peak_indices:
        before_peak = signal[:peak_index]
        local_min_index = argrelextrema(before_peak,np.less)[0]
        if not local_min_index.any():
            continue
        #print(local_min_index)
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

#open a csv file
file=open('Results.csv','a',newline='')
writer=csv.writer(file)
head=['Index','TrackID','#splits','Start','end','manualstart','manualend']
ind=1
writer.writerow(head)
file.close()

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

    '''find peak widths
    width = peak_widths(yy,peaks,rel_height=0.8)'''

    #give up if no peaks identified
    if not peaks.size:
            continue
    
    #Find local maximum with smoothened curve
    local_minima = detect_local_minima_before_peaks(x, peaks)

    #give up if total frame less than 30
    if np.max(newdf.FRAME.values)<30:
        continue

    #getting user input for counting
    start=input("the TrackID is " + str(id) + ". Please input the starting point you count.")
    while not start.isdigit():
        start = input("Error. Please input an INTEGER: ")
    else:
         start=int(start)
    end=input("the TrackID is " + str(id) + ". What is the end point?")
    while not end.isdigit():
        end = input("Error. Please input an INTEGER: ")
    else:
        end=int(end)

    #show graph
    x = x.astype(float)
    fig, ax =plt.subplots() #curve
    ax.set_xlabel('Frames')
    ax.set_ylabel('Signal Standard deviation')
    ax.set_title('SD trend of Track: '+str(id))
    plt.plot(x,label='Raw Curve')
    plt.plot(yy,label='Smoothened Curve') #smooth
    for local_min in local_minima:
        index,values = local_min
        plt.plot(index,values,'x',label='Mitosis Start')
    plt.plot(peaks,yy[peaks],'o',label='Peak') #peak dots
    #plt.hlines(*width[1:], color="C2")
    plt.title('TRACK '+ str(id))
    plt.plot(start,x[start],'s',label='Manual Start')
    plt.plot(end,x[end],'^',label='Manual end')
    ax.legend()
    plt.savefig('Track ID '+str(id))
    plt.show()
    #printing it
    #id=str(id)
    #length=str(len(x))
    
    for fr_peaks in peaks:
        file=open('Results.csv','a',newline='')
        writer=csv.writer(file)
        Append=[[str(ind),str(id),str(len(peaks)),str(index),str(fr_peaks),str(start),str(end)]]
        ind=ind+1
        writer.writerows(Append)
    file.close()
    
    '''with open('Results.txt', 'a') as f: 
        for fr_peaks in peaks:
                fr_peaks = str(fr_peaks)
                Report= 'TRACK_ID:'+ str(id) + ' This cells divided for ' + str(len(peaks)) +' time(s).\n' + 'The division happens from Frame ' + str(index) +', and splits at Frame ' + fr_peaks +'.'
                Manual= 'Manual counted starts from Frame '+str(start)+', ends at Frame '+str(end)+'.'
                f.write(Report)
                f.write('\n')
                f.write(Manual)
        f.write('\n')'''


    