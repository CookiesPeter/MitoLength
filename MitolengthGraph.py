import pandas as pd
import numpy as np
from scipy.signal import argrelextrema, find_peaks, filtfilt, butter
from matplotlib import pyplot as plt
import czifile as cz
import xml.etree.ElementTree as ET
import csv

#define local minima before peak
def detect_local_minima_before_peaks(signal, peak_indices):
    local_minima = []
    for peak_index in peak_indices:
        before_peak = signal[:peak_index]
        local_min_index = argrelextrema(before_peak,np.less)[0]
        if not local_min_index.any():
            continue
        local_min_index = local_min_index[-1]
        local_minima.append(local_min_index)
    return local_minima

def detect_deltay_neighbourpeak(yy):
    deltay = []
    peak=[]
    #calculate derivative
    dydx = np.gradient(yy)
    dydx = dydx/max(dydx)
    butterdydx=butter_lowpass_filtfilt(dydx,order=10,fre=0.15)
    #findwheremeetszero
    dydxpeaks = list(find_peaks(butterdydx,prominence=0.8)[0])
    idx = np.argwhere(np.diff(np.sign(butterdydx - 0))).flatten()
    for dydxpeak in dydxpeaks:
        before_peak = [bp for bp in idx if bp < dydxpeak]
        lowbound = before_peak[-1]
        after_peak = [bp for bp in idx if bp > dydxpeak]
        try:
            upbound = after_peak[1]
            peak.append(after_peak[0])
        except:
            continue
        deltay.append((lowbound,upbound))
        deltalist = [(bound[0],yy[bound[1]]-yy[bound[0]]) for bound in deltay]
        apoplist = [apop[0] for apop in deltalist if apop[1] > 0.2]
    return apoplist,deltay,peak,butterdydx,dydxpeaks

#define butter_lowpass_filtfilt
def butter_lowpass_filtfilt(data,fre,order=8):
    b,a = butter(order,fre,"lowpass",analog=False)
    output = filtfilt(b,a,data,axis=0)
    return output

#import files
czi = "/Users/peterfu/Desktop/MitoLength/Optimization Results/MitosisOptimization/Optimization#1/raw data and manual counted/Test data.czi"
export = "/Users/peterfu/Desktop/MitoLength/Optimization Results/MitosisOptimization/Optimization#1/export.csv"
xml_metadata = cz.CziFile(czi).metadata()
df=pd.read_csv(export,low_memory=False)

#append/start a csv file, set initial indices, add a header
ind=0
file = open('Results.csv','a',newline='')
writer=csv.writer(file)
head=['Index','TrackID','v1_#splits','v1 Start','v1 End','v2 start','v2 midpoint','v2 end']
writer.writerow(head)
file.close()

#get metadata from czi
root = ET.fromstring(xml_metadata)
for val in root.findall('.//Distance[@Id="X"]/Value'):
    pixel_size_in_meters=float(val.text)
    pixel_size_in_microns = float(pixel_size_in_meters)*1000000000

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
df.drop(df[df.POSITION_X < 10].index,axis=0,inplace=True)
df.drop(df[df.POSITION_X > bound].index,axis=0,inplace=True)
df.drop(df[df.POSITION_Y < 10].index,axis=0,inplace=True)
df.drop(df[df.POSITION_Y > bound].index,axis=0,inplace=True)

#Search unique TRACK ID
for id in df.index.unique():

    #obtain Frame, Std data, sort from a specific track ID
    newdf=df.loc[id,['FRAME','STD_INTENSITY_CH1']].sort_values(by='FRAME',ascending=True)
    x = newdf.STD_INTENSITY_CH1.values.astype(float)
    

    #Screen for tracks with length more than 50 frames
    if len(x) <50:
        continue
    
    #Smoothening the curve by filtfilt
    yy=butter_lowpass_filtfilt(x,fre=0.1)
    yy=yy/max(yy)
    x=x/max(x)
    
    #find peaks and threshold
    peaks = list(find_peaks(yy,distance=60,prominence=0.4)[0])
    
    #give up if no peaks identified
    if not peaks:
        continue

    #Find local maximum with smoothened curve
    local_minima = detect_local_minima_before_peaks(yy, peaks)

    #getbounds
    try:
        apoplist,bounds,peakk,butterdydx,dydxpeaks = detect_deltay_neighbourpeak(yy)
    except:
        continue

    #plotgraph
    #plt.plot(x,label="raw",color="blue")
    plt.plot(yy,label="filtfilt",color="green")
    plt.plot(local_minima,yy[local_minima],marker='x',label='v1_start')
    plt.plot(peaks,yy[peaks],marker='o',label='v1_peak')
    #plt.plot(dydx,label='dydx',color='grey')
    plt.plot(butterdydx,label='smooth dydx',color='red')
    plt.plot(dydxpeaks,butterdydx[dydxpeaks],'*',label='v2_peaks')
    plt.plot(apoplist,np.zeros(len(apoplist)),marker='P',label='apoptosis',markersize=20)
    plt.plot(peakk,butterdydx[peakk],marker='D',label='v2_midpoint')
    for bound in bounds:
        plt.plot(bound[0],0,marker='^',label='v2_start',markersize=10)

        plt.plot(bound[1],0,marker='v',label='v2_upbound',markersize=10)
    plt.axhline()
    plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
    plt.tight_layout()
    plt.savefig("Track: "+str(id))
    plt.close()
