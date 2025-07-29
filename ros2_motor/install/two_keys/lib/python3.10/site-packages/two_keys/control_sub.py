import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32
import serial

class ConSub(Node):
    def __init__(self):
        super().__init__('control_sub')
        self.subcscription = self.create_subscription(Int32, 'control', self.listener_callback, 10)
        self.subcscription
        self.ser = serial.Serial('/dev/ttyACM0',9600, timeout=1)

    def listener_callback(self, msg):
        self.get_logger().info(f'Recieved Angle: {msg.data}')
        self.ser.write(f"{msg.data}\n".encode())

def main(args=None):
    rclpy.init(args=args)
    node = ConSub()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

def destroy_node(self):
    if self.ser and self.ser.is_open:
        self.ser.close()
    super().destroy_node()

if __name__ == '__main__':
    main()

"""import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32
import serial

class ConSub(Node):
    def __init__(self):
        super().__init__('control_sub')
        self.subscription = self.create_subscription(
            Int32,
            'control',
            self.listener_callback,
            10
        )
        try:
            self.ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
            self.get_logger().info('Serial port /dev/ttyACM1 opened successfully.')
        except serial.SerialException as e:
            self.get_logger().error(f"Could not open serial port: {e}")
            self.ser = None

    def listener_callback(self, msg):
        self.get_logger().info(f'Received Angle: {msg.data}')
        if self.ser and self.ser.is_open:
            try:
                self.ser.write(f"{msg.data}\n".encode())
            except serial.SerialException as e:
                self.get_logger().error(f"Serial write failed: {e}")
        else:
            self.get_logger().error("Serial port not open.")

    def destroy_node(self):
        if self.ser and self.ser.is_open:
            self.ser.close()
            self.get_logger().info('Serial port closed.')
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)
    node = ConSub()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()"""

