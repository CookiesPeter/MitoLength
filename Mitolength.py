import pandas as pd
import numpy as np
from scipy.signal import argrelextrema, find_peaks, filtfilt, butter, peak_prominences
from matplotlib import pyplot as plt
from sklearn.linear_model import LinearRegression
import csv
import czifile as cz
import xml.etree.ElementTree as ET

'hello'
#Create list for data
Manual_Start_list=[]
Manual_End_list=[]
Algorithm_Start_list=[]
Algorithm_End_list=[]
Falsepos_Start_list=[]
Falsepos_End_list=[]
Missed_Start_list=[]
Missed_End_list=[]

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
        print(local_min_index,local_min_value)
        local_minima.append((local_min_index, local_min_value))
    return local_minima
#define digit error
def checkdigit(ans):
    while not ans.isdigit():
            ans = input("Error. Please input an INTEGER: ")
    else:
        ans=int(ans)
        return ans
#define yn error
def checkyn(yn):
    while yn != 'y' and yn != 'n':
        yn = input('Programming monkeys are unhappy. Small single letter of y or n.')
    else:
        return yn

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
file=open('Results.csv','a',newline='')
writer=csv.writer(file)
head=['Index','TrackID','#splits','Algorithm Start','Algorithm End','Manual Start','Manual End','false+?','accumulated false+ count','missed peak start','missed peak end','accumulated missed count']
writer.writerow(head)
file.close()

#add a cheat code
skip=int(input('Please indicate the track Id you wanna skip to:'))

#Search unique TRACK ID
for id in df.index.unique():

    #reset
    manualstart = None
    manualend = None

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
    local_minima = detect_local_minima_before_peaks(x, peaks,np.quantile(x,0.95))
    #Record Algorithm Starting Points and Ending Points
    if len(peaks)!=len(local_minima):
        #for i in range(len(peaks)):
            #Algorithm_End_list.append(peaks[i])
            #Algorithm_Start_list.append(local_minima[i][0])
    
        continue

    #getting user input for counting
    for local_min,i in local_minima,range(len(peaks)):
        index,values = local_min

        #add curve
        plt.plot(x,label='Raw Curve')
        plt.plot(yy,label='Smoothened Curve')

        #add algorithm dots
        plt.plot(index,values,'x',label='Algorithm start',color='green')
        plt.plot(peaks,yy[peaks],'o',label='Algorithm end',color='red') 
        #plt.axhline(y=threshold, color='r', linestyle='-')
        #plt.axhline(y=np.mean(yy), color='b', linestyle='-')
        #plt.axhline(y=np.quantile(yy,0.5),color='g',linestyle = '-')
        prominences= peak_prominences(yy,peaks)[0]
        contour_heights = yy[peaks] - prominences
        plt.vlines(x=peaks, ymin=contour_heights, ymax=yy[peaks])

        #preliminarily show plot
        plt.title('TRACK '+ str(id))
        plt.show(block=False)
        
        #ask for user input
        skip=False
        prescence=input('Do you see a peak near to computer? Please type y or n.\n')
        prescence=checkyn(prescence)
        if prescence == 'y':   
            manualstart=input("the TrackID is " + str(id) + ". Please input the manual starting point.\n")
            manualstart = checkdigit(manualstart)
            manualend=input("the TrackID is " + str(id) + ". What is the manual end point?\n")
            manualend = checkdigit(manualend)

            #add to regression list
            Algorithm_End_list.append(peaks[i])
            Algorithm_Start_list.append(local_minima[i][0])
            Manual_Start_list.append(manualstart)
            Manual_End_list.append(manualend)
        elif prescence == 'n':
            falsepositive = falsepositive + 1
            Falsepos_Start_list.append(index)
            Falsepos_End_list.append(peaks)
            skip = True
            plt.close()
            continue

    #skip showing plot if false positive
    if skip is True:
        print('Sad but next.')
        plt.close()
        continue

    #show entire track
    while True:
        fig, ax =plt.subplots() #curve

        #set label
        ax.set_xlabel('Frames')
        ax.set_ylabel('Signal Standard deviation')
        ax.set_title('SD trend of Track: '+str(id))

        #plot curve
        plt.plot(x,label='Raw Curve')
        plt.plot(yy,label='Smoothened Curve')

        #plot dots, including false positive ones
        for local_min in local_minima:
            index,values = local_min
            plt.plot(index,values,'x',label='Algorithm start',color='green')
            plt.plot(peaks,yy[peaks],'o',label='Algorithm end',color='red')

        #add vertical lines indicating the manual start and end
            plt.axvline(manualstart,linestyle='--',label='Manual Start',color='lightgreen')
            plt.axvline(manualend,linestyle='--',label='Manual end',color='lightcoral')

        #show plot
        ax.legend()
        plt.show(block=False)

        #check if there is missed
        miss=input('Any peak missing?Input y or n.\n')
        miss=checkyn(miss)
        miss_start=None
        miss_end=None
        if miss == 'y':
            miss_count = miss_count+1
            miss_start=input("the TrackID is " + str(id) + ". Please input the missing starting point.\n")
            miss_start = checkdigit(miss_start)
            miss_end=input("the TrackID is " + str(id) + ". What is the missing end point?\n")
            miss_end = checkdigit(miss_end)
            Missed_Start_list.append(miss_start)
            Missed_End_list.append(miss_end)

            #displays final graph
            fig, ax =plt.subplots() #curve
            ax.set_xlabel('Frames')
            ax.set_ylabel('Signal Standard deviation')
            ax.set_title('SD trend of Track: '+str(id))
            plt.plot(x,label='Raw Curve')
            plt.plot(yy,label='Smoothened Curve')
            for local_min in local_minima:
                index,values = local_min
                plt.plot(index,values,'x',label='Algorithm start',color='green')
                plt.plot(peaks,yy[peaks],'o',label='Algorithm end',color='red')
                plt.axvline(manualstart,linestyle='--',label='Manual Start',color='lightgreen')
                plt.axvline(manualend,linestyle='--',label='Manual end',color='lightcoral')
                plt.axvline(miss_start,linestyle='--',label='Missing manual Start',color='darkgreen')
                plt.axvline(miss_end,linestyle='--',label='Missing manual end',color='darkred')
            ax.legend()
            plt.savefig('Track ID '+str(id))
            plt.show(block=True)
            break
            
        if miss =='n':
            print('Great! Next.\n')
            plt.savefig('Track ID '+str(id))
            plt.close()
            break
            
    for fr_peaks in peaks:
        file=open('result.csv','a',newline='')
        writer=csv.writer(file)
        ind=ind+1
        Append=[[str(ind),str(id),str(len(peaks)),str(index),str(fr_peaks),str(manualstart),str(manualend),skip,falsepositive,miss_start,miss_end,miss_count]]
        writer.writerows(Append)
    file.close()

#linear regression of starting point

All_start_list_manual=Manual_Start_list+len(Falsepos_Start_list)*[0]+Missed_Start_list
All_end_list_manual=Manual_End_list+len(Falsepos_End_list)*[0]+Missed_End_list
All_start_list_alg=Algorithm_Start_list+Falsepos_Start_list+len(Missed_Start_list)*[0]
All_end_list_alg=Algorithm_End_list+Falsepos_End_list+len(Missed_End_list)*[0]
colors=["blue"]*len(Manual_End_list)+["green"]*len(Falsepos_End_list)+["yellow"]*len(Missed_End_list)




data_start =pd.DataFrame({'manual_start':All_start_list_manual,'Algo_start':All_start_list_alg})
data_manual_start=np.array(data_start['manual_start']).reshape((-1,1))
data_algo_start=np.array(data_start['Algo_start'])
regr_start=LinearRegression()
regr_start.fit(data_manual_start,data_algo_start)

print(f"intercept: {regr_start.intercept_}")
print(f"coeffcient: {regr_start.coef_}")
print(f"R^2:{regr_start.score(data_manual_start,data_algo_start)}")



plt.scatter(data_start['manual_start'],data_start['Algo_start'],c=colors)
plt.plot(data_start['manual_start'],regr_start.predict(np.array(data_start['manual_start']).reshape((-1,1))),color ='red',label=
         f"R^2:{regr_start.score(data_manual_start,data_algo_start)}\ncoeffcient: {regr_start.coef_}\nintercept: {regr_start.intercept_}")
plt.xlabel("Manual Starting Data in Frame(10min gap)")
plt.ylabel('Algorithm Starting Data in Frame(10min gap)')
plt.title('Linear Regression of Starting Point')
plt.legend()
plt.show()


data_end=pd.DataFrame({'manual_end':All_end_list_manual,'Algo_end':All_end_list_alg})
data_manual_end=np.array(data_end['manual_end']).reshape((-1,1))
data_algo_end=np.array(data_end['Algo_end'])
regr_end=LinearRegression()
regr_end.fit(data_manual_end,data_algo_end)
print(f"intercept:{regr_end.intercept_}")
print(f"coeffcient: {regr_end.coef_}")
print(f"R^2:{regr_end.score(data_manual_end,data_algo_end)}")
plt.scatter(data_end['manual_end'],data_end['Algo_end'],c=colors)
plt.plot(data_end['manual_end'],regr_end.predict(np.array(data_end['manual_end']).reshape((-1,1))),color ='red',label=f"R^2:{regr_end.score(data_manual_end,data_algo_end)}\ncoeffecient:{regr_end.coef_}\nintercept:{regr_end.intercept_}")
plt.title('Linear Regression of Ending Point')
plt.xlabel("Manual Starting Data in Frame(10min gap)")
plt.ylabel('Algorithm Starting Data in Frame(10min gap)')
plt.legend()
plt.show()


print(f"Correctly Identidfied:{len(Manual_Start_list)}\n")
print(f"False Positive:{len(Falsepos_End_list)}\n")
print(f"Missed:{len(Missed_Start_list)}")