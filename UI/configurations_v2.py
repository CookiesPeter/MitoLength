from PySide6 import QtCore, QtWidgets
import sys

class Ui_Mainwindow(object):
    def setupUi(self, Mainwindow):
        Mainwindow.setObjectName("Mainwindow")
        Mainwindow.resize(286, 432)
        self.verticalLayout = QtWidgets.QVBoxLayout(Mainwindow)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(Mainwindow)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.Openfile = QtWidgets.QPushButton(Mainwindow)
        self.Openfile.setObjectName("Openfile")
        self.verticalLayout.addWidget(self.Openfile)
        self.label_7 = QtWidgets.QLabel(Mainwindow)
        self.label_7.setObjectName("label_7")
        self.verticalLayout.addWidget(self.label_7)
        self.czibutton = QtWidgets.QPushButton(Mainwindow)
        self.czibutton.setObjectName("czibutton")
        self.verticalLayout.addWidget(self.czibutton)
        self.label_2 = QtWidgets.QLabel(Mainwindow)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.Openfolder = QtWidgets.QPushButton(Mainwindow)
        self.Openfolder.setObjectName("Openfolder")
        self.verticalLayout.addWidget(self.Openfolder)
        self.label_3 = QtWidgets.QLabel(Mainwindow)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.Promslider = QtWidgets.QSlider(Mainwindow)
        self.Promslider.setMaximum(9)
        self.Promslider.setPageStep(0)
        self.Promslider.setProperty("value", 2)
        self.Promslider.setOrientation(QtCore.Qt.Horizontal)
        self.Promslider.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.Promslider.setTickInterval(1)
        self.Promslider.setObjectName("Promslider")
        self.verticalLayout.addWidget(self.Promslider)
        self.label_4 = QtWidgets.QLabel(Mainwindow)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.Frameslider = QtWidgets.QSlider(Mainwindow)
        self.Frameslider.setMaximum(500)
        self.Frameslider.setProperty("value", 60)
        self.Frameslider.setOrientation(QtCore.Qt.Horizontal)
        self.Frameslider.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.Frameslider.setTickInterval(50)
        self.Frameslider.setObjectName("Frameslider")
        self.verticalLayout.addWidget(self.Frameslider)
        self.hboxlayout = QtWidgets.QHBoxLayout()
        self.hboxlayout.setObjectName("hboxlayout")
        self.label_5 = QtWidgets.QLabel(Mainwindow)
        self.label_5.setMinimumSize(QtCore.QSize(200, 0))
        self.label_5.setMaximumSize(QtCore.QSize(306, 16777215))
        self.label_5.setObjectName("label_5")
        self.hboxlayout.addWidget(self.label_5)
        self.Dropbox = QtWidgets.QCheckBox(Mainwindow)
        self.Dropbox.setObjectName("Dropbox")
        self.hboxlayout.addWidget(self.Dropbox, 0, QtCore.Qt.AlignRight)
        self.verticalLayout.addLayout(self.hboxlayout)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_6 = QtWidgets.QLabel(Mainwindow)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout.addWidget(self.label_6)
        self.OrderSpin = QtWidgets.QSpinBox(Mainwindow)
        self.OrderSpin.setMaximum(10)
        self.OrderSpin.setProperty("value", 4)
        self.OrderSpin.setObjectName("OrderSpin")
        self.horizontalLayout.addWidget(self.OrderSpin, 0, QtCore.Qt.AlignRight)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(Mainwindow)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Mainwindow)
        self.buttonBox.accepted.connect(Mainwindow.accept) # type: ignore
        self.buttonBox.rejected.connect(Mainwindow.reject) # type: ignore
        self.Openfile.pressed.connect(Mainwindow.accept) # type: ignore
        self.Openfolder.pressed.connect(Mainwindow.accept) # type: ignore
        self.Dropbox.toggled['bool'].connect(self.Dropbox.toggle) # type: ignore
        self.OrderSpin.valueChanged['int'].connect(self.OrderSpin.setValue) # type: ignore
        self.Promslider.valueChanged['int'].connect(self.Promslider.setValue) # type: ignore
        self.Frameslider.valueChanged['int'].connect(self.Frameslider.setValue) # type: ignore
        self.czibutton.pressed.connect(Mainwindow.openczi) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Mainwindow)

    def retranslateUi(self, Mainwindow):
        _translate = QtCore.QCoreApplication.translate
        Mainwindow.setWindowTitle(_translate("Mainwindow", "Configurations"))
        self.label.setText(_translate("Mainwindow", "Trackmate Output:"))
        self.Openfile.setText(_translate("Mainwindow", "Choose..."))
        self.label_7.setText(_translate("Mainwindow", "Czi File:"))
        self.czibutton.setText(_translate("Mainwindow", "Choose..."))
        self.label_2.setText(_translate("Mainwindow", "Save folder location:"))
        self.Openfolder.setText(_translate("Mainwindow", "Save As..."))
        self.label_3.setText(_translate("Mainwindow", "Prominence:"))
        self.label_4.setText(_translate("Mainwindow", "Minimum frame number between mitosis:"))
        self.label_5.setText(_translate("Mainwindow", "Drop marginal cells?"))
        self.Dropbox.setText(_translate("Mainwindow", "Drop"))
        self.label_6.setText(_translate("Mainwindow", "Order of Butterworth"))

    def openfile(self):
        filepath = QtWidgets.QFileDialog.getOpenFileName(None, caption="Open File", filter="Csv Files (*.csv);;All Files (*)")
        if filepath:
            # do something with the selected file
            print("Selected file:", filepath)

    def openfolder(self):
        savepath = QtWidgets.QFileDialog.getSaveFileName(None, caption="Open File", filter="Csv Files (*.csv);;All Files (*)")
        if savepath:
            # do something with the selected file
            print("Selected file:", savepath)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QDialog()
    ui = Ui_Mainwindow()
    ui.setupUi(window)
    window.show()
    app.exec_()

print(ui.OrderSpin.value())
print(ui.Dropbox.isChecked())
print(ui.Promslider.value())
print(ui.Frameslider.value())