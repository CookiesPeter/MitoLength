import pandas as pd
import numpy as np
from scipy.signal import argrelextrema, find_peaks, filtfilt, butter
from matplotlib import pyplot as plt
import czifile as cz
import xml.etree.ElementTree as ET
import tkinter.filedialog as tk
from sklearn.linear_model import LinearRegression
import time

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

#define butter_lowpass_filtfilt
def butter_lowpass_filtfilt(data,fre,order=10):
    b,a = butter(order,fre,'lowpass', analog=False)
    output = filtfilt(b,a,data,axis=0)
    return output

#plot 3d
def plot3d(X,Y,Z,Title):
    #plotting
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    # Plot the surface
    ax.scatter(X, Y, Z,c=Z)
    plt.title(Title)
    ax.set_xlabel('Cutoff Frequency')
    ax.set_ylabel('Prominence')
    ax.set_zlabel(Title)
    plt.savefig(Title)
    plt.show()

#get metadata from czi
xml_metadata = cz.CziFile("/Users/peterfu/Desktop/MitoLength/Optimization Results/Optimization#3(distance=120)/raw data/RN221213abc-Scene(64).czi").metadata()
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

#set bound
bound = pixel_size_in_microns-10
'''df.drop(df[df.POSITION_X < 10].index,axis=0,inplace=True)
df.drop(df[df.POSITION_X > bound].index,axis=0,inplace=True)
df.drop(df[df.POSITION_Y < 10].index,axis=0,inplace=True)
df.drop(df[df.POSITION_Y > bound].index,axis=0,inplace=True)'''

#set initial indices
ind=0
falsepositive=0
miss_count =0
normal=0
normal_list=[]
falsep_list=[]
miss_list=[]
normal_rate_list=[]
r_list=[]
freq_list=[]
promnum_list=[]
idlist=[]

for freq in range(5,10,1):
    for promnum in range(0,501,25):
        print("cutoff freq: ",freq/10,"Prominence:",promnum)
        falsepositive=0
        miss_count =0
        normal=0
        freq_list.append(freq/10)
        promnum_list.append(promnum)
        All_start_list_manual=[]
        All_end_list_manual=[]
        All_start_list_alg=[]
        All_end_list_alg=[]

        #Search unique TRACK ID
        for id in df.index.unique():

            #obtain Frame, Std data, sort from a specific track ID
            newdf=df.loc[id,['FRAME','STD_INTENSITY_CH1']].sort_values(by='FRAME',ascending=True)
            dfm=pd.read_excel("/Users/peterfu/Desktop/MitoLength/Optimization Results/Optimization#3(distance=120)/Manual_Data_Collection.xlsx")
            manualdata=dfm.loc[id]
            x = newdf.STD_INTENSITY_CH1.values.astype(float)

            #Screen for tracks with length more than 50 frames
            if len(x) <50:
                if manualdata["MS1"]!="None" and manualdata["MS2"]=="None":
                    miss_count=miss_count+1
                if manualdata["MS1"]!="None" and manualdata["MS2"]!="None":
                    miss_count=miss_count+2
                continue
            
            #Smoothening the curve by filtfilt
            yy=butter_lowpass_filtfilt(x,fre=freq/10)
            #find peaks and threshold
            peaks,_ = find_peaks(yy,distance=120,prominence=promnum)
            peaks = list(idd + min(newdf['FRAME']) for idd in peaks)
            
            #give up if no peaks identified
            if not peaks:
                if manualdata["MS1"]!="None" and manualdata["MS2"]=="None":
                    miss_count=miss_count+1
                if manualdata["MS1"]!="None" and manualdata["MS2"]!="None":
                    miss_count=miss_count+2
                continue

            #Find local maximum with smoothened curve
            local_minima = detect_local_minima_before_peaks(x, peaks)

            if not len(local_minima):
                continue
            
            for i,ipeak in enumerate(peaks):
                if min(local_minima)>ipeak:
                    peaks = np.delete(peaks,i)
            #manual None
            if manualdata["MS1"]=="None":
                falsepositive = falsepositive +len(peaks)

            #Manual One
            if manualdata["MS1"]!="None" and manualdata["MS2"]=="None":
                if manualdata["ME1"]=="None":
                    continue
                if len(peaks)==0:
                    miss_count=miss_count+1
                else:
                    differ = abs(peaks[0]-manualdata["ME1"])
                    real_peak=peaks[0]
                    index1=0
                    for i in range(len(peaks)):
                        if abs(peaks[i]-manualdata["ME1"])<differ:
                            differ=abs(peaks[i]-manualdata["ME1"])
                            real_peak=peaks[i]
                            index1=i
                    All_end_list_manual.append(manualdata["ME1"])
                    All_end_list_alg.append(real_peak)
                    All_start_list_manual.append(manualdata["MS1"])
                    All_start_list_alg.append(local_minima[index1])
                    falsepositive=falsepositive+len(peaks)-1
                    normal=normal+1
                    idlist += [id]
            
            #Manual TWO
            if manualdata["MS1"]!="None" and manualdata["MS2"]!="None":
                if manualdata["ME2"]=="None":
                    continue
                if len(peaks)==0:
                    miss_count=miss_count+2
                if len(peaks)==1:
                    miss_count=miss_count+1
                    if abs(peaks[0]- manualdata["ME1"])<=abs(peaks[0]-manualdata["ME2"]):
                        All_end_list_manual.append(manualdata["ME1"])
                        All_end_list_alg.append(peaks[0])
                        All_start_list_manual.append(manualdata["MS1"])
                        All_start_list_alg.append(local_minima[0])
                    if abs(peaks[0]- manualdata["ME1"])>abs(peaks[0]-manualdata["ME2"]):
                        All_end_list_manual.append(manualdata["ME2"])
                        All_end_list_alg.append(peaks[0])
                        All_start_list_manual.append(manualdata["MS2"])
                        All_start_list_alg.append(local_minima[0])
                    normal=normal+1
                    idlist += [id]
                if len(peaks)>1:
                    differ = abs(peaks[0]-manualdata["ME1"])
                    real_peak=peaks[0]
                    index2=0
                    for j in range(len(peaks)):
                        if abs(peaks[j]-manualdata["ME1"])<differ:
                            differ=abs(peaks[j]-manualdata["ME1"])
                            real_peak=peaks[j]
                            index2=j
                    All_end_list_manual.append(manualdata["ME1"])
                    All_end_list_alg.append(real_peak)
                    All_start_list_manual.append(manualdata["MS1"])
                    All_start_list_alg.append(local_minima[index2])
                    differ = abs(peaks[0]-manualdata["ME2"])
                    real_peak=peaks[0]
                    index3=0
                    for j in range(len(peaks)):
                        if abs(peaks[j]-manualdata["ME2"])<differ:
                            differ=abs(peaks[j]-manualdata["ME2"])
                            real_peak=peaks[j]
                            index3=j
                    All_end_list_manual.append(manualdata["ME2"])
                    All_end_list_alg.append(real_peak)
                    All_start_list_manual.append(manualdata["MS2"])
                    All_start_list_alg.append(local_minima[j])
                    falsepositive=falsepositive+len(peaks)-2
                    normal=normal+2
                    idlist += 2 * [id]
                
        #give it a break
        #time.sleep(1)
        
        data_start =pd.DataFrame({'manual_start':All_start_list_manual,'Algo_start':All_start_list_alg})
        data_manual_start=np.array(data_start['manual_start'])
        data_algo_start=np.array(data_start['Algo_start']).reshape((-1,1))
        regr_start=LinearRegression()
        regr_start.fit(data_algo_start,data_manual_start)
        data_end=pd.DataFrame({'manual_end':All_end_list_manual,'Algo_end':All_end_list_alg})
        data_manual_end=np.array(data_end['manual_end'])
        data_algo_end=np.array(data_end['Algo_end']).reshape((-1,1))
        regr_end=LinearRegression()
        regr_end.fit(data_algo_end,data_manual_end)
        r_square=regr_end.score(data_algo_end,data_manual_end)*1+regr_start.score(data_algo_start,data_manual_start)*0
        normal_rate=float(normal)/(normal+falsepositive+miss_count)
        print("R square: "+str(r_square)+" Normal Rate: "+str(normal_rate)+"\nTracked normal cell#: "+str(normal))
        print(falsepositive)
        r_list.append(r_square)
        normal_rate_list.append(normal_rate)
        normal_list.append(normal)
        falsep_list.append(falsepositive)
        miss_list.append(miss_count)

all_data={"Cutoff Frequency":freq_list,"Prominance":promnum_list,"R_Square":r_list,"Normal_rate":normal_rate_list,
          "Normal":normal_list,"Falsepos":falsep_list,"Missing":miss_list}
all_df=pd.DataFrame(all_data)
all_df.to_csv("data.csv")

#Rsquare
plot3d(freq_list,promnum_list,r_list,"R square")

#NormalRate
plot3d(freq_list,promnum_list,normal_rate_list,"Normal Rate")

#CellNumber
plot3d(freq_list,promnum_list,normal_list,"Cell Number")