import time # imported for sleep

import sys  # default setting
from PyQt5 import QtWidgets, uic   # default setting
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar # imported for graph
import pyvisa
import u3


class Form(QtWidgets.QMainWindow):   
    def __init__(self):
        super().__init__()   
        uic.loadUi('AFG_and_U3_pulse_UI.ui', self)           # Load UI file 
       
##### U3 initiallization #####
        self.d = None
        self.d = u3.U3()
        self.d.debug = True
        self.d.configIO(FIOAnalog=0x0F)
        self.d.configIO(EnableCounter0=1,TimerCounterPinOffset = 6)

##### GUI setting #####
        self.refreshButton.clicked.connect(self.connection_refresh)
        self.selectButton.clicked.connect(self.select_Clicked)

        self.runButton.clicked.connect(self.run_clicked)  
        
        self.closeButton.clicked.connect(self.close_Clicked)
 
#####  list create #####
        self.xdata=[]
        self.ydata=[]   
        
######## graph setting #####  
        self.fig = plt.Figure((5,5))
        self.canvas = FigureCanvas(self.fig)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.graph.addWidget(self.canvas)
        self.graph.addWidget(self.toolbar)    
        self.ax = self.fig.add_subplot(111)
        self.ax.plot(self.xdata, self.ydata, 'ro', label="graph" )
        self.ax.set_xlabel("x")
        self.ax.set_xlabel("y")
        self.ax.patch.set_facecolor('white')
        self.ax.set_title("my graph")
        self.ax.legend()
        self.canvas.draw()       

##### Button_click conection #####
    def connection_refresh(self):
        self.rm = pyvisa.ResourceManager()
        self.comboBox.clear()
        self.comboBox.addItems(self.rm.list_resources())
        self.dev = self.rm.open_resource(self.comboBox.currentText())   
    def select_Clicked(self):
        self.dev = self.rm.open_resource(self.comboBox.currentText())
        
    def close_Clicked(self):
        print("clicked!!")
        self.dev.close()
        self.d.close()


    def run_clicked(self):  

        rep=int(self.lineEdit_rep.text()) 
        sec=float(self.lineEdit_duration.text())
        
        self.ax.cla()
        self.xdata=[]
        self.ydata=[]
        self.ax.plot(self.xdata, self.ydata, 'ro', label="graph" )
        self.ax.set_xlabel("x")
        self.ax.set_xlabel("y")
        self.ax.patch.set_facecolor('white')
        self.ax.set_title("my graph")
        self.ax.legend()
        self.canvas.draw()
        QtWidgets.QApplication.processEvents()
        
        self.d.getFeedback(u3.Counter(counter =0, Reset=True))
        QtWidgets.QApplication.processEvents() 

        for x in range(rep):   # Here, i is index, x is the value in the list, actually any symbol can be used for i and x
            
            self.xdata.append(x)  
#            self.output_on()

            self.Pulse_count() # clear counter
            time.sleep(sec)
            value=self.Pulse_count()
            self.ydata.append(value)
            print(x, value)
            time.sleep(1)
            self.ax.plot(self.xdata, self.ydata, 'ro', label="rep" )
            self.canvas.draw()
            QtWidgets.QApplication.processEvents()   # this is for update graph in user interface! (important)
            

##### instrument method define #####

    def Pulse_count(self):
        count=self.d.getFeedback(u3.Counter(counter =0, Reset=True))
        return count[0]
    
        
 #### common setting for pyqt##########
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = Form()
    w.show()
    sys.exit(app.exec_())