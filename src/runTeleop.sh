# Starts the keyboard controller and pipes message to topic /autocar/cmd_vel
ros2 run keyboard_controller keyboard_controller speed:=3 turn:=250 cmd_vel:=/autocar/cmd_vel
