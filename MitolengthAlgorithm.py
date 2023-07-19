import pandas as pd
import numpy as np
from scipy.signal import argrelextrema, find_peaks, filtfilt, butter, peak_prominences
from matplotlib import pyplot as plt
from sklearn.linear_model import LinearRegression
import csv
import czifile as cz
import xml.etree.ElementTree as ET

#define local minima before peak
def detect_local_minima_before_peaks(signal, peak_indices,htres):
    local_minima = []
    for peak_index in peak_indices:
        before_peak = signal[:peak_index]
        before_peak = before_peak[before_peak < htres]
        local_min_index = argrelextrema(before_peak,np.less)[0]
        if not local_min_index.any():
            continue
        local_min_index = local_min_index[-1]
        local_min_value = before_peak[local_min_index]
        local_minima.append(((local_min_index, local_min_value),peak_index))
    return local_minima

#get metadata from czi
xml_metadata = cz.CziFile('raw data and manual counted/Test data.czi').metadata()
root = ET.fromstring(xml_metadata)
for val in root.findall('.//Distance[@Id="X"]/Value'):
    pixel_size_in_meters=float(val.text)
    pixel_size_in_microns = float(pixel_size_in_meters)*1000000000

#data import and tidying
df=pd.read_csv('export.csv')

#Drop some useless labels
df.drop(index = df.index[0:3],axis=0,inplace=True)

#set index
df.set_index('TRACK_ID',inplace=True)
df.index = df.index.astype(int) 
df.FRAME= df.FRAME.astype(int)
df.POSITION_X = df.POSITION_X.astype(float)
df.POSITION_Y = df.POSITION_Y.astype(float)

#set bound
bound = pixel_size_in_microns-10
df = df.drop(df[(df.POSITION_X < 10) & (df.POSITION_X > bound)].index)
df = df.drop(df[(df.POSITION_Y < 10) & (df.POSITION_Y > bound)].index)

#append/start a csv file, set initial indices, add a header
ind=0
falsepositive=0
miss_count = 0
file = open('Results.csv','a',newline='')
writer=csv.writer(file)
head=['Index','TrackID','#splits','Algorithm Start','Algorithm End']
writer.writerow(head)
file.close()

#add a cheat code
skip=int(input('Please indicate the track Id you wanna skip to:'))

#Search unique TRACK ID
for id in df.index.unique():

    #skip code
    if id < skip:
        continue

    #obtain Frame, Std data, sort from a specific track ID
    newdf=df.loc[id,['FRAME','STD_INTENSITY_CH1']].sort_values(by='FRAME',ascending=True)
    x = newdf.STD_INTENSITY_CH1.values.astype(float)

    #Screen for tracks with length more than 50 frames
    if len(x) <50:
         continue
    
    #Smoothening the curve by filtfilt
    b, a = butter(8, 0.125,analog=False)
    yy= filtfilt(b,a,x)

    #find peaks and threshold
    threshold = np.maximum(200,np.quantile(yy,0.85))
    peaks,_ = find_peaks(yy,height=threshold,distance=60,prominence=100)

    #give up if no peaks identified
    if not peaks.size:
            continue
    #give up if median is above mean
    #if np.median(yy) > np.mean(yy):
        #continue
    
    #Find local maximum with smoothened curve
    local_minima = detect_local_minima_before_peaks(x, peaks,np.quantile(x,0.95))'
    
    for peakpair in local_minima:
        ((index,values),peakss) = peakpair
        file =open('Results.csv','a',newline='')
        writer=csv.writer(file)
        ind=ind+1
        Append=[[str(ind),str(id),str(len(peaks)),str(index),str(peakss)]]
        writer.writerows(Append)
        file.close()

    #add curve
    plt.plot(x,label='Raw Curve')
    plt.plot(yy,label='Smoothened Curve')

    #add algorithm dots
    plt.plot(index,values,'x',label='Algorithm start',color='green')
    plt.plot(peaks,yy[peaks],'o',label='Algorithm end',color='red') 
    #plt.axhline(y=threshold, color='r', linestyle='-')
    #plt.axhline(y=np.mean(yy), color='b', linestyle='-')
    #plt.axhline(y=np.quantile(yy,0.5),color='g',linestyle = '-')
    #prominences= peak_prominences(yy,peaks)[0]
    #contour_heights = yy[peaks] - prominences
    #plt.vlines(x=peaks, ymin=contour_heights, ymax=yy[peaks])

    #preliminarily show plot
    plt.title('TRACK '+ str(id))
    plt.legend()
    plt.savefig('Track ID '+str(id))
    plt.close()
    print('Track'+str(id))
    
