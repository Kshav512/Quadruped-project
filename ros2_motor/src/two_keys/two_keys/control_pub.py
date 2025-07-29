import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32
from pynput import keyboard
import time

class ConPub(Node):
    def __init__(self):
        super().__init__('control_pub')

        self.publisher = self.create_publisher(Int32, 'control', 10)
        self.angle = 0
        self.key = None

        self.timer = self.create_timer(0.1, self.zeit)
        listner = keyboard.Listener(on_press = self.on_press, on_release= self.on_release)
        listner.start()

    def on_press(self, key):
        try:
            if key.char in ['a', 'd']:
                self.key = key.char
        except AttributeError:
            pass

    def on_release(self, key):
        try:
            if key.char in ['a', 'd']:
                self.key = None
        except AttributeError:
            pass

    def zeit(self):
        if self.key == 'a':
            if self.angle < 180:
                self.angle += 10
            else:
                self.key = None
    
        elif self.key == 'd':
            if self.angle > 0:
                self.angle -= 10
            else:
                self.key = None
        else:
            return
        
        msg = Int32()
        msg.data = self.angle
        self.publisher.publish(msg)
        self.get_logger().info(f'Publishing Angle: {self.angle}')

def main(args=None):
    rclpy.init(args=args)
    node = ConPub()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

