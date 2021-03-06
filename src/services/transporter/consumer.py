import time
import zmq
import random
import json

class Transporter:
    def __init__(self,address,port,mode):
        self.addr = "tcp://" + address + ":" + port;
        self.mode = mode;

    def createTransporter(self):
        context = zmq.Context();
        flag = True
        if self.mode == "send":
            self.transporter = context.socket(zmq.PUSH)
            self.transporter.bind(self.addr)
        elif self.mode == "receive":
            self.transporter = context.socket(zmq.PULL)
            self.transporter.connect(self.addr)
        else:
            print("mode is not properly set")
            flag = False

        return flag


# receive work
transporter = Transporter("0.0.0.0","9998","receive");#.transporter
transporter.createTransporter();
i = 0
while True:
    work = transporter.transporter.recv_json()
    print work

    # send()
