import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32

class ServoPublisher(Node):
    def __init__(self):
        super().__init__('servo_publisher')
        self.publisher_ = self.create_publisher(Int32, 'servo_angle', 10)
        self.timer = self.create_timer(1.0, self.publish_angle)
        self.angle = 90

    def publish_angle(self):
        msg = Int32()
        msg.data = self.angle
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing: {msg.data}')
        self.angle = (self.angle + 30) % 180

def main(args=None):
    rclpy.init(args=args)
    node = ServoPublisher()
    rclpy.spin(node)
    rclpy.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()



