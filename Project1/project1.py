import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
import Adafruit_DHT as sensor

class project1(QDialog):
    def __init__(self):
        super(project1,self).__init__()
        loadUi('project1.ui',self)
        self.setWindowTitle('EID project 1')
        time = QTime.currentTime()
        self.refresh_temp.clicked.connect(self.temp_refresh_clicked)
        self.refresh_hum.clicked.connect(self.humidity_refresh_clicked)

    @pyqtSlot()
    def get_temp(self):
         try:
            time = QTime.currentTime()
            timeout = 1;
            humidity,temp = sensor.read(sensor.DHT22, 4)
            if temp is None and humidity is None:
               self.temp_value.setText('ERROR')
            else:
               self.temp_value.setText('{} C'.format(round(temp,4)))
            self.temp_time.setText(time.toString(Qt.DefaultLocaleLongDate))
         finally:
            QTimer.singleShot(5000, self.get_temp)

    def get_hum(self):
        try:
            time = QTime.currentTime()
            humidity,temp = sensor.read(sensor.DHT22, 4)
            if temp is None and humidity is None:
               self.hum_value.setText('ERROR')
            else:
               self.hum_value.setText('{} %'.format(round(humidity,4)))
            self.hum_time.setText(time.toString(Qt.DefaultLocaleLongDate))
        finally:
            QTimer.singleShot(5000, self.get_hum)

    def temp_refresh_clicked(self):
        time = QTime.currentTime()
        self.get_temp()
       # self.list_temp.addItems(round(temp,2))
       # list_temp.addItem(temp_item)

    def humidity_refresh_clicked(self):
        time = QTime.currentTime()
        self.get_hum()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = project1()
    widget.show()
    sys.exit(app.exec_())
