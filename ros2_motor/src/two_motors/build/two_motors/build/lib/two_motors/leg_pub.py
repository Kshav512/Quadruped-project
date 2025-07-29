import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32
from std_msgs.msg import String
from pynput import keyboard

class LegInput(Node):
    def __init__(self):
        super().__init__('leg_pub')

        self.publisher = self.create_publisher(String, 'Leg_Control', 10)
        self.angle1 = 90
        self.angle2 = 90
        self.key = None

        self.timer = self.create_timer(0.05, self.leg_mover)
        Horer = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        Horer.start()
        self.get_logger().info("Leg Control Node Started")

    def on_press(self,key):
        try:
            if key.char in ['a', 'd', 'j','l']:
                self.key = key.char
        except AttributeError:
            pass

    def on_release(self, key):
        try:
            if key.char in ['a', 'd', 'j','l']:
                self.key = None
        except AttributeError:
            pass

    def leg_mover(self):
        if self.key == 'a':
            if self.angle1 < 180:
                self.angle1 += 5
            else:
                self.key = None

        elif self.key == 'd':
            if self.angle1 > 0:
                self.angle1 -= 5
            else:
                self.key = None
            
        elif self.key == 'j':
            if self.angle2 < 180:
                self.angle2 += 5
            else:
                self.key = None

        elif self.key == 'l':
            if self.angle2 > 0:
                self.angle2 -= 5
            else:
                self.key = None
        else:
            return
        

        msg = String()
        msg.data = f"{self.angle1},{self.angle2}"
        self.publisher.publish(msg)
        self.get_logger().info(f"Publishing: Servo1 = {self.angle1}, Servo2 = {self.angle2}")

def main(args=None):
    rclpy.init(args=args)
    node = LegInput()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()        

