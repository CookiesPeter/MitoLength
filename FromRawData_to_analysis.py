import pandas as pd
import numpy as np
from scipy.signal import argrelextrema, find_peaks, filtfilt, butter
from matplotlib import pyplot as plt
from sklearn.linear_model import LinearRegression #import Linear Package
import csv

#Create list for data
Manual_Start_list=[]
Manual_End_list=[]
Algorithm_Start_list=[]
Algorithm_End_list=[]

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
head=['Index','TrackID','#splits','Start','end','manualstart','manualend','false+ count','missed count']
ind=1
writer.writerow(head)
file.close()

skip=int(input('please indicate the track Id you wanna skip to:'))
falsepositive=0

#Search unique TRACK ID
for id in df.index.unique():
    
    if id < skip:
        continue

    newdf=df.loc[id,['FRAME','STD_INTENSITY_CH1']].sort_values(by='FRAME',ascending=True)
    x = newdf.STD_INTENSITY_CH1.values.astype(float)
    
    #Screen for tracks with length more than 50 frames
    if len(x) <50:
         continue
    
    #Smoothening the curve by filtfilt
    b, a = butter(8, 0.125,analog=False)
    yy= filtfilt(b,a,x)

    #find peaks (dynamic peak here??)
    #threshold = float(np.max(yy))*0.75
    peaks,_ = find_peaks(yy,height=300,distance=60,prominence=10)

    #give up if no peaks identified
    if not peaks.size:
            continue
    
    #Find local maximum with smoothened curve
    local_minima = detect_local_minima_before_peaks(x, peaks)
    #Record Algorithm Starting Point and Ending Point
    if len(peaks)==len(local_minima):
        for i in range(len(peaks)):
            Algorithm_End_list.append(peaks[i])
            Algorithm_Start_list.append(local_minima[i][0])
    else:
        continue
    #give up if total frame less than 30
    if np.max(newdf.FRAME.values)<30:
        continue

    #getting user input for counting
    for local_min in local_minima:
        index,values = local_min
        x = x.astype(float)
        plt.plot(x,label='Raw Curve')
        plt.plot(yy,label='Smoothened Curve')
        plt.plot(index,values,'x',label='Algorithm start',color='green')
        plt.plot(peaks,yy[peaks],'o',label='Algorithm end',color='red') #peak dots
        plt.title('TRACK '+ str(id))
        plt.show(block=False)
        prescence=input('Do you see a peak near to computer? Please type y or n.\n')
        prescence=checkyn(prescence)
        skip=False
        if prescence == 'y':   
            manualstart=input("the TrackID is " + str(id) + ". Please input the starting point you count.\n")
            manualstart = checkdigit(manualstart)
            manualend=input("the TrackID is " + str(id) + ". What is the end point?\n")
            manualend = checkdigit(manualend)
            
            Manual_Start_list.append(manualstart)
            Manual_End_list.append(manualend)
        elif prescence == 'n':
            falsepositive = falsepositive+1
            skip = True
            continue
    plt.close()

    if skip is True:
        print('Sad but next.')
        continue

    #show graph
    while True:
        x = x.astype(float)
        fig, ax =plt.subplots() #curve
        ax.set_xlabel('Frames')
        ax.set_ylabel('Signal Standard deviation')
        ax.set_title('SD trend of Track: '+str(id))
        #plot
        plt.plot(x,label='Raw Curve')
        plt.plot(yy,label='Smoothened Curve') #smooth
        #define limits
        plt.xlim(left=np.min(newdf.FRAME.values),right=np.max(newdf.FRAME.values))
        for local_min in local_minima:
            index,values = local_min
            plt.plot(index,values,'x',label='Algorithm start',color='green')
            plt.plot(peaks,yy[peaks],'o',label='Algorithm end',color='red') #peak dots
        #plt.hlines(*width[1:], color="C2")
        plt.title('TRACK '+ str(id))
        try:
            plt.axvline(manualstart,linestyle='--',label='Manual Start',color='green')
            plt.axvline(manualend,linestyle='--',label='Manual end',color='red')
        except:
            print('error.Skipping.')
            break
        ax.legend()
        plt.show(block=False)

        miss_count = 0
        miss=input('Any peak missing?Input y or n.\n')
        miss=checkyn(miss)
        if miss == 'y':
            miss_count = miss_count+1
            miss_start=input("the TrackID is " + str(id) + ". Please input the missing starting point you count.\n")
            miss_start = checkdigit(miss_start)
            miss_end=input("the TrackID is " + str(id) + ". What is the missing end point?\n")
            miss_end = checkdigit(miss_end)
            fig, ax =plt.subplots() #curve
            ax.set_xlabel('Frames')
            ax.set_ylabel('Signal Standard deviation')
            ax.set_title('SD trend of Track: '+str(id))
            #plot
            plt.plot(x,label='Raw Curve')
            plt.plot(yy,label='Smoothened Curve') #smooth
            #define limits
            plt.xlim(left=np.min(newdf.FRAME.values),right=np.max(newdf.FRAME.values))
            for local_min in local_minima:
                index,values = local_min
                plt.plot(index,values,'x',label='Algorithm start',color='green')
                plt.plot(peaks,yy[peaks],'o',label='Algorithm end',color='red') #peak dots
            #plt.hlines(*width[1:], color="C2")
            plt.title('TRACK '+ str(id))
            try:
                plt.axvline(manualstart,linestyle='--',label='Manual Start',color='green')
                plt.axvline(manualend,linestyle='--',label='Manual end',color='red')
                plt.axvline(miss_start,linestyle='--',label='Missing manual Start',color='darkgreen')
                plt.axvline(miss_end,linestyle='--',label='Missing manual end',color='darkred')
            except:
                print('error.Skipping.')
                break
            ax.legend()
            plt.savefig('Track ID '+str(id))
            plt.show()
            break
        if miss =='n':
            print('Great! Next.\n')
            plt.savefig('Track ID '+str(id))
            plt.close()
            break
    for fr_peaks in peaks:
        file=open('Results.csv','a',newline='')
        writer=csv.writer(file)
        Append=[[str(ind),str(id),str(len(peaks)),str(index),str(fr_peaks),str(manualstart),str(manualend),falsepositive,miss_count]]
        ind=ind+1
        writer.writerows(Append)
    file.close()

#linear regression of starting point
data_start =pd.DataFrame({'manual_start':Manual_Start_list,'Algo_start':Algorithm_Start_list})
data_manual_start=np.array(data_start['manual_start']).reshape((-1,1))
data_algo_start=np.array(data_start['Algo_start'])
regr_start=LinearRegression()
regr_start.fit(data_manual_start,data_algo_start)

print(f"intercept: {regr_start.intercept_}")
print(f"coeffcient: {regr_start.coef_}")
print(f"R^2:{regr_start.score(data_manual_start,data_algo_start)}")

plt.scatter(data_start['manual_start'],data_start['Algo_start'])
plt.plot(data_start['manual_start'],regr_start.predict(np.array(data_start['manual_start']).reshape((-1,1))),color ='red')
plt.title('Linear Regression of Starting Point')
plt.axline( (0,0),slope=1,linestyle='--',color='grey',label='y=x')
larger=np.maximum(np.max(Manual_Start_list),np.max(Algorithm_Start_list))
plt.xlim(0,larger)
plt.ylim(0,larger)
plt.show()

data_end=pd.DataFrame({'manual_end':Manual_End_list,'Algo_end':Algorithm_End_list})
data_manual_end=np.array(data_end['manual_end']).reshape((-1,1))
data_algo_end=np.array(data_end['Algo_end'])
regr_end=LinearRegression()
regr_end.fit(data_manual_end,data_algo_end)
print(f"intercept:{regr_end.intercept_}")
print(f"coeffcient: {regr_end.coef_}")
print(f"R^2:{regr_end.score(data_manual_end,data_algo_end)}")
plt.scatter(data_end['manual_end'],data_end['Algo_end'])
plt.plot(data_end['manual_end'],regr_end.predict(np.array(data_end['manual_end']).reshape((-1,1))),color ='red')
plt.title('Linear Regression of Ending Point')
plt.axline( (0,0),slope=1,linestyle='--',color='grey',label='y=x')
plt.show()