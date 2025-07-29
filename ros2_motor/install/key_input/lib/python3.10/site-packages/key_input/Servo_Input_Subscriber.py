import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32
import serial
import time

class Communicator(Node):
    def __init__(self):
        super().__init__('Servo_Input_Subscriber')

        # Serial setup
        self.ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
        time.sleep(2)

        # ROS topic subscription
        self.subscription = self.create_subscription(
            Int32,
            'motor_input',
            self.listener_callback,
            10
        )

        self.get_logger().info("Subscriber initialized and listening on 'motor_input'...")

        # Optional heartbeat
        self.create_timer(2.0, self.heartbeat)

    def listener_callback(self, msg):
        self.get_logger().info(f"Received angle: {msg.data}")
        self.ser.write(f"{msg.data}\n".encode())

    def heartbeat(self):
        self.get_logger().info("Subscriber node alive...")

def main(args=None):
    rclpy.init(args=args)
    node = Communicator()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
