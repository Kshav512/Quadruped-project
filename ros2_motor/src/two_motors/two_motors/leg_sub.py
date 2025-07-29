import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import serial

class LegOutput(Node):
    def __init__(self):
        super().__init__('leg_sub')

        self.subscription = self.create_subscription(String, 'Leg_Control', self.listner_callback, 10)
        self.subscription
        
        try:
            self.ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
            self.get_logger().info("Serial connection established")
        except Exception as e:
            self.get_logger().error(f"Failed to establish serial connection: {e}")
            self.ser = None

    def listner_callback(self,msg):
        self.get_logger().info(f'Recieved: {msg.data}')

        if self.ser:
            try:
                self.ser.write((msg.data +'\n').encode())
            except Exception as e:
                self.get_logger().error(f"Failed to write to serial: {e}")

def main(args=None):
    rclpy.init(args=args)
    node = LegOutput()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()


