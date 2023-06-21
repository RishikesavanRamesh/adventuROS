
import os
import sys

# Add the base path of the project to the Python path
base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_path)


import unittest
import time
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from py_pubsub.subscriber_member_function import MinimalSubscriber

class TestMinimalSubscriber(unittest.TestCase):
    def setUp(self):
        rclpy.init()

    def tearDown(self):
        rclpy.shutdown()

    def test_subscription(self):
        received_messages = []

        def listener_callback(msg):
            received_messages.append(msg.data)

        minimal_subscriber = MinimalSubscriber()
        minimal_subscriber.create_subscription(
            String, 'topic', listener_callback, 10)

        # Create a publisher to publish test messages
        publisher_node = Node('minimal_publisher')
        publisher = publisher_node.create_publisher(String, 'topic', 10)

        # Publish a test message
        test_message = 'Test Message'
        msg = String()
        msg.data = test_message

        timeout_sec = 5  # Set a timeout of 5 seconds
        start_time = time.time()

        while time.time() - start_time < timeout_sec:
            # Publish the test message
            publisher.publish(msg)

            # Spin the subscription once
            rclpy.spin_once(minimal_subscriber)

            # Check if the message has been received
            if received_messages:
                break

        # Clean up
        minimal_subscriber.destroy_node()
        publisher_node.destroy_node()

        # Assert the received message
        self.assertEqual(received_messages, ['Test Message'])

if __name__ == '__main__':
    unittest.main()
