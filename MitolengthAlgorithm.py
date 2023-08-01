import pandas as pd
import numpy as np
from scipy.signal import argrelextrema, find_peaks, filtfilt, butter
from matplotlib import pyplot as plt
import csv
import czifile as cz
import xml.etree.ElementTree as ET
import tkinter.filedialog as tk

#define local minima before peak
def detect_local_minima_before_peaks(signal, peak_indices):
    local_minima = []
    for peak_index in peak_indices:
        before_peak = signal[:peak_index]
        local_min_index = argrelextrema(before_peak,np.less)[0]
        if not local_min_index.any():
            continue
        local_min_index = local_min_index[-1]
        local_minima_pair = (local_min_index,peak_index)
        local_minima.append(local_minima_pair)
    return local_minima

#define butter_lowpass_filtfilt
def butter_lowpass_filtfilt(data,fre,order=10):
    b,a = butter(order,fre,'lowpass', analog=False)
    output = filtfilt(b,a,data,axis=0)
    return output

#get metadata from czi
xml_metadata = cz.CziFile('/Users/peterfu/Desktop/MitoLength/Optimization Results/Optimization#3/raw data/RN221213abc-Scene(64).czi').metadata()
root = ET.fromstring(xml_metadata)
for val in root.findall('.//Distance[@Id="X"]/Value'):
    pixel_size_in_meters=float(val.text)
    pixel_size_in_microns = float(pixel_size_in_meters)*1000000000

#data import and tidying
filepath=tk.askopenfilenames(title='Please select the csv file from TrackMate.',filetypes=(('Csv','*.csv'),('All files','*')))
df=pd.read_csv(filepath[0],low_memory=False)

#Drop some useless labels
df.drop(index = df.index[0:3],axis=0,inplace=True)

#set index
df.set_index('TRACK_ID',inplace=True)
df.index = df.index.astype(int) 
df.FRAME= df.FRAME.astype(int)
df.POSITION_X = df.POSITION_X.astype(float)
df.POSITION_Y = df.POSITION_Y.astype(float)

#append/start a csv file, set initial indices, add a header
ind=0
file = open('Results.csv','a',newline='')
writer=csv.writer(file)
head=['Index','TrackID','#splits','Mitotic Start','Mitotic End']
writer.writerow(head)
file.close()

#Search unique TRACK ID
for id in df.index.unique():

    #obtain Frame, Std data, sort from a specific track ID
    newdf=df.loc[id,['FRAME','STD_INTENSITY_CH1']].sort_values(by='FRAME',ascending=True)
    x = newdf.STD_INTENSITY_CH1.values.astype(float)

    #Screen for tracks with length more than 50 frames
    if len(x) <50:
         continue
    
    #Smoothening the curve by filtfilt
    yy=butter_lowpass_filtfilt(x,fre=0.5)
    #find peaks and threshold
    peaks,_ = find_peaks(yy,distance=120,prominence=(2.0478*np.std(x)-68.183))
    peaks = list(idd + min(newdf['FRAME']) for idd in peaks)
    
    #give up if no peaks identified
    if not peaks:
            continue

    #Find local maximum with smoothened curve
    local_minima = detect_local_minima_before_peaks(x, peaks)
    for (start,peakss) in local_minima:
        #Excel output
        file =open('Results.csv','a',newline='')
        writer=csv.writer(file)
        ind=ind+1
        Append=[[str(ind),str(id),str(len(peaks)),str(start),str(peakss)]]
        writer.writerows(Append)
        file.close()