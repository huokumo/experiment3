from pathlib import Path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    package_dir = Path(get_package_share_directory("experiment3"))
    gazebo_launch = Path(get_package_share_directory("gazebo_ros")) / "launch" / "gazebo.launch.py"
    world = package_dir / "worlds" / "indoor_mapping.world"
    robot_xacro = package_dir / "urdf" / "differential_robot_fault_double.urdf.xacro"

    enable_camera = LaunchConfiguration("enable_camera")
    enable_lidar = LaunchConfiguration("enable_lidar")
    robot_description = Command([
        "xacro ", str(robot_xacro),
        " enable_camera:=", enable_camera,
        " enable_lidar:=", enable_lidar,
    ])

    return LaunchDescription([
        DeclareLaunchArgument(
            "enable_camera",
            default_value="true",
            description="Enable the Gazebo camera sensor; set false on headless servers.",
        ),
        DeclareLaunchArgument(
            "enable_lidar",
            default_value="false",
            description="Enable the Gazebo Mid-360 ray sensor.",
        ),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(str(gazebo_launch)),
            launch_arguments={"world": str(world), "verbose": "false"}.items(),
        ),
        Node(
            package="robot_state_publisher",
            executable="robot_state_publisher",
            name="robot_state_publisher",
            parameters=[{"robot_description": robot_description, "use_sim_time": True}],
            output="screen",
        ),
        Node(
            package="gazebo_ros",
            executable="spawn_entity.py",
            name="spawn_diffbot",
            arguments=["-topic", "robot_description", "-entity", "diffbot", "-x", "0", "-y", "0", "-z", "0.15"],
            output="screen",
        ),
    ])
