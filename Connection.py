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
        self.server_address = (host, port)
        self.udpClient = socket(AF_INET, SOCK_DGRAM)
        self.udpClient.settimeout(1)
        #self.udpClient.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        print('testasdhadkjhsdkjhad')
        self.count = 0
        #self.tcpClient = socket(AF_INET, SOCK_STREAM)
        #self.tcpClient.settimeout(3)
        #self.tcpClient.connect(self.server_address)
        #self.tcpClient.settimeout(None)
        #self.tcpClient.sendall('connection successful'.encode())
        #self.tcpClient.sendall('   done   '.encode())


    def sendMessage(self, message, frame1):
        #im = Image.fromarray(np.uint8(cm.gist_earth(frame1)*255))
        frame1 = cv2.resize(frame1, dsize=(400,200), interpolation=cv2.INTER_CUBIC)
        frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)
        im = Image.fromarray(np.uint8(frame1))
        buffered = BytesIO()
        im.save(buffered, format="JPEG")
        encoded_string = base64.b64encode(buffered.getvalue())
        #encoded_string = base64.b64encode(frame1)


        #self.sendTcpMessage(message, encoded_string)
        self.sendUdpMessage(message, encoded_string)


    def sendTcpMessage(self, message, encoded_string):
        #self.tcpClient.sendall(message.encode())
        self.count +=1
        #self.tcpClient.sendall(str(self.count).encode())


        self.tcpClient.sendall(encoded_string)

        self.tcpClient.sendall(bytearray("   done   ".encode()))
        #img = Image.fromarray(frame1, 'RGB')
        #encoded_string = base64.b64encode(img.read())
        #self.client.sendall(encoded_string)


    def sendUdpMessage(self, message, encoded_string):
        print('sending message to ' + self.server_address[0] + ' ' + str(self.server_address[1]))
        self.count = self.count+1
        print(str(self.count))
        self.udpClient.sendto(encoded_string, self.server_address)
        #self.udpClient.sendto(b'hej' , ("127.0.0.1", 15003))
