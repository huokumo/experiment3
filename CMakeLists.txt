cmake_minimum_required(VERSION 3.8)
project(experiment3)

find_package(ament_cmake REQUIRED)

install(
  DIRECTORY
    config
    launch
    urdf
    worlds
  DESTINATION share/${PROJECT_NAME}
)

install(
  PROGRAMS
    scripts/verify_installation.py
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()
