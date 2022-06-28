import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt
from app_UI import Ui_MainWindow
from control import Control

"""
Слайдер и спин-бокс взаимосвязанны:
    При изменении значения слайдера изменяется значение спин-бокса и наоборот

:SERVO_SLIDER_MAX_VALUE: максимальное значение слайдера сервопривода
:SERVO_SLIDER_MIN_VALUE: минимальное значение слайдера сервопривода
:SERVO_SLIDER_SINGLE_STEP_VALUE: шаг изменения слайдера сервопривода

:SPEED_SLIDER_MAX_VALUE: максимальное значение слайдера управления двигателем
:SPEED_SLIDER_MIN_VALUE: минимальное значение слайдера управления двигателем
:SPEED_SLIDER_SINGLE_STEP_VALUE: шаг изменения слайдера управления двигателем

для поворотов:
    :LEFT_OFFSET: максимальное смещение сервопривода в левую сторону
    :RIGHT_OFFSET: максимальное смещение сервопривода в правую сторону

для движения:
    :FORWARD_OFFSET: максимальное смещение скорости
    :FORWARD_OFFSET: максимальное смещение скорости

ESC для выхода и закрытия программы
"""

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.SERVO_SLIDER_MAX_VALUE = 160
        self.SERVO_SLIDER_MIN_VALUE = 75
        self.SERVO_SLIDER_SINGLE_STEP_VALUE = 2

        self.SPEED_SLIDER_MAX_VALUE = 99
        self.SPEED_SLIDER_MIN_VALUE = -99
        self.SPEED_SLIDER_SINGLE_STEP_VALUE = 10

        self.LEFT_OFFSET = 35
        self.RIGHT_OFFSET = 50
        self.FORWARD_OFFSET = 99
        self.BACKWARD_OFFSET = -99
        self.DEFAULT_SERVO_SLIDER_POS = 110
        self.DEFAULT_SPEED_SLIDER_POS = 0

        # настройка слайдера управления сервоприводом
        self.servo_angle_slider.setMaximum(self.SERVO_SLIDER_MAX_VALUE)
        self.servo_angle_slider.setMinimum(self.SERVO_SLIDER_MIN_VALUE)
        self.servo_angle_slider.setSingleStep(self.SERVO_SLIDER_SINGLE_STEP_VALUE)

        # настройка спин-бокса управления сервоприводом
        self.servo_angle_spin_box.setMaximum(self.SERVO_SLIDER_MAX_VALUE)
        self.servo_angle_spin_box.setMinimum(self.SERVO_SLIDER_MIN_VALUE)
        self.servo_angle_spin_box.setSingleStep(self.SERVO_SLIDER_SINGLE_STEP_VALUE)

        # настройка слайдера управления скоростью и направлением двигателя
        self.speed_slider.setMaximum(self.SPEED_SLIDER_MAX_VALUE)
        self.speed_slider.setMinimum(self.SPEED_SLIDER_MIN_VALUE)
        self.speed_slider.setSingleStep(self.SPEED_SLIDER_SINGLE_STEP_VALUE)

        # настройка спин-бокса управления скоростью и направлением двигателя
        self.speed_spin_box.setMaximum(self.SPEED_SLIDER_MAX_VALUE)
        self.speed_spin_box.setMinimum(self.SPEED_SLIDER_MIN_VALUE)
        self.speed_spin_box.setSingleStep(self.SPEED_SLIDER_SINGLE_STEP_VALUE)

        # настройка логики работы и взаимодействия слайдеров и спин-боксов
        self.servo_angle_slider.valueChanged[int].connect(self.changed_servo_angle_event)
        self.speed_slider.valueChanged[int].connect(self.changed_speed_event)
        self.speed_slider.sliderReleased.connect(lambda: self.speed_slider.setSliderPosition(self.DEFAULT_SPEED_SLIDER_POS))
        self.servo_angle_slider.sliderReleased.connect(lambda: self.servo_angle_slider.setSliderPosition(self.DEFAULT_SERVO_SLIDER_POS))
        self.servo_angle_spin_box.valueChanged.connect(lambda: self.servo_angle_slider.setSliderPosition(self.servo_angle_spin_box.value()))
        self.speed_spin_box.valueChanged.connect(lambda: self.speed_slider.setSliderPosition(self.speed_spin_box.value()))
        self.speed_slider.setSliderPosition(self.DEFAULT_SPEED_SLIDER_POS)
        self.servo_angle_spin_box.setValue(self.DEFAULT_SERVO_SLIDER_POS)
        self.servo_angle_slider.setSliderPosition(self.DEFAULT_SERVO_SLIDER_POS)

    def keyPressEvent(self, event):
        """
        отслеживание нажатия клавиши
        
        для A и D:
            поворот колес влево и вправо
        для W и S:
            направление движения вперед и назад
        """
        key = event.key()
        if key == Qt.Key.Key_A and not event.isAutoRepeat():
            self.changed_servo_angle_event(self.servo_angle_slider.value() - self.LEFT_OFFSET)

        if key == Qt.Key.Key_D and not event.isAutoRepeat():
            self.changed_servo_angle_event(self.servo_angle_slider.value() + self.RIGHT_OFFSET)

        if key == Qt.Key.Key_W and not event.isAutoRepeat():
            self.changed_speed_event(self.FORWARD_OFFSET)

        if key == Qt.Key.Key_S and not event.isAutoRepeat():
            self.changed_speed_event(self.BACKWARD_OFFSET)

        elif key == Qt.Key.Key_Escape:
            self.close()

    def keyReleaseEvent(self, event):
        """
        отслеживание отпускания клавиши
        если клавиша была отпущена - вернуть дефолтные положения слайдеров и спинбоксов
        """
        key = event.key()
        if key == Qt.Key.Key_A and not event.isAutoRepeat():
            self.servo_angle_slider.setSliderPosition(self.DEFAULT_SERVO_SLIDER_POS)

        if key == Qt.Key.Key_D and not event.isAutoRepeat():
            self.servo_angle_slider.setSliderPosition(self.DEFAULT_SERVO_SLIDER_POS)

        if key == Qt.Key.Key_W and not event.isAutoRepeat():
            self.speed_slider.setSliderPosition(self.DEFAULT_SPEED_SLIDER_POS)

        if key == Qt.Key.Key_S and not event.isAutoRepeat():
            self.speed_slider.setSliderPosition(self.DEFAULT_SPEED_SLIDER_POS)

    def changed_servo_angle_event(self, angle_value):
        controller.change_angle_servo(angle_value)
        self.label.setText(f"Угол сервопривода -- {angle_value}°")
        self.servo_angle_spin_box.setValue(angle_value)

    def changed_speed_event(self, speed_value):
        self.label_2.setText(f"Скорость двигателя -- {speed_value}")
        self.speed_spin_box.setValue(speed_value)
        if speed_value < 0:
            controller.move_backward(abs(speed_value))
        controller.move_forward(speed_value)
    
if __name__ == "__main__":
    controller = Control()
    app = QApplication(sys.argv)
    demo = MainWindow()
    demo.show()

    sys.exit(app.exec_())