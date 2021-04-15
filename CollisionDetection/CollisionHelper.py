import cv2

def helper():
    print('called the collision helper')


def findSafestDirection(frame, originalFrame, scaleFactor, debug):
    shift = int(scaleFactor/2)
    height = frame.shape[0]
    width = frame.shape[1]

    maxValue = 0
    if debug: frame1 = cv2.resize(frame, (width*scaleFactor, height*scaleFactor))
    for i in range(2, height-2):
        for j in range(1, width-1):
            if debug: cv2.circle(frame1, (j*scaleFactor + shift, i*scaleFactor + shift), 8, (frame[i][j]*1, 0, 0), 5)
            if frame[i][j] > maxValue:
                maxValue = frame[i][j]
                x = j
                y = i

    directionFromPoint(x, y, width, height, shift, maxValue)

    if debug:
        cv2.imshow('h', frame1)
        cv2.circle(frame1, (x*scaleFactor + shift, y*scaleFactor + shift), 8, (1, 0, 0), 5)
        cv2.imshow('j', frame1)
        cv2.waitKey(0)

def directionFromPoint(x, y, width, height, shift, maxValue):
    shift = shift/32
    if maxValue < 0.25:
        print('no viable path')
        print(maxValue)
        return 'stop'

    #determine how to get there
    if (x+shift) > (width/2 + width*0.1):
        print('right')
    elif (x+shift) < (width/2 - width*0.1):
        print('left')
    else: print('no x axis changes required')

    if (y+shift) > (height/2 + height*0.1):
        print('down')
    elif (y+shift) < (height/2 - height*0.1):
        print('up')
    else: print('no y axis changes required')

def findClosestSafeDirection(frame):
    #Need a threshold
    pass

def findClosestSpotToOriginal(frame, directionDesired):
    pass
