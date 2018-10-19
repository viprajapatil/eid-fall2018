"""
Interfacing DHT22 with Rpi3
@author Vipraja Patil
@description
Created .ui files using QT GUI. Using these .ui files craeted a Python application for retrieving temperature and humidity values from DHT22 sensor which is interfaced with Rpi3 and displaying them.
@references:
https://stackoverflow.com/questions/11812000/login-dialog-pyqt
https://ralsina.me/posts/BB974.html
https://gist.github.com/pklaus/3e16982d952969eb8a9a#file-embedding_in_qt5-py-L14
https://www.youtube.com/watch?v=7SrD4l2o-uk
https://www.w3schools.com/python/python_mysql_getstarted.asp
"""
import sys
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
import Adafruit_DHT as sensor
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import mysql.connector

temp_list = []
hum_list = []

# Class defining Login dialog
class Login(QDialog):
    def __init__(self, parent=None):
        super(Login, self).__init__(parent)
        loadUi('login.ui',self)
        self.setWindowTitle('Login')
        self.user.text()
        self.password.text()
        self.login_button.clicked.connect(self.login_func)

    def login_func(self):
        if (self.user.text() == "vipraja" and self.password.text() == "vipraja"):
           self.accept()
        else:
           self.login_result.setText('Login unsucessful')

# This class includes the basic initialization required for displaying a graph
class Graph(FigureCanvas):
    def __init__(self, parent=None, width=10, height=7, dpi=300):
        graph = Figure(figsize=(width, height), dpi=dpi)
        self.axes = graph.add_subplot(111)
        self.axes.clear()
        self.compute_initial_figure()

        FigureCanvas.__init__(self,graph)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        
# This class defines functions for temperature graph.
# compute_initial_figure -  This function creates a initial graph which is displayd at the start
# of the application
# update_figure - This function updates the graph after every 12secs
# reference - https://gist.github.com/pklaus/3e16982d952969eb8a9a#file-embedding_in_qt5-py-L14
class temperature_graph(Graph):
    def __init__(self, *args, **kwargs):
        Graph.__init__(self, *args, **kwargs)
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_figure)
        timer.start(12000)

    def compute_initial_figure(self):
        self.axes.plot([0, 1, 2, 3], [0, 0, 0 ,0], 'r')
    
    def update_figure(self):
        self.axes.clear()
        self.axes.plot([0, 1, 2, 3], temp_list[-4:], 'r')
        self.draw()

# This class defines functions for humidity graph.
# compute_initial_figure -  This function creates a initial graph which is displayd at the start
# of the application
# update_figure - This function updates the graph after every 12secs
# reference - https://gist.github.com/pklaus/3e16982d952969eb8a9a#file-embedding_in_qt5-py-L14
class humidity_graph(Graph):
    def __init__(self, *args, **kwargs):
        Graph.__init__(self, *args, **kwargs)
        timer1 = QtCore.QTimer(self)
        timer1.timeout.connect(self.update_figure)
        timer1.start(12000)

    def compute_initial_figure(self):
        self.axes.plot([0, 1, 2, 3], [0, 0, 0 ,0], 'r')
    
    def update_figure(self):
        self.axes.clear()
        print(hum_list[-4:])
        self.axes.plot([0, 1, 2, 3], hum_list[-4:], 'r')
        self.draw()
 
# Main class which initializes all the functions required for displaying sensor values
class project1(QDialog):
    def __init__(self, parent=None):
        super(project1,self).__init__()
        loadUi('project2.ui',self)
        self.setWindowTitle('EID project 1')
        self.temp_button = 0
        self.hum_button = 0
        self.conversion_flag = 0      # 0- Celsius, 1- Fahrenheit
		self.temp_count = 0;
		self.hum_count = 0;
        time = QTime.currentTime()
        self.temp_threshold.text()
        self.hum_threshold.text()
        self.temp_widget = QWidget(self)
        self.temp_widget.setGeometry(QtCore.QRect(60,350,500,350))
        temp_layout = QVBoxLayout(self.temp_widget)
        temp = temperature_graph(self.temp_widget, width=4, height=3, dpi=50)
        self.hum_widget = QWidget(self)
        self.hum_widget.setGeometry(QtCore.QRect(400,350,500,350))
        hum_layout = QVBoxLayout(self.hum_widget)
        hum = humidity_graph(self.hum_widget, width=4, height=3, dpi=50)
        self.refresh_temp.clicked.connect(self.temp_refresh_clicked)
        self.refresh_hum.clicked.connect(self.humidity_refresh_clicked)
        self.conversion_button.clicked.connect(self.conversion_clicked)
        self.get_temp()
        self.get_hum()
		
		#Create mysql database
		mydb = mysql.connector.connect(
				host="localhost",
				user="vipraja",
				passwd="vipraja",
				database="project2_database"
			)
		mycursor = mydb.cursor()
		try:
			mycursor.execute("CREATE DATABASE project2_database")
		except mysql.connector.Error as err:
			print("Failed creating database: {}".format(err))
			exit(1)
		
		mycursor.execute("""CREATE TABLE IF NOT EXISTS Temperature(
						Count INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
						Temperature_value DOUBLE,
						Highest DOUBLE,
						Lowest DOUBLE,
						Average DOUBLE,
						Last DOUBLE,
						Timestamp DateTime""")
		mydb.commit()
		mycursor.execute("""CREATE TABLE IF NOT EXISTS Humidity(
						Count INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
						Humidity_value DOUBLE,
						Highest DOUBLE,
						Lowest DOUBLE,
						Average DOUBLE,
						Last DOUBLE,
						Timestamp DateTime""")
		mydb.commit()


    @pyqtSlot()
    # Displays temperature values, allows user to enter threshold value and gives an alert accordingly
    def get_temp(self):
        try:
            time = QTime.currentTime()
            humidity,temp = sensor.read(sensor.DHT22, 4)
            if temp is None and humidity is None:
               self.temp_value.setText('ERROR')
            else:
               temp_list.append(round(temp,4))
			   temp_count++;
               tstr = self.temp_threshold.text()
               if not tstr:
                  t = 26
               else:
                  t = int(tstr)
               if self.temp_button == 1:
                  if self.conversion_flag == 1:
                     temp = conversion(temp)
                     tstr = self.temp_threshold.text()
                     if temp > (t*1.8)+32:
                        self.alarm_temp.setText('ALERT HIGH TEMP')
                     else:
                        self.alarm_temp.setText('')
                     self.temp_value.setText('{} F'.format(round(temp,4)))
                  else:
                     if temp > t:
                        self.alarm_temp.setText('ALERT HIGH TEMP')
                     else:
                        self.alarm_temp.setText('')
                    
                  self.temp_value.setText('{} C'.format(round(temp,4)))
                  self.temp_time.setText(time.toString(Qt.DefaultLocaleLongDate))
                  self.temp_button = 0

               temp_avg = 0
               temp_list_count = 0;
               for i in temp_list:
                  temp_avg = i + temp_avg
                  temp_list_count = temp_list_count + 1
               temp_avg = temp_avg/temp_list_count
               if self.conversion_flag == 1:
                  temp_avg_f = conversion(temp_avg)
			
			if temp_count is 8:
				if self.conversion_flag == 1:
					self.last_temp_label.setText('Last value: {} F'.format(round(temp,2)))					
					self.avg_temp_label.setText('Average: {} F'.format(round(temp_avg_f,2)))					
					self.high_temp_label.setText('Highest: {} F'.format(round(conversion(max(temp_list),2)))	
					self.low_temp_label.setText('Lowest: {} F'.format(round(conversion(min(temp_list),2)))	
				else:
					self.last_temp_label.setText('Last value: {} C'.format(round(temp,2)))
					self.avg_temp_label.setText('Average: {} C'.format(round(temp_avg,2)))
					self.high_temp_label.setText('Highest: {} C'.format(round(max(temp_list),2)))
					self.low_temp_label.setText('Lowest: {} C'.format(round(min(temp_list),2)))
				# print timestamp
				self.last_temp_time.setText('Time: {}'.format(time.toString(Qt.DefaultLocaleLongDate)))
				self.avg_temp_time.setText('Time: {}'.format(time.toString(Qt.DefaultLocaleLongDate)))
				self.high_temp_time.setText('Time: {}'.format(time.toString(Qt.DefaultLocaleLongDate)))
				self.low_temp_time.setText('Time: {}'.format(time.toString(Qt.DefaultLocaleLongDate)))

			# Insert values in mysql database
			insert_statement = "INSERT INTO Temperature (Temperature_value, Highest, Lowest, Average, Last, Timestamp) VALUES (%d, %d, %d, %d, %d, %s)"
			val = (temp, max(temp_list), min(temp_list), temp_avg, temp, time.toString(Qt.DefaultLocaleLongDate))
			mycursor.execute(insert_statement, val)
			mydb.commit()
			
        finally:
               self.temp_button = 0
               QTimer.singleShot(1000, self.get_temp)

	# Celcius to Fahreinheit
	def conversion(temp):
		temp = temp * 1.8
		temp = temp + 32
		return temp
			   
    # Displays humidity values, allows user to enter threshold value and gives an alert accordingly
    def get_hum(self):
        try:
            time = QTime.currentTime()
            humidity,temp = sensor.read(sensor.DHT22, 4)
            if temp is None and humidity is None:
               self.hum_value.setText('ERROR')
            else:
				hum_count++;
               if self.hum_button == 1:
                  self.hum_value.setText('{} %'.format(round(humidity,4)))
                  self.hum_time.setText(time.toString(Qt.DefaultLocaleLongDate))
                  self.hum_button = 0
               hstr = self.hum_threshold.text()
               if not hstr:
                   h = 50
               else:
                   h = int(hstr)                  
               if humidity > h:
                  self.alarm_hum.setText('ALERT HIGH HUM')
               else:
                  self.alarm_hum.setText('')
               hum_avg = 0
               hum_list_count = 0
               hum_list.append(round(humidity,4))
               for i in hum_list:
                  hum_avg = i + hum_avg
                  hum_list_count = hum_list_count + 1
               hum_avg = hum_avg/hum_list_count
			   
			   if hum_count is 8:
					self.last_hum_label.setText('Last value: {} %'.format(round(temp,2)))
					self.avg_hum_label.setText('Average: {} %'.format(round(temp_avg,2)))
					self.high_hum_label.setText('Highest: {} %'.format(round(max(temp_list),2)))
					self.low_hum_label.setText('Lowest: {} %'.format(round(min(temp_list),2)))
				
			# Insert Humidity values in mysql data base
			insert_statement = "INSERT INTO Humidity (Humidity_value, Highest, Lowest, Average, Last, Timestamp) VALUES (%d, %d, %d, %d, %d, %s)"
			val = (humidity, max(hum_list), min(hum_list), hum_avg, humidity, time.toString(Qt.DefaultLocaleLongDate))
			mycursor.execute(insert_statement, val)
			mydb.commit()
			
        finally:
               self.hum_button = 0
               QTimer.singleShot(1000, self.get_hum)

    # Whenever temeprature refresh button is pressed this function is called. This function then calls get_temp()
    # for displaying the temperature value
    def temp_refresh_clicked(self):
        self.temp_button = 1
        time = QTime.currentTime()
        self.get_temp()

    # Whenever humidity refresh button is pressed this function is called. This function then calls get_hum()
    # for displaying the humidity value
    def humidity_refresh_clicked(self):
        self.hum_button = 1
        time = QTime.currentTime()
        self.get_hum()

    # This function is called whenever the user needs to switch between units Celsius and Fahreinheit
    def conversion_clicked(self):
        self.conversion_flag = 1 - self.conversion_flag

if __name__ == '__main__':
    app = QApplication(sys.argv)
    login = Login()

    if login.exec_() == QtWidgets.QDialog.Accepted:
       widget = project1()
       widget.show()
       sys.exit(app.exec_())

