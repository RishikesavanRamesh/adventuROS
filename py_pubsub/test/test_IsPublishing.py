import os
import sys
import unittest
import rclpy
from std_msgs.msg import String
from py_pubsub.publisher_member_function import MinimalPublisher

# Add the base path of the project to the Python path
base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_path)


class TestMinimalPublisher(unittest.TestCase):
    def setUp(self):
        rclpy.init()

    def tearDown(self):
        rclpy.shutdown()

    def test_publishing(self):
        minimal_publisher = MinimalPublisher()

        received_messages = []

        def callback(msg):
            received_messages.append(msg.data)

        minimal_publisher.create_subscription(
            String, 'topic', callback, 10)

        # Publish a test message
        test_message = 'Test Message'
        msg = String()
        msg.data = test_message
        minimal_publisher.publisher_.publish(msg)

        # Wait for the message to be received
        rclpy.spin_once(minimal_publisher)

        # Assert the received message
        self.assertEqual(received_messages, [test_message])


if __name__ == '__main__':
    unittest.main()
