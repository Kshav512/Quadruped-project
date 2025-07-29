import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import math
from pynput import keyboard

class Loop_equation(Node):
    def __init__(self):
        super().__init__('equa')
        self.publisher = self.create_publisher(String, 'Common_Topic', 10)
        self.X0 = 0
        self.Y0 = -100
        self.key = None
        self.l1 = 100
        self.l2 = 90.9
        self.X1 = self.X0
        self.Y1 = self.Y0
        self.step = 4
        self.angle1 = None
        self.angle2 = None
        self.radius = 30.0

        self.timer = self.create_timer(0.1, self.callback)

        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.listener.start()

    def on_press(self, key):
        try: 
            if key.char in ['a','d','h']:
                self.key = key.char
        except AttributeError:
            pass

    def on_release(self, key):
        try:
            if key.char in ['a','d','h']:
                self.key = None
        except AttributeError:
            pass

    def callback(self):
        if self.key == 'h':
            self.X1 = self.X0 + self.radius
            self.Y1 = self.Y0

        elif self.key == 'a':
            if self.X1 > 0:
                self.Y1 -= self.step
                self.X1 = math.sqrt(self.radius**2 - (self.Y1 - self.Y0)**2) + self.X0
            elif self.X1 < 0:
                self.Y1 += self.step
                self.X1 = -math.sqrt(self.radius**2 - (self.Y1 - self.Y0)**2) + self.X0
            elif self.X1 == 0 and self.Y1 < self.Y0:
                self.Y1 += self.step
                self.X1 = -math.sqrt(self.radius**2 - (self.Y1 - self.Y0)**2) + self.X0
            elif self.X1 == 0 and self.Y1 > self.Y0:
                self.Y1 -= self.step
                self.X1 = math.sqrt(self.radius**2 - (self.Y1 - self.Y0)**2) + self.X0


        elif self.key == 'd':
            self.Y1 += self.step
            self.X1 = math.sqrt(self.radius**2 - (self.Y1 - self.Y0)**2) + self.X0

        else:
            return
        
        r = round(math.sqrt(self.X1**2 + self.Y1**2),2)

        if r > self.l1 + self.l2 or r < abs(self.l1 - self.l2):
            self.get_logger().info('Point is unreachable.')
            return
        else:
            phi = math.degrees(math.atan(self.X1/abs(self.Y1)))

            a = math.degrees(math.acos((self.l1**2 + r**2 - self.l2**2)/(2*self.l1*r)))

            b = math.degrees(math.acos((self.l1**2 + self.l2**2 - r**2)/(2*self.l1*self.l2)))

            self.angle1 = int(round(90 + phi + a))
            self.angle2 = int(round(b))


        msg = String()
        msg.data = f"{self.angle1},{self.angle2}"
        self.publisher.publish(msg)
        self.get_logger().info(f"Published angles: Servo 1:{self.angle1}, Servo 2:{self.angle2}")
        self.get_logger().info(f"X: {self.X1}, Y: {self.Y1}")

def main(args=None):
    rclpy.init(args=args)
    node = Loop_equation()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()    