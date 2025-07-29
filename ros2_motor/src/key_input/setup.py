from setuptools import find_packages, setup

package_name = 'key_input'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools','std_msgs','pynput','pyserial'],
    zip_safe=True,
    maintainer='eds-spiderbyte-01',
    maintainer_email='eds-spiderbyte-01@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': ['Servo_Input = key_input.Servo_Input:main',
                            'Servo_Input_Subscriber = key_input.Servo_Input_Subscriber:main',
        ],
    },
)
