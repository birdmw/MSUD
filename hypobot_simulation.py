import pygame, sys, math, io
from pygame.locals import *

pygame.init()
screen=pygame.display.set_mode((960,960),0,32)
colorCan=(139,137,137) #RGB
colorWood=(160,82,45) #RGB
radius=33
x1,y1,x2,y2 = 0,0,0,0
blocks = [(273,235,34,34),(960-34,183,34,34),(253,591,34,34),(755,723,34,34)]
circles = [(180,880),(470,590),(480,120)]
radius = 33
firstTimeFlag = 1


def drawBackground():
        screen=pygame.display.set_mode((960,960),0,32)
#-------------------------------------------------------------#
#       uncomment drawObjects() to see objects                #
#-------------------------------------------------------------#
        drawObjects()

def drawObjects():
        screen.lock()
        for block in blocks:
            pygame.draw.rect(screen, colorWood, block)
        for circle in circles:
            pygame.draw.circle(screen, colorCan, circle, radius)
        screen.unlock()
        pygame.display.update()

def patchArray(localArray):
    #fix edge behavior
    if localArray[0]>1.3*localArray[1]:
        localArray[0]=localArray[1]
    if localArray[180]>1.3*localArray[179]:
        localArray[180]=localArray[179]
    #fix lines that run through objects
    for i in range(2,178):
        if localArray[i-1]>1.5*localArray[i] and localArray[i+1]>1.5*localArray[i]:
            localArray[i] = (localArray[i-1]+localArray[i+1])/2
    return localArray

def circleDetection(heading):
    array=range(181)
    #phi is the sensor angle relative to the bot
    for phi in range(181):
           r = 600
           angle = heading+90-phi
           h = math.tan(math.pi / 180 * (angle+90))
           h = math.tan(math.pi / 180 * (angle+90))
           if (not h==0) and (not h**2+1==0):
            for circle in circles:
                a = circle[0]
                b = circle[1]
                k = y1+x1/h-b
                try:
                    #Generate collisions IR sensor should expect to see. One positive and one negative for both sides of the circle.
                    x_intercept1 = ((-math.sqrt(-(a**2)*(h**2)+2*a*(h**3)*k+(h**4)*-(k**2)+(h**4)*(radius**2)+(h**2)*(radius**2)))+a*(h**2)+h*k)/(h**2+1)
                    x_intercept2 = (( math.sqrt(-(a**2)*(h**2)+2*a*(h**3)*k+(h**4)*-(k**2)+(h**4)*(radius**2)+(h**2)*(radius**2)))+a*(h**2)+h*k)/(h**2+1)
                    y_intercept1 =(-x_intercept1/h+y1+x1/h)
                    y_intercept2 =(-x_intercept2/h+y1+x1/h)
                    #Use only the shortest distance.
                    if math.hypot(x1-x_intercept1,y1-y_intercept1)<math.hypot(x1-x_intercept2,y1-y_intercept2):
                        x_intercept = x_intercept1
                        y_intercept = y_intercept1
                    elif math.hypot(x1-x_intercept1,y1-y_intercept1)>math.hypot(x1-x_intercept2,y1-y_intercept2):
                        x_intercept = x_intercept2
                        y_intercept = y_intercept2
                    #Remove the back side of the rays (the part behind the sensor)
                    if (heading+90 > 180/math.pi*math.atan2(y_intercept-y1, x_intercept-x1) > heading-90):
                        r=min(math.hypot(x1-x_intercept,y1-y_intercept),r)
                    elif (heading+90+360 > 180/math.pi*math.atan2(y_intercept-y1, x_intercept-x1) > heading-90+360):
                        r=min(math.hypot(x1-x_intercept,y1-y_intercept),r)
                    elif (heading+90-360 > 180/math.pi*math.atan2(y_intercept-y1, x_intercept-x1) > heading-90-360):
                        r=min(math.hypot(x1-x_intercept,y1-y_intercept),r)
                #exception executes when there are no collisions
                except:
                    r=r
           #store radius into array
           array[phi]=r

    #patch up array
    array = patchArray(array)
    return array

def squareDetection(array,heading):
        for phi in range(181):
            slope = math.tan(math.pi / 180 * (heading+90-phi))
            #y1=slope*x1+b1, so b1=y1-slope*x1
            b1 = y1-slope*x1
            #blocks = [(920,210,40,40),(272,272,40,40),(239,602,40,40),(747,747,40,40)]
            for square in blocks:
                #xl means x of the blocks left side (t is top, r is right, b is bottom)
                xr = square[0]
                yt = square[1]
                xl = square[0]+square[2]
                yb = square[1]+square[3]
                #yline means y of the line, xl is x is the line

                yline=slope*xl+b1
                if yb>yline>yt:
                    #collision at xb,yline
                    if (heading+90 > 180/math.pi*math.atan2(yline-y1, xl-x1) > heading-90):
                        array[phi]= min(array[phi],math.hypot(x1-xl,y1-yline))
                    elif (heading+90+360 > 180/math.pi*math.atan2(yline-y1, xl-x1) > heading-90+360):
                        array[phi]= min(array[phi],math.hypot(x1-xl,y1-yline))
                    elif (heading+90-360 > 180/math.pi*math.atan2(yline-y1, xl-x1) > heading-90-360):
                        array[phi]= min(array[phi],math.hypot(x1-xl,y1-yline))
                yline=slope*xr+b1
                if yb>yline>yt:
                    #collision at xb,yline
                    if (heading+90 > 180/math.pi*math.atan2(yline-y1, xr-x1) > heading-90):
                        array[phi]= min(array[phi],math.hypot(x1-xr,y1-yline))
                    elif (heading+90+360 > 180/math.pi*math.atan2(yline-y1, xr-x1) > heading-90+360):
                        array[phi]= min(array[phi],math.hypot(x1-xr,y1-yline))
                    elif (heading+90-360 > 180/math.pi*math.atan2(yline-y1, xr-x1) > heading-90-360):
                        array[phi]= min(array[phi],math.hypot(x1-xr,y1-yline))

                if slope==0:
                    slope=.01

                xline = (yb-b1)/slope
                if xl>xline>xr:
                    if (heading+90 > 180/math.pi*math.atan2(yb-y1, xline-x1) > heading-90):
                        array[phi]= min(array[phi],math.hypot(x1-xline,y1-yb))
                    if (heading+90+360 > 180/math.pi*math.atan2(yb-y1, xline-x1) > heading-90+360):
                        array[phi]= min(array[phi],math.hypot(x1-xline,y1-yb))
                    if (heading+90-360 > 180/math.pi*math.atan2(yb-y1, xline-x1) > heading-90-360):
                        array[phi]= min(array[phi],math.hypot(x1-xline,y1-yb))

                xline = (yt-b1)/slope
                if xl>xline>xr:
                    if (heading+90 > 180/math.pi*math.atan2(yt-y1, xline-x1) > heading-90):
                        array[phi]= min(array[phi],math.hypot(x1-xline,y1-yt))
                    if (heading+90+360 > 180/math.pi*math.atan2(yt-y1, xline-x1) > heading-90+360):
                        array[phi]= min(array[phi],math.hypot(x1-xline,y1-yt))
                    if (heading+90-360 > 180/math.pi*math.atan2(yt-y1, xline-x1) > heading-90-360):
                        array[phi]= min(array[phi],math.hypot(x1-xline,y1-yt))
        array = patchArray(array)
        return array



def drawHypobotRays(heading):
        array=range(181)
        array=circleDetection(heading)
        array=squareDetection(array,heading)
        #draw lines
        for index in range(181):
            pygame.draw.line(screen, (50,255,50), (x1,y1),(x1+array[index]*math.cos(math.pi/180*(heading+90-index)),y1+array[index]*math.sin(math.pi/180*(heading+90-index))), 1)

        #draw robot
        pygame.draw.line(screen, (255,255,255), (x1,y1), (x1+50*(x2-x1)/hypot, y1+50*(y2-y1)/hypot), 3)
        pygame.draw.circle(screen, (255,255,255), (x1,y1), 15)
        pygame.display.update()

while True:
    if firstTimeFlag==1:
        drawBackground()
        firstTimeFlag=0

    for event in pygame.event.get():
        if event.type==QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                x1,y1 = pygame.mouse.get_pos()
        if event.type == MOUSEBUTTONUP:
            if event.button == 1:
                x2,y2 = pygame.mouse.get_pos()
                hypot=math.hypot(x2-x1,y2-y1)
                heading = 180 / math.pi * math.atan2((y2-y1),(x2-x1))
                if not hypot == 0:
                    drawBackground()
                    drawHypobotRays(heading)


