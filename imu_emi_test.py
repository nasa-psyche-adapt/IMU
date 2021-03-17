import time
import psutil
import matplotlib.pyplot as plt
import time
import board
import busio
import adafruit_icm20x
i2c = busio.I2C(board.SCL, board.SDA)
icm = adafruit_icm20x.ICM20948(i2c)
# type of plot
plt.rcParams['animation.html'] = 'jshtml'
fig = plt.figure()
#p1 = fig.add_subplot(311)               # plot 1
#p2 = fig.add_subplot(312)               # plot 2
#p3 = fig.add_subplot(313)               # plot 3
p = fig.add_subplot(111)                 # plot
fig.show()
i = 0
x = []
a1, a2, a3 = [], [], []                 # for storing accelerometer data
v1, v2, v3 = [], [], []                 # for storing gyro data
h1, h2, h3 = [], [], []                 # for storing magnetometer data
k = 0
while True:
    x.append(i)
    #y.append(psutil.cpu_percent())
    #a.x, a.y, a.z = icm.acceleration
    #v.x, v.y, v.z = icm.gyro
    #h.x, h.y, h.z = icm.magnetic
    ax, ay, az = icm.acceleration[:]    # unpack accelerometer tuple
    vx, vy, vz = icm.gyro[:]            # unpack gyro tuple
    hx, hy, hz = icm.magnetic[:]        # unpack magnetometer tuple
    # store linear acceleration (m/s^2) x,y,z (accelerometer)
    a1.append(ax)
    a2.append(ay)
    a3.append(az)
    # store angular velocity (rad/s) x,y,z (gyro)
    v1.append(vx)
    v2.append(vy)
    v3.append(vz)
    # store magnetic field (uT) x,y,z (magnetometer)    
    h1.append(hx)
    h2.append(hy)
    h3.append(hz)
    # subplot 1
    #p1.plot(x, a1, color='r')
    #p1.plot(x, a2, color='g')
    #p1.plot(x, a3, color='b')
    # subplot 2
    #p2.plot(x, v1, color='r')
    #p2.plot(x, v2, color='g')
    #p2.plot(x, v3, color='b')
    # subplot 3
    #p3.plot(x, h1, color='r')
    #p3.plot(x, h2, color='g')
    #p3.plot(x, h3, color='b')
    # plot
    p.plot(x, h1, color='r', linewidth=0.5, label="mag-x")
    p.plot(x, h2, color='g', linewidth=0.5, label="mag-y")
    p.plot(x, h3, color='b', linewidth=0.5, label="mag-z")
    # fix for repeating legends printing
    if k == 0:
        p.legend(loc='upper right')
        k = 1
    fig.canvas.draw()
    #p1.set_xlim(left=max(0, i-50), right=i+50)
    #p2.set_xlim(left=max(0, i-50), right=i+50)
    #p3.set_xlim(left=max(0, i-50), right=i+50)
    p.set_xlim(left=max(0, i-30), right=i+30)
    plt.title("IMU EMI Testing")
    plt.xlabel("Sample Number")
    plt.ylabel("Magnetic Field (uT)")
    time.sleep(0.1)
    i += 1
plt.close()