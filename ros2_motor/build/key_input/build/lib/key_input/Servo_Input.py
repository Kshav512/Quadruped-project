import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32
from pynput import keyboard
import time

class Input(Node):
    def __init__(self):
        super().__init__('Servo_Input')
        self.publisher = self.create_publisher(Int32, 'motor_input', 10)
        self.angle = 0
        self.direction = 3
        self.pressed = False
        time_period = 0.1
        self.timer = self.create_timer(time_period, self.timer_callback)

        listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        listener.start()

    def on_press(self,key):
        if key == keyboard.Key.left:
            self.pressed = True

    def on_release(self,key):
        if key == keyboard.Key.left:
            self.pressed = False
    

    def timer_callback(self):
        self.move_motor()

    def move_motor(self):
        if self.pressed:
            self.angle += self.direction
            if self.angle >= 180:
                self.angle = 180
                self.direction = -10
            elif self.angle <= 0:
                self.angle = 0
                self.direction = 10


        self.publisher.publish(Int32(data=self.angle))
        self.get_logger().info(f"Publishing angle: {self.angle}")
        
        
def main(args=None):
    rclpy.init(args=args)
    input_node = Input()
    rclpy.spin(input_node)
    input_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()