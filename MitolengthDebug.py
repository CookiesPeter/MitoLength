import pandas as pd
import numpy as np
from scipy.signal import argrelextrema, find_peaks, filtfilt, butter, peak_prominences
from matplotlib import pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator
import csv
import czifile as cz
import xml.etree.ElementTree as ET
import tkinter.filedialog as tk
from sklearn.linear_model import LinearRegression




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
        local_minima.append(local_min_index)
    return local_minima

#get metadata from czi
xml_metadata = cz.CziFile("C:/Users/Ludwig.Qi/Desktop/POON Lab first analysis/Testing Single Sample/230414_LK_MH_PF_AcquisitionBlock3_pt3-Scene-26-P1-C05.czi").metadata()
root = ET.fromstring(xml_metadata)
for val in root.findall('.//Distance[@Id="X"]/Value'):
    pixel_size_in_meters=float(val.text)
    pixel_size_in_microns = float(pixel_size_in_meters)*1000000000

#data import and tidying
filepath=tk.askopenfilenames(title='Please select the csv file from TrackMate.',filetypes=(('Csv','*.csv'),('All files','*')))

df=pd.read_csv(filepath[0])

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
miss_count =0
normal=0
file = open('Results.csv','a',newline='')
writer=csv.writer(file)
head=['Index','TrackID','#splits','Algorithm Start','Algorithm End','Prominences','Adaptive Threshold']
writer.writerow(head)
file.close()

#add a cheat code
skip=int(input('Please indicate the track Id you wanna skip to:'))
normal_list=[]
falsep_list=[]
miss_list=[]
normal_rate_list=[]
r_list=[]
qnum_list=[]
promnum_list=[]
for qnum in range(0,101,20):
    
    for promnum in range(0,468,94):
        print("Quantile: ",qnum,"Prominence:",promnum)
        falsepositive=0
        miss_count =0
        normal=0
        qnum_list.append(qnum)
        promnum_list.append(promnum)
        Manual_Start_list=[]
        Manual_End_list=[]
        Algorithm_Start_list=[]
        Algorithm_End_list=[]

        
        #Search unique TRACK ID
        for id in df.index.unique():

            #skip code
            if id < skip:
                continue

            #obtain Frame, Std data, sort from a specific track ID
            newdf=df.loc[id,['FRAME','STD_INTENSITY_CH1']].sort_values(by='FRAME',ascending=True)
            dfm=pd.read_excel("C:\\Users\\Ludwig.Qi\\Desktop\\POON Lab first analysis\\Testing Single Sample\\Manual_Data_Collection..xlsx")
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
            b, a = butter(8, 0.125,analog=False)
            yy= filtfilt(b,a,x)
            #find peaks and threshold
            threshold = np.maximum(200,np.quantile(yy,qnum/100))
            peaks,_ = find_peaks(yy,height=threshold,distance=60,prominence=promnum)
            

            #give up if no peaks identified
            if not peaks.size:
                if manualdata["MS1"]!="None" and manualdata["MS2"]=="None":
                    miss_count=miss_count+1
                if manualdata["MS1"]!="None" and manualdata["MS2"]!="None":
                    miss_count=miss_count+2
                continue
            #give up if median is above mean
            #if np.median(yy) > np.mean(yy):
                #continue
            
            #Find local maximum with smoothened curve
            local_minima = detect_local_minima_before_peaks(x, peaks,np.quantile(x,0.85))
            prominences= peak_prominences(yy,peaks)[0]

            #for i,peakpair in enumerate(local_minima):
                #((index,values),peakss) = peakpair
                #file =open('Results.csv','a',newline='')
                #writer=csv.writer(file)
                #ind=ind+1
                #Append=[[str(ind),str(id),str(len(peaks)),str(index),str(peakss),str(prominences[i]),str(np.quantile(x,0.95))]]
                #writer.writerows(Append)
                #file.close()
            if not len(local_minima):
                continue
            
            for i,ipeak in enumerate(peaks):
                if min(local_minima)>ipeak:
                    peaks = np.delete(peaks,i)
            if manualdata["MS1"]=="None":
                falsepositive = falsepositive +len(peaks)
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
                    Manual_End_list.append(manualdata["ME1"])
                    Algorithm_End_list.append(real_peak)
                    Manual_Start_list.append(manualdata["MS1"])
                    Algorithm_Start_list.append(local_minima[index1])
                    falsepositive=falsepositive+len(peaks)-1
                    normal=normal+1
            if manualdata["MS1"]!="None" and manualdata["MS2"]!="None":
                if manualdata["ME2"]=="None":
                    continue
                if len(peaks)==0:
                    miss_count=miss_count+2
                if len(peaks)==1:
                    miss_count=miss_count+1
                    if abs(peaks[0]- manualdata["ME1"])<=abs(peaks[0]-manualdata["ME2"]):
                        Manual_End_list.append(manualdata["ME1"])
                        Algorithm_End_list.append(peaks[0])
                        Manual_Start_list.append(manualdata["MS1"])
                        Algorithm_Start_list.append(local_minima[0])
                    if abs(peaks[0]- manualdata["ME1"])>abs(peaks[0]-manualdata["ME2"]):
                        Manual_End_list.append(manualdata["ME2"])
                        Algorithm_End_list.append(peaks[0])
                        Manual_Start_list.append(manualdata["MS2"])
                        Algorithm_Start_list.append(local_minima[0])
                    normal=normal+1
                if len(peaks)>1:
                    differ = abs(peaks[0]-manualdata["ME1"])
                    real_peak=peaks[0]
                    index2=0
                    for j in range(len(peaks)):
                        if abs(peaks[j]-manualdata["ME1"])<differ:
                            differ=abs(peaks[j]-manualdata["ME1"])
                            real_peak=peaks[j]
                            index2=j
                    Manual_End_list.append(manualdata["ME1"])
                    Algorithm_End_list.append(real_peak)
                    Manual_Start_list.append(manualdata["MS1"])
                    Algorithm_Start_list.append(local_minima[index2])
                    differ = abs(peaks[0]-manualdata["ME2"])
                    real_peak=peaks[0]
                    index3=0
                    for j in range(len(peaks)):
                        if abs(peaks[j]-manualdata["ME2"])<differ:
                            differ=abs(peaks[j]-manualdata["ME2"])
                            real_peak=peaks[j]
                            index3=j
                    Manual_End_list.append(manualdata["ME2"])
                    Algorithm_End_list.append(real_peak)
                    Manual_Start_list.append(manualdata["MS2"])
                    Algorithm_Start_list.append(local_minima[j])
                    falsepositive=falsepositive+len(peaks)-2
                    normal=normal+2
            
            
        All_start_list_manual=Manual_Start_list
        All_end_list_manual=Manual_End_list
        All_start_list_alg=Algorithm_Start_list
        All_end_list_alg=Algorithm_End_list
        



        data_start =pd.DataFrame({'manual_start':All_start_list_manual,'Algo_start':All_start_list_alg})
        data_manual_start=np.array(data_start['manual_start']).reshape((-1,1))
        data_algo_start=np.array(data_start['Algo_start'])
        regr_start=LinearRegression()
        regr_start.fit(data_manual_start,data_algo_start)
        data_end=pd.DataFrame({'manual_end':All_end_list_manual,'Algo_end':All_end_list_alg})
        data_manual_end=np.array(data_end['manual_end']).reshape((-1,1))
        data_algo_end=np.array(data_end['Algo_end'])
        regr_end=LinearRegression()
        regr_end.fit(data_manual_end,data_algo_end)
        r_square=regr_end.score(data_manual_end,data_algo_end)*0.5+regr_start.score(data_manual_start,data_algo_start)*0.5
        normal_rate=float(normal)/(normal+falsepositive+miss_count)

        r_list.append(r_square)
        normal_rate_list.append(normal_rate)
        normal_list.append(normal)
        falsep_list.append(falsepositive)
        miss_list.append(miss_count)

all_data={"Quantile":qnum_list,"Prominance":promnum_list,"R_Square":r_list,"Normal_rate":normal_rate_list,
          "Normal":normal_list,"Falsepos":falsep_list,"Missing":miss_list}
all_df=pd.DataFrame(all_data)
all_df.to_csv("data.csv")
#plotting
fig = plt.figure()
ax = fig.add_subplot(projection='3d')

# Make data.
X = qnum_list
Y = promnum_list
Z= r_list

# Plot the surface.
surf = ax.scatter(X, Y, Z,c=Z)
plt.title('Rsquare mapping')
ax.set_xlabel('Quantile')
ax.set_ylabel('Prominence')
ax.set_zlabel('R Square')

plt.show()

#plotting
fig = plt.figure()
ax = fig.add_subplot(projection='3d')

# Make data.
X = qnum_list
Y = promnum_list
Z= normal_rate_list
# Plot the surface.
surf = ax.scatter(X, Y, Z,c=Z)
plt.title('Normal Proportion')
ax.set_xlabel('Quantile')
ax.set_ylabel('Prominence')
ax.set_zlabel('Normal Proportion')


plt.show()


