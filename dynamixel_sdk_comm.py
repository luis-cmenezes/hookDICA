#!/usr/bin/env python3

import time, getpass
from pynput.keyboard import Key, Listener
from dynamixel_sdk import *

BAUDRATE = 1000000

DEVICENAME = '/dev/ttyUSB0'

PROTOCOL_1_INFOS =  {'TORQUE_ADDR': 24, 'LED_ADDR': 25 , 'GOAL_POS_ADDR': 30, 'SPEED_ADDR': 32}

SPEED = (110).to_bytes(2, byteorder='little')
POS_INCREMENT = 30

MAP_INPUT_TO_MOTOR = [['w','s'],['d','e'],['f','r'],['g','t'],['y','h'],['u','j']]
MIN_MAX = [[0,1023],[120,890],[10,1000],[200,810],[0,1023],[500,850]]

class u2d2Control():

    def __init__(self):        
        self.startComm()

        self.enableTorque() 

        self.motorsCurrentPosition = [512,415,785,721,512,512]

        self.positionGroup = GroupSyncWrite(self.portHandler, self.packetHandler, PROTOCOL_1_INFOS['GOAL_POS_ADDR'], 2)  
        self.velocityGroup = GroupSyncWrite(self.portHandler, self.packetHandler, PROTOCOL_1_INFOS['SPEED_ADDR'], 2)  

        for motor_id in range(6):
            self.velocityGroup.addParam(motor_id, SPEED)

        self.velocityGroup.txPacket()
        self.data2motors()

    def startComm(self):
        self.portHandler = PortHandler(DEVICENAME)

        # Open port
        try:
            self.portHandler.openPort()
            print("Succeeded to open the port")
        except:
            print("Failed to open the port")
            quit()

        # Set port baudrate
        try:
            self.portHandler.setBaudRate(BAUDRATE)
            print("Succeeded to change the baudrate")
        except:
            print("Failed to change the baudrate")
            quit()
        
        self.packetHandler = PacketHandler(1.0)

    def enableTorque(self):
        
        for _ in range(3):
            
            for motor_id in range(6):
                
                self.packetHandler.write1ByteTxOnly(self.portHandler, motor_id, PROTOCOL_1_INFOS['TORQUE_ADDR'], True)
                self.packetHandler.write1ByteTxOnly(self.portHandler, motor_id, PROTOCOL_1_INFOS['LED_ADDR'], True)

    def data2motors(self):

        self.positionGroup.clearParam()

        for motor_id in range(6):
            value = self.motorsCurrentPosition[motor_id]

            bytes_value = value.to_bytes(2, byteorder='little')

            self.positionGroup.addParam(motor_id, bytes_value)

        self.positionGroup.txPacket()

    def on_press(self, key):
        try:

            if key.char == '0':
                self.motorsCurrentPosition = [512,415,785,721,512,512]
                self.data2motors()
                return

            for l_id, inputs in enumerate(MAP_INPUT_TO_MOTOR):
                if key.char in inputs:
                    motor_id = l_id
                    direction = -1 if inputs.index(key.char) else 1

                    self.motorsCurrentPosition[motor_id] += direction*POS_INCREMENT
                    self.motorsCurrentPosition[motor_id] = max(self.motorsCurrentPosition[motor_id], MIN_MAX[motor_id][0])
                    self.motorsCurrentPosition[motor_id] = min(self.motorsCurrentPosition[motor_id], MIN_MAX[motor_id][1])

                    self.data2motors()

                    break
            
        except AttributeError:
            print(f'Tecla especial pressionada: {key}')     

        return
        
    def run(self):
        with Listener(on_press=self.on_press) as listener:
            getpass.getpass("")
            listener.join()

if __name__ == '__main__':

    u2d2 = u2d2Control()
    u2d2.run()