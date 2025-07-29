import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/eds-spiderbyte-01/ros2_motor/install/two_keys'
