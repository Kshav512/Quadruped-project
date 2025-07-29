import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32
import serial
import time

class ServoSubscriber(Node):
    def __init__(self):
        super().__init__('servo_subscriber')
        self.subcribtion = self.create_subscription(Int32,'servo_angle',self.listener_callback,10)
        
        serial_port = "/dev/ttyACM0"
        self.ser = serial.Serial(serial_port,9600,timeout = 1)
        time.sleep(2)

    def listener_callback(self, msg):
        self.get_logger().info(f"Recieved angle: {msg.data}")
        self.ser.write(f"{msg.data}\n".encode())
def main(args=None):
    rclpy.init(args=args)
    node = ServoSubscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
    
