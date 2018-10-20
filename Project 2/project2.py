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
from datetime import datetime, time
import MySQLdb
import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import socket

temp_list = []
hum_list = []
#Create mysql database

db = MySQLdb.connect(host="localhost", user="root", passwd="root", db="project2db")
# Create a Cursor object to execute queries.
cur = db.cursor()

cur.execute("DELETE IGNORE FROM temperatureDB")
db.commit()
cur.execute("DELETE IGNORE FROM humidityDB")
db.commit()
cur.execute("""CREATE TABLE IF NOT EXISTS humidityDB (
                    count int NOT NULL AUTO_INCREMENT,
                    humidity varchar(255),
                    timestamp varchar(255),
                    highest varchar(255),
                    lowest varchar(255),
                    last varchar(255),
                    average varchar(255),
                    PRIMARY KEY (count)
                    );""")
db.commit();

cur.execute("""CREATE TABLE IF NOT EXISTS temperatureDB (
                    count int NOT NULL AUTO_INCREMENT,
                    temperature varchar(255),
                    timestamp varchar(255),
                    highest varchar(255),
                    lowest varchar(255),
                    last varchar(255),
                    average varchar(255),
                    PRIMARY KEY (count)
                    );""")
db.commit()

class WSHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print('new connection')
      
    def on_message(self, message):
        print('message received:  {}'.format(message))
        # Reverse Message and send it back
        print('sending back message: %s' % message[::-1])
        self.write_message(message[::-1])
 
    def on_close(self):
        print('connection closed')
 
    def check_origin(self, origin):
        return True
 
application = tornado.web.Application([
    (r'/ws', WSHandler),
])

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
        self.temp_count = 0
        self.hum_count = 0
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
        

    @pyqtSlot()
    # Celcius to Fahreinheit
    def conversion(self, temp):
        temp = temp * 1.8
        temp = temp + 32
        return temp

    # Displays temperature values, allows user to enter threshold value and gives an alert accordingly
    def get_temp(self):
        try:
            time = QTime.currentTime()
            humidity,temp = sensor.read(sensor.DHT22, 4)
            if temp is None and humidity is None:
               self.temp_value.setText('ERROR')
            else:
                self.temp_count = self.temp_count + 1
                today = datetime.now().strftime("%H:%M:%S %Y-%m-%d")
                temp_list.append(round(temp,4))
                print('{} count:{}'.format(temp,self.temp_count))
                tstr = self.temp_threshold.text()
                if not tstr:
                    t = 26
                else:
                    t = int(tstr)
                if self.temp_button == 1:
                    if self.conversion_flag == 1:
                        temp = temp * 1.8
                        temp = temp + 32
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
                    self.temp_time.setText(today)
                    self.temp_button = 0

                temp_avg = 0
                temp_list_count = 0;
                for i in temp_list:
                    temp_avg = i + temp_avg
                    temp_list_count = temp_list_count + 1
                temp_avg = temp_avg/temp_list_count
                if self.conversion_flag == 1:
                    temp_avg_f = temp_avg
                    temp_avg_f = temp_avg_f * 1.8
                    temp_avg_f = temp_avg_f + 32

                if (self.temp_count%8) == 0:
                    if self.conversion_flag == 1:
                        self.last_temp_label.setText('Last value: {} F'.format(round(temp,2)))                  
                        self.avg_temp_label.setText('Average: {} F'.format(round(temp_avg_f,2))) 
                        temp_f_high = self.conversion(max(temp_list))
                        temp_f_low = self.conversion(min(temp_list))
                        self.high_temp_label.setText('Highest: {} F'.format(round(temp_f_high,2)))    
                        self.low_temp_label.setText('Lowest: {} F'.format(round(temp_f_low,2)))  
                    else:
                        self.last_temp_label.setText('Last value: {} C'.format(round(temp,2)))
                        self.avg_temp_label.setText('Average: {} C'.format(round(temp_avg,2)))
                        self.high_temp_label.setText('Highest: {} C'.format(round(max(temp_list),2)))
                        self.low_temp_label.setText('Lowest: {} C'.format(round(min(temp_list),2)))
                    # print timestamp
                    self.last_temp_time.setText('Time: {}'.format(today))
                    self.avg_temp_time.setText('Time: {}'.format(today))
                    self.high_temp_time.setText('Time: {}'.format(today))
                    self.low_temp_time.setText('Time: {}'.format(today))
                global cur
                #insert values in data base
                insert_statement = "INSERT INTO temperatureDB (temperature, highest, lowest, average, last, timestamp) VALUES (%s, %s, %s, %s, %s, %s)"
                val = (temp, max(temp_list), min(temp_list), temp_avg, temp, today)
                cur.execute(insert_statement, val)
                db.commit()
                cur.execute("SELECT * FROM temperatureDB")
                db.commit()
                print(cur.rowcount, "record inserted.")
                        
        finally:
               self.temp_button = 0
               QTimer.singleShot(1000, self.get_temp)


    # Displays humidity values, allows user to enter threshold value and gives an alert accordingly
    def get_hum(self):
        try:
            time = QTime.currentTime()
            humidity,temp = sensor.read(sensor.DHT22, 4)
            if temp is None and humidity is None:
               self.hum_value.setText('ERROR')
            else:
                today = datetime.now().strftime("%H:%M:%S %Y-%m-%d")
                self.hum_count = self.hum_count + 1
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

                if self.hum_count is 8:
                    self.last_hum_label.setText('Last value: {} %'.format(round(humidity,2)))
                    self.avg_hum_label.setText('Average: {} %'.format(round(hum_avg,2)))
                    self.high_hum_label.setText('Highest: {} %'.format(round(max(hum_list),2)))
                    self.low_hum_label.setText('Lowest: {} %'.format(round(min(hum_list),2)))
                    self.last_hum_time.setText('Time: {}'.format(today))
                    self.avg_hum_time.setText('Time: {}'.format(today))
                    self.high_hum_time.setText('Time: {}'.format(today))
                    self.low_hum_time.setText('Time: {}'.format(today))

                global cur
                #insert values in data base
                insert_statement = "INSERT INTO humidityDB (humidity, highest, lowest, average, last, timestamp) VALUES (%s, %s, %s, %s, %s, %s)"
                val = (humidity, max(hum_list), min(hum_list), hum_avg, humidity, today)
                cur.execute(insert_statement, val)
                db.commit()
               # cur.execute("SELECT * FROM humdidityDB")

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
       http_server = tornado.httpserver.HTTPServer(application)
       http_server.bind(8888)
       http_server.start(0)
       myIP = socket.gethostbyname(socket.gethostname())
       print ('*** Websocket Server Started at %s***' % myIP)
       tornado.ioloop.IOLoop.instance().start()
       sys.exit(app.exec_())
    

