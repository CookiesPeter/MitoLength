import pandas as pd
import numpy as np
from scipy.signal import argrelextrema, find_peaks, filtfilt, butter
from matplotlib import pyplot as plt
import csv
import czifile as cz
import xml.etree.ElementTree as ET
from PySide6 import QtCore, QtWidgets
import sys

class Ui_Mainwindow(object):
    def setupUi(self, Mainwindow):
        Mainwindow.setObjectName("Mainwindow")
        Mainwindow.resize(470, 584)
        self.verticalLayout = QtWidgets.QVBoxLayout(Mainwindow)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(Mainwindow)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.Openfile = QtWidgets.QPushButton(Mainwindow)
        self.Openfile.setObjectName("Openfile")
        self.verticalLayout.addWidget(self.Openfile)
        self.label_10 = QtWidgets.QLabel(Mainwindow)
        self.label_10.setObjectName("label_10")
        self.verticalLayout.addWidget(self.label_10)
        self.label_7 = QtWidgets.QLabel(Mainwindow)
        self.label_7.setObjectName("label_7")
        self.verticalLayout.addWidget(self.label_7)
        self.czibutton = QtWidgets.QPushButton(Mainwindow)
        self.czibutton.setObjectName("czibutton")
        self.verticalLayout.addWidget(self.czibutton)
        self.label_12 = QtWidgets.QLabel(Mainwindow)
        self.label_12.setObjectName("label_12")
        self.verticalLayout.addWidget(self.label_12)
        self.label_2 = QtWidgets.QLabel(Mainwindow)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.Openfolder = QtWidgets.QPushButton(Mainwindow)
        self.Openfolder.setObjectName("Openfolder")
        self.verticalLayout.addWidget(self.Openfolder)
        self.label_13 = QtWidgets.QLabel(Mainwindow)
        self.label_13.setObjectName("label_13")
        self.verticalLayout.addWidget(self.label_13)
        self.label_3 = QtWidgets.QLabel(Mainwindow)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.Promslider = QtWidgets.QSlider(Mainwindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Promslider.sizePolicy().hasHeightForWidth())
        self.Promslider.setSizePolicy(sizePolicy)
        self.Promslider.setMinimumSize(QtCore.QSize(300, 0))
        self.Promslider.setMouseTracking(False)
        self.Promslider.setMaximum(9)
        self.Promslider.setPageStep(0)
        self.Promslider.setProperty("value", 2)
        self.Promslider.setOrientation(QtCore.Qt.Horizontal)
        self.Promslider.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.Promslider.setTickInterval(1)
        self.Promslider.setObjectName("Promslider")
        self.horizontalLayout_2.addWidget(self.Promslider)
        self.label_8 = QtWidgets.QLabel(Mainwindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy)
        self.label_8.setMinimumSize(QtCore.QSize(30, 0))
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_2.addWidget(self.label_8, 0, QtCore.Qt.AlignRight)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.label_4 = QtWidgets.QLabel(Mainwindow)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.Frameslider = QtWidgets.QSlider(Mainwindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Frameslider.sizePolicy().hasHeightForWidth())
        self.Frameslider.setSizePolicy(sizePolicy)
        self.Frameslider.setMinimumSize(QtCore.QSize(300, 0))
        self.Frameslider.setMaximum(500)
        self.Frameslider.setProperty("value", 60)
        self.Frameslider.setOrientation(QtCore.Qt.Horizontal)
        self.Frameslider.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.Frameslider.setTickInterval(50)
        self.Frameslider.setObjectName("Frameslider")
        self.horizontalLayout_3.addWidget(self.Frameslider)
        self.label_9 = QtWidgets.QLabel(Mainwindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy)
        self.label_9.setMinimumSize(QtCore.QSize(30, 0))
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_3.addWidget(self.label_9, 0, QtCore.Qt.AlignRight)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.hboxlayout = QtWidgets.QHBoxLayout()
        self.hboxlayout.setObjectName("hboxlayout")
        self.label_5 = QtWidgets.QLabel(Mainwindow)
        self.label_5.setMinimumSize(QtCore.QSize(200, 0))
        self.label_5.setMaximumSize(QtCore.QSize(306, 16777215))
        self.label_5.setObjectName("label_5")
        self.hboxlayout.addWidget(self.label_5)
        self.Dropbox = QtWidgets.QCheckBox(Mainwindow)
        self.Dropbox.setChecked(True)
        self.Dropbox.setObjectName("Dropbox")
        self.hboxlayout.addWidget(self.Dropbox, 0, QtCore.Qt.AlignRight)
        self.verticalLayout.addLayout(self.hboxlayout)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_14 = QtWidgets.QLabel(Mainwindow)
        self.label_14.setObjectName("label_14")
        self.horizontalLayout_5.addWidget(self.label_14)
        self.dropdaughter = QtWidgets.QCheckBox(Mainwindow)
        self.dropdaughter.setChecked(True)
        self.dropdaughter.setObjectName("dropdaughter")
        self.horizontalLayout_5.addWidget(self.dropdaughter, 0, QtCore.Qt.AlignRight)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_6 = QtWidgets.QLabel(Mainwindow)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout.addWidget(self.label_6)
        self.OrderSpin = QtWidgets.QSpinBox(Mainwindow)
        self.OrderSpin.setMinimum(1)
        self.OrderSpin.setMaximum(10)
        self.OrderSpin.setProperty("value", 4)
        self.OrderSpin.setObjectName("OrderSpin")
        self.horizontalLayout.addWidget(self.OrderSpin, 0, QtCore.Qt.AlignRight)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.pushButton = QtWidgets.QPushButton(Mainwindow)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_11 = QtWidgets.QLabel(Mainwindow)
        self.label_11.setObjectName("label_11")
        self.horizontalLayout_4.addWidget(self.label_11)
        self.buttonBox = QtWidgets.QDialogButtonBox(Mainwindow)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayout_4.addWidget(self.buttonBox)
        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.retranslateUi(Mainwindow)
        self.buttonBox.accepted.connect(Mainwindow.accept) # type: ignore
        self.buttonBox.rejected.connect(Mainwindow.reject) # type: ignore
        self.Openfile.pressed.connect(self.openfile) # type: ignore
        self.Openfolder.pressed.connect(self.openfolder) # type: ignore
        self.czibutton.pressed.connect(self.openczi) # type: ignore
        self.Promslider.valueChanged['int'].connect(self.label_8.setNum) # type: ignore
        self.Frameslider.valueChanged['int'].connect(self.label_9.setNum) # type: ignore
        self.pushButton.clicked.connect(self.preview) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Mainwindow)

    def retranslateUi(self, Mainwindow):
        _translate = QtCore.QCoreApplication.translate
        Mainwindow.setWindowTitle(_translate("Mainwindow", "Configurations"))
        self.label.setWhatsThis(_translate("Mainwindow", "This takes the \"export.csv\" file from Trackmate\'s Tracking data. Only csv file."))
        self.label.setText(_translate("Mainwindow", "Trackmate Output:"))
        self.Openfile.setText(_translate("Mainwindow", "Choose..."))
        self.label_10.setText(_translate("Mainwindow", ">No files selected<"))
        self.label_7.setWhatsThis(_translate("Mainwindow", "This takes the czi file from Zeiss imaging and extracts some metadata from it. Only czi file."))
        self.label_7.setText(_translate("Mainwindow", "Czi File:"))
        self.czibutton.setText(_translate("Mainwindow", "Choose..."))
        self.label_12.setText(_translate("Mainwindow", ">No files selected<"))
        self.label_2.setWhatsThis(_translate("Mainwindow", "This specifies the location you want to save the results at."))
        self.label_2.setText(_translate("Mainwindow", "Save folder location:"))
        self.Openfolder.setText(_translate("Mainwindow", "Save As..."))
        self.label_13.setText(_translate("Mainwindow", ">No location selected<"))
        self.label_3.setWhatsThis(_translate("Mainwindow", "This defines the threshold for the promience of mitosis identification. The higher, the more stringent the peak identification is. From 0 to 9."))
        self.label_3.setText(_translate("Mainwindow", "Prominence (Default=2):"))
        self.label_8.setText(_translate("Mainwindow", "2"))
        self.label_4.setWhatsThis(_translate("Mainwindow", "This defines the minimum expected frames between two mitotic peaks. Please specify according to your sampling interval."))
        self.label_4.setText(_translate("Mainwindow", "Minimum period between mitosis (Default=60):"))
        self.label_9.setText(_translate("Mainwindow", "60"))
        self.label_5.setWhatsThis(_translate("Mainwindow", "This button controls whether to drop cells that has come in contact with the margins of the field of view."))
        self.label_5.setText(_translate("Mainwindow", "Exclude cells at the margins"))
        self.Dropbox.setText(_translate("Mainwindow", "Exclude"))
        self.label_14.setWhatsThis(_translate("Mainwindow","Choose whether to keep only one of the daughter cells from a cell division."))
        self.label_14.setText(_translate("Mainwindow", "Exclude one of the daughter cell:"))
        self.dropdaughter.setText(_translate("Mainwindow", "Exclude"))
        self.label_6.setWhatsThis(_translate("Mainwindow", "<html><head/><body><p>Frequency of the butterworth. The stronger the frequency, the higher the cutoff frequency. Usually lower means more smoothening. From 1 to 10.</p></body></html>"))
        self.label_6.setText(_translate("Mainwindow", "Smoothing power (Default 4):"))
        self.pushButton.setText(_translate("Mainwindow", "Preview smoothening"))
        self.label_11.setText(_translate("Mainwindow", "©Poon Lab"))

    def openfile(self):
        self.filepath,_ = QtWidgets.QFileDialog.getOpenFileName(None, caption="Open export.csv", filter="Csv Files (*.csv);;All Files (*)")
        if self.filepath:
            # do something with the selected file
            print("Selected file:", self.filepath)
            self.label_10.setText(self.filepath)

    def openfolder(self):
        self.savepath,_ = QtWidgets.QFileDialog.getSaveFileName(None, caption="Save As...", filter="Csv Files (*.csv);;All Files (*)")
        if self.savepath:
            # do something with the selected file
            print("Selected file:", self.savepath)
            self.label_13.setText(self.savepath)

    def openczi(self):
        self.czipath,_ = QtWidgets.QFileDialog.getOpenFileName(None, caption="Open Czi File", filter="Czi Files (*.czi);;All Files (*)")
        if self.czipath:
            # do something with the selected file
            print("Selected file:", self.czipath)
            self.label_12.setText(self.czipath)

    def butter_lowpass_filtfilt(self,data,fre,order=8):
        b,a = butter(order,fre,"lowpass",analog=False)
        output = filtfilt(b,a,data,axis=0)
        return output
    
    def preview(self):
        try:
            if self.filepath:
                dfp=pd.read_csv(self.filepath,low_memory=False)
                dfp.drop(index = dfp.index[0:3],axis=0,inplace=True)
                newdfp=dfp[dfp['TRACK_ID']=='0']
                newdfpp=newdfp[['FRAME','STD_INTENSITY_CH1']].sort_values(by='FRAME',ascending=True)
                xp = newdfpp.STD_INTENSITY_CH1.values.astype(float)
                filtxp=self.butter_lowpass_filtfilt(xp,fre=ui.OrderSpin.value()/10)
                plt.plot(xp,label='raw',color='blue')
                plt.plot(filtxp,label='smoothened',color='red')
                plt.legend()
                plt.show()
        except:
            QtWidgets.QMessageBox.warning(None, 'Error', 'No csv import selected!')

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QDialog()
    ui = Ui_Mainwindow()
    ui.setupUi(window)
    window.show()
    app.exec_()

#define local minima before peak
def detect_local_minima_before_peaks(signal, peak_indices):
    local_minima = []
    for peak_index in peak_indices:
        before_peak = signal[:peak_index]
        local_min_index = argrelextrema(before_peak,np.less)[0]
        if not local_min_index.any():
            continue
        local_min_index = local_min_index[-1]
        local_minima.append((local_min_index,peak_index))
    return local_minima

#define butter_lowpass_filtfilt
def butter_lowpass_filtfilt(data,fre,order=8):
    b,a = butter(order,fre,"lowpass",analog=False)
    output = filtfilt(b,a,data,axis=0)
    return output

#get metadata from czi
xml_metadata = cz.CziFile(ui.czipath).metadata()
root = ET.fromstring(xml_metadata)
for val in root.findall('.//Distance[@Id="X"]/Value'):
    pixel_size_in_meters=float(val.text)
    pixel_size_in_microns = float(pixel_size_in_meters)*1000000000

#data import and tidying
df=pd.read_csv(ui.filepath,low_memory=False)

#Drop some useless labels
df.drop(index = df.index[0:3],axis=0,inplace=True)

#set index
df.set_index('TRACK_ID',inplace=True)
df.index = df.index.astype(int) 
df.FRAME= df.FRAME.astype(int)
df.POSITION_X = df.POSITION_X.astype(float)
df.POSITION_Y = df.POSITION_Y.astype(float)
celldia = np.mean(df.RADIUS.astype(float).astype(int))

#set bound
if ui.Dropbox.isChecked():
    bound = pixel_size_in_microns-celldia
    df.drop(df[df.POSITION_X < celldia].index,axis=0,inplace=True)
    df.drop(df[df.POSITION_X > bound].index,axis=0,inplace=True)
    df.drop(df[df.POSITION_Y < celldia].index,axis=0,inplace=True)
    df.drop(df[df.POSITION_Y > bound].index,axis=0,inplace=True)

#append/start a csv file, set initial indices, add a header
ind=0
file = open(ui.savepath,'a',newline='')
writer=csv.writer(file)
head=['Index','TrackID','Interphase apoptosis','mitotic entry','anaphase onset','mitotic apoptosis','mitotic slippage','multipolar division','fusion','post mitoitc Apoptosis','second mitotic entry','second anaphase onset','second anaphase onset','second post mitotic apoptosis','#splits']
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

    #Dropping Daughter cells
    if min(newdf['FRAME'])!=0 or max(newdf['FRAME'])<140:
        continue
    
    #Smoothening the curve by filtfilt
    yy=butter_lowpass_filtfilt(x,fre=ui.OrderSpin.value()/10)
    x=x/max(x)
    yy=yy/max(yy)
    #find peaks and threshold
    peaks = find_peaks(yy,distance=ui.Frameslider.value(),prominence=ui.Promslider.value())[0]
    
    #Dropping Daughter cells
    if ui.dropdaughter.isChecked() is True:
        if min(newdf["FRAME"])!=0 or max(newdf["FRAME"])<140:
            continue
    
    #give up if no peaks identified
    if not list(peaks):
        file =open(ui.savepath,'a',newline='')
        writer=csv.writer(file)
        ind=ind+1
        Append=[[str(ind),str(id),'','','','','','','','','','','','','0']]
        writer.writerows(Append)    
        continue

    #Find local maximum with smoothened curve
    local_minima = detect_local_minima_before_peaks(x, peaks)

    #fit frames
    peaks = list(idd + min(newdf['FRAME']) for idd in peaks)
    local_minima = list((idd[0] + min(newdf['FRAME']),idd[1] + min(newdf['FRAME'])) for idd in local_minima)

    #Excel output
    file =open(ui.savepath,'a',newline='')
    writer=csv.writer(file)
    ind=ind+1
    if len(local_minima)==1:
        Append=[[str(ind),str(id),'',str(local_minima[0][0]),str(local_minima[0][1]),'','','','','','','','','',len(local_minima)]]
        writer.writerows(Append)
    elif len(local_minima)==2:
        Append=[[str(ind),str(id),'',str(local_minima[0][0]),str(local_minima[0][1]),'','','','','',str(local_minima[1][0]),str(local_minima[1][1]),'','',len(local_minima)]]
        writer.writerows(Append)
    file.close()