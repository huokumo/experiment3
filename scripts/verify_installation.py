#!/usr/bin/env python3

import math
import sys
import time

import rclpy
from rclpy.duration import Duration
from rclpy.node import Node
from rclpy.time import Time
from tf2_ros import Buffer, TransformException, TransformListener


EXPECTED_TOPICS = {
    "/camera/image_raw": "sensor_msgs/msg/Image",
    "/camera/camera_info": "sensor_msgs/msg/CameraInfo",
    "/mid360/points": "sensor_msgs/msg/PointCloud2",
    "/imu/data": "sensor_msgs/msg/Imu",
}

EXPECTED_TRANSFORMS = {
    "camera_link": (0.38, 0.0, 0.68),
    "mid360_link": (0.0, 0.0, 0.68),
    "imu_link": (-0.28, 0.0, 0.59),
}


class InstallationVerifier(Node):
    def __init__(self):
        super().__init__("verify_installation")
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

    def wait_for_topics(self, timeout_seconds=15.0):
        deadline = time.monotonic() + timeout_seconds
        while time.monotonic() < deadline:
            rclpy.spin_once(self, timeout_sec=0.2)
            available = dict(self.get_topic_names_and_types())
            if all(
                topic in available and self.count_publishers(topic) > 0
                for topic in EXPECTED_TOPICS
            ):
                return available
        return dict(self.get_topic_names_and_types())

    def check_transform(self, child, expected, timeout_seconds=5.0):
        deadline = time.monotonic() + timeout_seconds
        while time.monotonic() < deadline:
            rclpy.spin_once(self, timeout_sec=0.1)
            try:
                transform = self.tf_buffer.lookup_transform(
                    "base_link", child, Time(), timeout=Duration(seconds=0.2)
                )
                translation = transform.transform.translation
                actual = (translation.x, translation.y, translation.z)
                error = math.sqrt(
                    sum((value - target) ** 2 for value, target in zip(actual, expected))
                )
                return error <= 0.02, actual
            except TransformException:
                continue
        return False, None


def report(passed, message):
    status = "PASS" if passed else "FAIL"
    print(f"[{status}] {message}")
    return int(passed)


def main():
    rclpy.init()
    verifier = InstallationVerifier()
    passed = 0
    total = len(EXPECTED_TOPICS) + len(EXPECTED_TRANSFORMS)

    try:
        topics = verifier.wait_for_topics()
        for topic, expected_type in EXPECTED_TOPICS.items():
            actual_types = topics.get(topic, [])
            publisher_count = verifier.count_publishers(topic)
            passed += report(
                expected_type in actual_types and publisher_count > 0,
                f"{topic} publishes {expected_type} ({publisher_count} publisher(s))",
            )

        for child, expected in EXPECTED_TRANSFORMS.items():
            transform_ok, actual = verifier.check_transform(child, expected)
            if actual is None:
                detail = "transform is unavailable"
            else:
                detail = "translation=({:.3f}, {:.3f}, {:.3f})".format(*actual)
            passed += report(
                transform_ok,
                f"base_link -> {child}: {detail}",
            )
    finally:
        verifier.destroy_node()
        rclpy.shutdown()

    print(f"\nResult: {passed}/{total} passed")
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
