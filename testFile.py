import math

x1=100
y1=100
x2=50
y2=100
dx = x2-x1
dy = (y2-y1)*-1
print("dx: ", dx,"\tdy: ", dy, "\n")
length = (dx**2 +dy**2)**0.5
cos_angle = dx/length
sin_angle = dy/length
angle = math.degrees(math.acos(cos_angle))
if(dy<0):
    angle*=-1
print("cos a = ", cos_angle, "\tsin a =", sin_angle)
print("angle = ", angle)


# x+=speed*cos_angle
# y+=speed*sin_angle