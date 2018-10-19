Name: Vipraja Patil
      Vipul Gupta

Installation instructions: run--> python3 project2.py
Dependencies:  
#install qt
#install matplotlib
#install mysql

Project Work: Created .ui files using QT GUI. Using these .ui files craeted a Python application for retrieving temperature and humidity values from DHT22 sensor which is interfaced with Rpi3 and displaying them. Mandatory features which have been implemented:

Request of current humidity/temperature values from the DHT22
Display the values as well as the time of the request
Handle not receiving data when requested (if sensor is disconnected)
References: https://stackoverflow.com/questions/11812000/login-dialog-pyqt https://ralsina.me/posts/BB974.html https://gist.github.com/pklaus/3e16982d952969eb8a9a#file-embedding_in_qt5-py-L14 https://www.youtube.com/watch?v=7SrD4l2o-uk

Project Additions:

A login screen to secure the application
Retrieve temp/hum values on a timer and display them. And also display these values using graph.
Calculate and display the average temp & hum
Allow user to set an alarm for an input high or low temperature or humidity value
Display temperature values in either Celsius and Fahreinheit
