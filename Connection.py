from socket import *
import base64
import numpy as np
from PIL import Image
from io import BytesIO
import cv2

class Connector:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client = socket(AF_INET, SOCK_STREAM)
        self.count = 0
        server_address = (host, port)
        self.client.settimeout(3)
        self.client.connect(server_address)
        self.client.settimeout(None)
        self.client.sendall('connection successful'.encode())
        self.client.sendall('   done   '.encode())

    def sendMessage(self, message, frame1):
        #self.client.sendall(message.encode())
        self.count +=1
        #self.client.sendall(str(self.count).encode())


        #im = Image.fromarray(np.uint8(cm.gist_earth(frame1)*255))
        frame1 = cv2.resize(frame1, dsize=(400,200), interpolation=cv2.INTER_CUBIC)
        frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)
        im = Image.fromarray(np.uint8(frame1))
        buffered = BytesIO()
        im.save(buffered, format="JPEG")
        encoded_string = base64.b64encode(buffered.getvalue())
        #encoded_string = base64.b64encode(frame1)
        self.client.sendall(encoded_string)

        self.client.sendall(bytearray("   done   ".encode()))
        #img = Image.fromarray(frame1, 'RGB')
        #encoded_string = base64.b64encode(img.read())
        #self.client.sendall(encoded_string)


