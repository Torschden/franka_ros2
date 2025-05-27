import os

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution, LaunchConfiguration
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    # Arguments
    robot_ip_arg = DeclareLaunchArgument('robot_ip', default_value='0.0.0.0')
    use_fake_hardware_arg = DeclareLaunchArgument('use_fake_hardware', default_value='false')
    fake_sensor_commands_arg = DeclareLaunchArgument('fake_sensor_commands', default_value='false')

    # Launch Gazebo with robot
    gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('franka_gazebo_bringup'),
                'launch',
                'visualize_franka_robot.launch.py'
            ])
        ]),
        launch_arguments={
            'load_gripper': 'true',
            'franka_hand': 'franka_hand',
            'arm_id': 'fr3'
        }.items()
    )

    # Launch MoveIt (reuse your moveit.launch.py, but skip robot_state_publisher and joint_state_publisher)
    moveit_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('franka_fr3_moveit_config'),
                'launch',
                'moveit.launch.py'
            ])
        ]),
        launch_arguments={
            'robot_ip': LaunchConfiguration('robot_ip'),
            'use_fake_hardware': 'false',
            'fake_sensor_commands': 'false'
        }.items()
    )

    return LaunchDescription([
        robot_ip_arg,
        use_fake_hardware_arg,
        fake_sensor_commands_arg,
        gazebo_launch,
        moveit_launch,
    ])
