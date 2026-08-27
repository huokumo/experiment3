# experiment3

高职、专科层次机器人环境感知仿真实验工程。

## 环境前提

实验默认使用已经配置好的：

- Ubuntu 22.04
- ROS 2 Humble
- Gazebo Classic 11
- RViz2

本仓库不重复提供 Ubuntu、ROS 2 或 Gazebo 的安装步骤。开始实验前，请确认当前终端已经加载 ROS 2：

```bash
source /opt/ros/humble/setup.bash
```

## 工程说明

ROS 2 工作空间：

```text
~/experiment3_ws
```

课程功能包：

```text
experiment3
```

实验一使用 Gazebo Classic 室内差速移动机器人，包含仿真相机、Mid-360-like 三维点云和 IMU 数据链路，并通过 RViz 完成可视化检查和故障诊断。

## 编译

将本仓库放入工作空间的 `src/experiment3` 后执行：

```bash
cd ~/experiment3_ws
source /opt/ros/humble/setup.bash
colcon build --symlink-install --packages-select experiment3
source install/setup.bash
```

## 实验一

学生指导书位于：

```text
实验/实验1/仿真传感器安装配置与故障诊断.md
```

正常仿真：

```bash
ros2 launch experiment3 sim.launch.py
```

双故障仿真：

```bash
ros2 launch experiment3 sim_fault_double.launch.py
```

双故障版本同时模拟两个配置问题：激光雷达不发布 `/mid360/points`，以及机器人基座坐标系名称异常。请先按实验指导书记录现象，再修改故障版本并完成重新编译、重启和复测。

RViz 配置：

```bash
rviz2 -d ~/experiment3_ws/src/experiment3/config/experiment3.rviz
```

实际传感器话题：

```text
/camera/depth_camera/image_raw
/camera/depth_camera/camera_info
/mid360/points
/imu/data
```

## 目录约定

```text
experiment3/
├── launch/       # 正常和故障启动文件
├── urdf/         # 机器人与传感器模型
├── worlds/       # Gazebo 场景
├── config/       # RViz 和参数文件
└── 实验/          # 学生实验指导书
```

故障版本只用于教学诊断，不要覆盖正常模型和正常启动文件。
