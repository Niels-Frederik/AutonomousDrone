import cv2

def helper():
    print('called the collision helper')


def findSafestDirection(frame, originalFrame, test):
    height = frame.shape[0]
    width = frame.shape[1]

    x = 0
    y = 0
    maxValue = 0
    frame1 = cv2.resize(frame, (width*16, height*16))
    for i in range(3, height-3):
        for j in range(1, width-1):
            cv2.circle(frame1, (j*16, i*16), 8, (frame[i][j]*1, 0, 0), 5)
            if frame[i][j] > maxValue:
                maxValue = frame[i][j]
                x = j
                y = i
    print('max x: ' + str(x) + ', max y: ' + str(y) + ', maxValue: ' + str(maxValue))


    print(maxValue)
    if maxValue < 0.25:
        print('no viable path')
        print(maxValue)
        return 'stop'

    directionFromPoint (x, y, width, height)

    if test:
        #cv2.circle(originalFrame, (i1*16, j1*16), 10, (255, 0, 0), 5)
        #cv2.circle(frame, (x*16, y*16), 10, (255, 0, 0), 5)
        #cv2.circle(frame, (j1*16, i1*16), 10, (255, 0, 0), 5)
        #cv2.circle(frame, (height*16, j1*16), 10, (255, 0, 0), 5)
        cv2.imshow('h', frame1)
        cv2.circle(frame1, (x*16, y*16), 8, (1, 0, 0), 5)
        cv2.imshow('j', frame1)
        cv2.waitKey(0)


def directionFromPoint(x, y, width, height):
    #determine how to get there
    if x > (width/2 + width*0.1):
        print('right')
    elif x < (width/2 - width*0.1):
        print('left')
    else: print('no x axis changes required')

    if y > (height/2 + height*0.1):
        print('down')
    elif y < (height/2 - height*0.1):
        print('up')
    else: print('no y axis changes required')

def findClosestSafeDirection(frame):
    #Need a threshold
    pass

def findClosestSpotToOriginal(frame, directionDesired):
    pass
