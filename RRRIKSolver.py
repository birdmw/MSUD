#!/usr/bin/python
import math

resolution = 0.0174532925 #seeded resolution, any will work
a1=5.0 #arm length (change these)
a2=5.0
necessaryDistance = 0.1 #IK ends when within this range of the solution (in units of arm length)
currentDistance = 0.0 #this is just a global declaration

Xnow = 0.0
Ynow = 0.0
Znow = 0.0
Xlast = 0.0
Ylast = 0.0
Zlast = 0.0

Xdest=0 #destination coordinates (change these)
Ydest=0
Zdest=10

theta1=0.0 #input angles (starting point of arm)
theta2=0.0
theta3=0.0

angle1=0.0
angle2=0.0
angle3=0.0

dx=1.0 #these are just global placeholders (don't change these)
dy=1.0
dz=1.0
travel = 0.0
passes = 0

def performFK(theta1, theta2, theta3, dimension):
    global dx, dy, dz
    if dimension == 'x':
        dx=(a1*math.cos(theta1)*math.cos(theta2)+a2*math.cos(theta1)*math.cos(theta2+theta3))
        return dx
    elif dimension == 'y':
        dy=(a1*math.cos(theta2)*math.sin(theta1)+a2*math.sin(theta1)*math.cos(theta2+theta3))
        return dy
    elif dimension == 'z':
        dz=(a1*math.sin(theta2)+a2*math.sin(theta2+theta3))
        return dz

def distance(a,b,c,d,e,f):
    return math.sqrt((d-a)*(d-a)+(e-b)*(e-b)+(f-c)*(f-c))

def tryAllPossabilities(resolution):
    global angle1, angle2, angle3, Xnow, Ynow, Znow, theta1, theta2, theta3, travel, currentDistance, Xlast, Ylast, Zlast, dx, dy, dz
    currentDistance=distance(Xdest,Ydest,Zdest, performFK(theta1, theta2, theta3, 'x'), performFK(theta1, theta2, theta3, 'y'), performFK(theta1, theta2, theta3, 'z'))
    for i in range(-1,2):
        for j in range(-1,2):
            for k in range(-1,2):
                newDistance = distance (Xdest, Ydest, Zdest, performFK(theta1+i*resolution, theta2+j*resolution, theta3+k*resolution, 'x'), performFK(theta1+i*resolution, theta2+j*resolution, theta3+k*resolution, 'y'),  performFK(theta1+i*resolution, theta2+j*resolution, theta3+k*resolution, 'z'))
                

                if i==j==k==0:
                    Xlast=dx
                    Ylast=dy
                    Zlast=dz
                elif newDistance <= currentDistance:
                    currentDistance = newDistance
                    angle1=theta1+i*resolution
                    angle2=theta2+j*resolution
                    angle3=theta3+k*resolution
                    Xnow=dx
                    Ynow=dy
                    Znow=dz
    theta1=angle1
    theta2=angle2
    theta3=angle3
   # print "xyz=%f %f %f" % (Xnow, Ynow, Znow)
    travel = distance (Xlast,Ylast,Zlast,Xnow,Ynow,Znow)

def main():
    global resolution, currentDistance, passes, Xlast, Ylast, Zlast
    currentDistance=distance(Xdest,Ydest,Zdest, performFK(theta1, theta2, theta3, 'x'), performFK(theta1, theta2, theta3, 'y'), performFK(theta1, theta2, theta3, 'z'))
    while currentDistance > necessaryDistance:
        # print "%f %f %f %f %f %f %f %f" % (Xnow, Ynow, Znow, Xlast, Ylast, Zlast, currentDistance, resolution)
        tryAllPossabilities(resolution)
       # print "distance=%f, resolution=%f, coords=%f, %f, %f " % (currentDistance, resolution,dx,dy,dz)

        passes = passes+1
       
        if resolution ==0:
                        resolution = 0.01
        if travel==0:
           
            resolution = resolution/2
          #  print "Zero Travel Occured"
        else:
          #  print "resolution is %f distance is %f" % (resolution, currentDistance)
            resolution = resolution * (currentDistance/travel)
    return
       
    
main()

while theta1>3.14159265:
    theta1=theta1-6.28318531
while theta1<-3.14159265:
    theta1=theta1+6.28318531
while theta2>3.14159265:
    theta1=theta1-6.28318531
while theta2<-3.14159265:
    theta1=theta1+6.28318531
while theta3>3.14159265:
    theta1=theta1-6.28318531
while theta3<-3.14159265:
    theta1=theta1+6.28318531
    

print "Theta1 = %f degrees, Theta2 = %f degrees, Theta3 = %f degrees" % (theta1*57.2957795, theta2*57.2957795, theta3*57.2957795)
print "Final X,Y,Z are %f %f %f" % (Xnow, Ynow, Znow)
print "Done in %d passes" % (passes)
