from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QComboBox, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap
import requests
from datetime import datetime
from pprint import pprint




class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings()
        self.create_widjets()
        self.put_widjets()
        self.show()

    def settings(self):
        self.setWindowTitle("Weather")
        self.setGeometry(200, 150, 400, 400)

    def create_widjets(self):
        self.lb_city = QLabel("Оберіть місто")
        self.lb_city.setStyleSheet("""
            QLabel {
                color: #ffffff;
                font-size: 30px;                
            } 
        """)
        self.combo_city= QComboBox()
        self.combo_city.addItems(["Київ", "Львів", "Харків"])
        self.combo_city.setStyleSheet("""
            QComboBox {
                padding: 10px;
                background-color: #954a56;
                border: 1px solid black;
            }                                                   
            """)
        self.combo_city.currentIndexChanged.connect(self.get_weather)
        self.btn_upd_weather = QPushButton("Оновити дані")
        self.btn_upd_weather.setStyleSheet("""
            QPushButton {
                background-color: #ffffff;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background-color: rgb(103, 135, 71);
            }
        """)
        self.btn_upd_weather.clicked.connect(self.get_weather)
        self.weather_info = QLabel("+20")
        self.lb_icon = QLabel()
        self.upd_time = QLabel("last time")

    def put_widjets(self):
        self.central_widget = QWidget()
        self.central_widget.setStyleSheet("background-color: #a98841;")
        self.setCentralWidget(self.central_widget)
        main_v_line = QVBoxLayout()
        main_v_line.addWidget(self.lb_city)
        main_v_line.addWidget(self.combo_city)
        main_v_line.addWidget(self.btn_upd_weather)
        main_v_line.addWidget(self.weather_info)
        main_v_line.addWidget(self.lb_icon)
        main_v_line.addWidget(self.upd_time)

        self.central_widget.setLayout(main_v_line)

    def get_weather(self): 
        api_key = 'f81703c1f3b81ad93e6644153c4a426e'
        city = self.combo_city.currentText()
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'

        response = requests.get(url)
        data_dict = response.json()
        pprint(data_dict)
        if data_dict['cod'] == 200:
            weather = data_dict['weather'][0]["description"]
            temp = data_dict["main"]["temp"]
            humidity = data_dict["main"]["humidity"]
            wind_speed = data_dict["wind"]["speed"]
            icon_name = data_dict["weather"][0]["icon"]
            url_icon = f'http://openweathermap.org/img/w/{icon_name}.png'
            
            result = f'weather: {weather}\ntemp: {temp}celsium\nhumidity: {humidity}%\nwind speed: {wind_speed}m/s'
            self.weather_info.setText(result)

            pix_map = QPixmap()
            pix_map.loadFromData(requests.get(url_icon).content)
            self.lb_icon.setPixmap(pix_map)

            start_time = datetime.now()
            time_str = start_time.strftime("%d/%m/%Y, %H:%M:%S")
            self.upd_time.setText(time_str)
            
            
        else:
            self.weather_info.setText("Site Error")
            



if __name__ == "__main__":
    app = QApplication([])
    window = Window()
    app.exec_()