# Reads data from the serial monitor without interrupting the main thread

from serial import Serial, serialutil
import time
from threading import Thread


class SerialListener:
    def __init__(self, baudrate=9600, timeout=0.5):
        try:
            self.ser = Serial('/dev/ttyACM0', baudrate, timeout=timeout)
        except serialutil.SerialException:
            try:
                self.ser = Serial('/dev/ttyACM1', baudrate, timeout=timeout)
            except serialutil.SerialException:
                try:
                    self.ser = Serial('/dev/ttyACM2', baudrate, timeout=timeout)
                except serialutil.SerialException:
                    self.ser = Serial('/dev/ttyACM2', baudrate, timeout=timeout)

        self.stopped = False
        self.paused = False
        self.stream = ''
        time.sleep(1)  # Wait for serial buffer to reset

    def start(self):
        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        while True:
            if not self.paused:
                if self.stopped:
                    self.ser.close()
                    self.paused = True
                try:
                    self.stream = self.ser.readline().decode('utf-8')
                except:
                    self.stream = self.ser.readline().decode('ascii')
                self.stream = self.stream.rstrip()

    def stop(self):
        self.paused = False
        self.stopped = True

    def resume(self):
        self.paused = False

    def pause(self):
        self.paused = True()

    def read(self):
        return self.stream

    def write(self, msg):
        self.ser.write(msg.encode())
