# experiment3

ROS 2 Humble and Gazebo Classic lab for installing and configuring simulated
camera, 3D lidar, and IMU sensors on a differential-drive robot.

The repository has one learning path and one robot model. The initial model
contains only the mobile base. Students edit the same Xacro file and install
the three sensors in sequence by calling ready-made macros.

## Environment

- Ubuntu 22.04
- ROS 2 Humble
- Gazebo Classic 11
- RViz2
- VS Code (`code` command)

Workspace used by the course image:

```text
/root/exp3/experiment3_ws
```

Package directory:

```text
/root/exp3/experiment3_ws/src/experiment3
```

## Build

```bash
cd /root/exp3/experiment3_ws
source /opt/ros/humble/setup.bash

rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install --packages-select experiment3
source install/setup.bash
```

## Open the project in VS Code

```bash
cd /root/exp3/experiment3_ws/src/experiment3
code .
```

When VS Code refuses to run as root, use:

```bash
code . --no-sandbox --user-data-dir=/root/.vscode-root
```

All student edits are made in:

```text
urdf/differential_robot.urdf.xacro
```

Do not edit `robot_base_macro.xacro` or `sensor_macros.xacro` during the lab.

## Initial state

Start the base robot before installing sensors:

```bash
source /opt/ros/humble/setup.bash
source /root/exp3/experiment3_ws/install/setup.bash
ros2 launch experiment3 sim.launch.py
```

Gazebo should show the mobile robot and indoor world. Sensor topics are absent
because no sensor macro has been called yet.

## Step 1: Install the camera

Add the following block below the `STEP 1` comment in
`differential_robot.urdf.xacro`:

```xml
<xacro:install_camera
  parent="base_link"
  frame="camera_link"
  optical_frame="camera_optical_frame"
  xyz="0.38 0 0.68"
  rpy="0 0 0"
  image_topic="/camera/image_raw"
  info_topic="/camera/camera_info"
  update_rate="10.0"/>
```

Expected topics:

```text
/camera/image_raw
/camera/camera_info
```

## Step 2: Install the 3D lidar

Add the following block below the `STEP 2` comment:

```xml
<xacro:install_lidar
  parent="base_link"
  frame="mid360_link"
  xyz="0 0 0.68"
  rpy="0 0 0"
  topic="/mid360/points"
  update_rate="10.0"/>
```

Expected topic:

```text
/mid360/points
```

The teaching model uses 360 horizontal samples and 16 vertical channels at
10 Hz. This keeps the point cloud three-dimensional while remaining practical
on a classroom virtual machine.

## Step 3: Install the IMU

Add the following block below the `STEP 3` comment:

```xml
<xacro:install_imu
  parent="base_link"
  frame="imu_link"
  xyz="-0.28 0 0.59"
  rpy="0 0 0"
  topic="/imu/data"
  update_rate="100.0"/>
```

Expected topic:

```text
/imu/data
```

## Rebuild and restart after each step

Stop Gazebo with `Ctrl+C`, then run:

```bash
cd /root/exp3/experiment3_ws
source /opt/ros/humble/setup.bash
colcon build --symlink-install --packages-select experiment3
source install/setup.bash
ros2 launch experiment3 sim.launch.py
```

## Visual verification

After installing all three sensors, start RViz in another terminal:

```bash
source /opt/ros/humble/setup.bash
source /root/exp3/experiment3_ws/install/setup.bash
rviz2 -d /root/exp3/experiment3_ws/src/experiment3/config/experiment3.rviz
```

The configuration uses:

```text
Fixed Frame: base_link
PointCloud2: /mid360/points
Image: /camera/image_raw
```

## Automatic acceptance check

Keep Gazebo running, then execute in another terminal:

```bash
source /opt/ros/humble/setup.bash
source /root/exp3/experiment3_ws/install/setup.bash
ros2 run experiment3 verify_installation.py
```

The check verifies four standard topics and three sensor transforms. A complete
installation reports:

```text
Result: 7/7 passed
```

## Files students should understand

```text
urdf/differential_robot.urdf.xacro  # one file edited during the lab
urdf/robot_base_macro.xacro         # ready-made mobile base
urdf/sensor_macros.xacro            # ready-made sensor templates
launch/sim.launch.py                # one launch entry point
config/experiment3.rviz             # ready-made visualization
scripts/verify_installation.py      # final automatic check
worlds/indoor_mapping.world         # indoor simulation world
```
