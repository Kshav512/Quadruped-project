import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from pynput import keyboard
import math

class point_to_point(Node):
    def __init__(self):
        super().__init__('point_to_point')
        self.publisher = self.create_publisher(String, 'Common_Topic', 10)
        self.target_angle1 = 90
        self.target_angle2 = 90
        self.angle1 = None
        self.angle2 = None
        self.X0 = -90.9
        self.Y0 = -100.0
        self.key = None
        self.X1 = -100.0
        self.Y1 = -160.0
        self.l1 = 100.0
        self.l2 = 90.9

        self.timer = self.create_timer(0.1, self.timer_callback)

        self.listner = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.listner.start()

        self.get_logger().info("Point to Point Node has been started.")

    def on_press(self, key):
            try:
                if key.char in ['a','d']:
                    self.key = key.char

            except AttributeError:
                pass

    def on_release(self, key):
            try:
                if key.char in ['a','d']:
                    self.key = None

            except AttributeError:
                pass

    def timer_callback(self):
        if self.key == 'a':
            self.target_angle1 = 90
            self.target_angle2 = 90
        elif self.key == 'd':
            step = 2
            r = math.sqrt(self.X1**2 + self.Y1**2)
            if r > self.l1 + self.l2 or r < abs(self.l1 - self.l2):
                self.get_logger().info("The point is unreachable.")
                return

            else:
                phi = math.degrees(math.atan(self.X1 / abs(self.Y1)))
                a = math.degrees(math.acos((self.l1**2 + r**2 - self.l2**2)/(2* self.l1 * r)))


                self.target_angle1 = int(round(90+ a + phi))
                '''if self.target_angle1 < self.angle1:
                    self.target_angle1 -= step
                elif self.target_angle1 > self.angle1:
                    self.target_angle1 += step'''

                self.target_angle2 = int(round(math.degrees(math.acos((self.l1**2 + self.l2**2 - r**2)/(2 * self.l1 * self.l2)))))

                '''if self.target_angle2 < self.angle2:
                    self.target_angle2 -= step
                elif self.target_angle2 > self.angle2:
                    self.target_angle2 -= step'''

        else:
            return


        msg = String()
        msg.data = f"{self.target_angle1},{self.target_angle2}"
        self.publisher.publish(msg)
        self.get_logger().info(f"Published angles: Servo 1:{self.target_angle1}, Servo 2:{self.target_angle2}")

def main(args=None):
    rclpy.init(args=args)
    node = point_to_point()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()


                
                