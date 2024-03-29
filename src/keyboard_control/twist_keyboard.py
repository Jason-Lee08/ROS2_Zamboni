import sys

import geometry_msgs.msg
import rclpy

if sys.platform == 'win32':
    import msvcrt
else:
    import termios
    import tty

import time


msg = """
This node takes keypresses from the keyboard and publishes them
as Twist messages. It works best with a US keyboard layout.
---------------------------
Moving around:
   u    i    o
   j    k    l
   m    ,    .
For Holonomic mode (strafing), hold down the shift key:
---------------------------
   U    I    O
   J    K    L
   M    <    >
t : up (+z)
b : down (-z)
anything else : stop
q/z : increase/decrease max speeds by 10%
w/x : increase/decrease only linear speed by 10%
e/c : increase/decrease only angular speed by 10%
CTRL-C to quit
"""

moveBindings = {
    'i': (1, 0, 0, 0),
    'o': (1, 0, 0, -1),
    'j': (0, 0, 0, 1),
    'l': (0, 0, 0, -1),
    'u': (1, 0, 0, 1),
    ',': (-1, 0, 0, 0),
    '.': (-1, 0, 0, 1),
    'm': (-1, 0, 0, -1),
    'O': (1, -1, 0, 0),
    'I': (1, 0, 0, 0),
    'J': (0, 1, 0, 0),
    'L': (0, -1, 0, 0),
    'U': (1, 1, 0, 0),
    '<': (-1, 0, 0, 0),
    '>': (-1, -1, 0, 0),
    'M': (-1, 1, 0, 0),
    't': (0, 0, 1, 0),
    'b': (0, 0, -1, 0),
}

speedBindings = {
    'q': (1.1, 1.1),
    'z': (.9, .9),
    'w': (1.1, 1),
    'x': (.9, 1),
    'e': (1, 1.1),
    'c': (1, .9),
}


def getKey(settings):
    if sys.platform == 'win32':
        # getwch() returns a string on Windows
        key = msvcrt.getwch()
    else:
        tty.setraw(sys.stdin.fileno())
        # sys.stdin.read() returns a string on Linux
        key = sys.stdin.read(1)
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key


def saveTerminalSettings():
    if sys.platform == 'win32':
        return None
    return termios.tcgetattr(sys.stdin)


def restoreTerminalSettings(old_settings):
    if sys.platform == 'win32':
        return
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)


def vels(speed, turn):
    return 'currently:\tspeed %s\tturn %s ' % (speed, turn)

def main():
    speed = 6.9
    turn = 5.0
    for arg in sys.argv:
        print(arg)
        if arg.startswith("speed:="):
            speed = float(arg.split(":=")[1])
            print('new speed: ', speed)
        
        if arg.startswith("turn:="):
            turn = float(arg.split(":=")[1])
            print('new turn: ', turn)

        if arg.startswith("cmd_vel:="):
            cmd_vel = str(arg.split(":=")[1])
            print('new cmd_vel: ', cmd_vel)
        else:
            cmd_vel = "cmd_vel"

    settings = saveTerminalSettings()

    rclpy.init()

    node = rclpy.create_node('teleop_twist_keyboard')
    pub = node.create_publisher(geometry_msgs.msg.Twist, cmd_vel, 10)

    STEP_DELAY = 0.25
    x = 0.0
    y = 0.0
    z = 0.0
    th = 0.0
    status = 0.0
    lastKey = 'artbitrary_placeholder'
    moveBinding = False

    #try:
    print(msg)
    print(vels(speed, turn))
    while True:
        key = getKey(settings)
        if key in moveBindings.keys():
            x = moveBindings[key][0]
            y = moveBindings[key][1]
            z = moveBindings[key][2]
            th = moveBindings[key][3]
            moveBinding = True
        elif key in speedBindings.keys():
            speed = speed * speedBindings[key][0]
            turn = turn * speedBindings[key][1]

            print(vels(speed, turn))
            if (status == 14):
                print(msg)
            status = (status + 1) % 15
            moveBinding = False
        else:
            x = 0.0
            y = 0.0
            z = 0.0
            th = 0.0
            if (key == '\x03'):
                break
            moveBinding = False
        
        # if key != lastKey or not moveBinding:
        #     for s in range(0, 6, 1):
        #         step = s / 5
        #         twist = geometry_msgs.msg.Twist()
        #         twist.linear.x = x * speed * step
        #         twist.linear.y = y * speed * step
        #         twist.linear.z = z * speed * step
        #         twist.angular.x = 0.0
        #         twist.angular.y = 0.0
        #         twist.angular.z = th * turn * step
        #         pub.publish(twist)
        #         time.sleep(STEP_DELAY)

        #         print(twist.linear.x, x, speed, step)

        twist = geometry_msgs.msg.Twist()
        twist.linear.x = x * speed
        twist.linear.y = y * speed
        twist.linear.z = z * speed 
        twist.angular.x = 0.0
        twist.angular.y = 0.0
        twist.angular.z = th * turn
        pub.publish(twist)

        #lastKey = key
            

    # except Exception as e:
    #     print(e)

    # finally:
    #     twist = geometry_msgs.msg.Twist()
    #     twist.linear.x = 0.0
    #     twist.linear.y = 0.0
    #     twist.linear.z = 0.0
    #     twist.angular.x = 0.0
    #     twist.angular.y = 0.0
    #     twist.angular.z = 0.0
    #     pub.publish(twist)

    #     restoreTerminalSettings(settings)


if __name__ == '__main__':
    main()