import cv2

def helper():
    print('called the collision helper')


def findSafestDirection(frame, originalFrame, test):
    width = frame.shape[1]
    height = frame.shape[0]

    i1 = 0
    j1 = 0
    maxValue = 0
    for i in range(2, width-2):
        for j in range(2, height-2):
            if frame[j][i] > maxValue:
                maxValue = frame[j][i]
                i1 = i
                j1 = j
    print('max i: ' + str(i1) + ', max j: ' + str(j1) + ', maxValue: ' + str(maxValue))

    if test:
        print('test')
        #cv2.circle(originalFrame, (i1*16, j1*16), 10, (255, 0, 0), 5)
        frame = cv2.resize(frame, (height*16, width*16))
        cv2.circle(frame, (i1*16, j1*16), 10, (255, 0, 0), 5)
        cv2.imshow('h', frame)
        cv2.waitKey(0)

    print(maxValue)
    if maxValue < 0.25:
        print('no viable path')
        print(maxValue)
        return 'stop'

    #determine how to get there
    if i1 > (width/2 + width*0.1):
        print('right')
    elif i1 < (width/2 - width*0.1):
        print('left')
    else: print('no x axis changes required')

    if j1 > (height/2 + height*0.1):
        print('down')
    elif j1 < (height/2 - height*0.1):
        print('up')
    else: print('no y axis changes required')

def findClosestSafeDirection(frame):
    #Need a threshold
    pass

def findClosestSpotToOriginal(frame, directionDesired):
    pass
