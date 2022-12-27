import os
import subprocess

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument, ExecuteProcess, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():

    navpkg = 'autocar_nav'
    gzpkg = 'autocar_gazebo'
    descpkg = 'autocar_description'

    # set the world
    world = os.path.join(get_package_share_directory(gzpkg), 'worlds', 'ice_rink.world')
    urdf = os.path.join(get_package_share_directory(descpkg),'urdf', 'autocar.xacro')
    rviz = os.path.join(get_package_share_directory(descpkg), 'rviz', 'view2.rviz')
    
    navconfig = os.path.join(get_package_share_directory(navpkg), 'config', 'navigation_params.yaml')

    use_sim_time = LaunchConfiguration('use_sim_time', default='True')

    subprocess.run(['killall', 'gzserver'])
    subprocess.run(['killall', 'gzclient'])

    # zed = Node(
    #         package='zed_wrapper',
    #         executable='zed.launch.py',
    #         name='rviz2',
    #         output={'both': 'log'}
    #     )
    RTABMap = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([
                    FindPackageShare("rtabmap_ros"), '/launch', '/rtabmap.launch.py']),
                launch_arguments={'use_sim_time': use_sim_time,
                "rgb_topic":"/depth_camera/image_raw", 
                "depth_topic":"/depth_camera/depth/image_raw",
                "camera_info_topic":"/depth_camera/camera_info",
                "odom_topic":"/autocar/odom",
                "frame_id":"base_link", 
                "approx_sync":"true", 
                "wait_imu_to_init":"true", 
                "imu_topic":"/imu/data",
                "visual_odometry":"false",
                "qos":"2"}.items()
            )

    return LaunchDescription([
        SetEnvironmentVariable(
            'RCUTILS_CONSOLE_OUTPUT_FORMAT', '[{severity}]: {message}'
        ),

        SetEnvironmentVariable(
            'RCUTILS_COLORIZED_OUTPUT', '1'
        ),

        ExecuteProcess(
            cmd=['gazebo', world, 'libgazebo_ros_factory'],
        ),

        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use simulation (Gazebo) clock if true'
        ),

        Node(
            package='robot_state_publisher',
            name='robot_state_publisher',
            executable='robot_state_publisher',
            output={'both': 'log'},
            parameters=[{'use_sim_time': use_sim_time}],
            arguments=[urdf]
        ),
        
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            arguments=['-d', rviz],
            output={'both': 'log'}
        ),
        RTABMap
        # Node(
        #     package = navpkg,
        #     name = 'localisation',
        #     executable = 'localisation.py',
        #     parameters = [navconfig]
        # )
    ])

def main():

    generate_launch_description()

if __name__ == '__main__':
    main()
