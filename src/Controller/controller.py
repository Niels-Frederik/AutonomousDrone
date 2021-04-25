
class Controller():
    def __init__(self, debug):
        self.debug = debug
        self.defaultText = 'Drone control: '

    def stop(self):
        self.printToUser('stop')

    def takeoff(self):
        self.printToUser('takeoff')

    def land(self):
        self.printToUser('land')

    def rotateLeft(self):
        self.printToUser('rotate left')

    def rotateRight(self):
        self.printToUser('rotate right')

    def moveForward(self):
        self.printToUser('move forward')

    def moveBackward(self):
        self.printToUser('move backwards')

    def moveLeft(self):
        self.printToUser('move left')

    def moveRight(self):
        self.printToUser('move right')

    def printToUser(self, action):
        if self.debug:
            print(self.defaultText + action)
