import unittest
from gradescope_utils.autograder_utils.decorators import weight, visibility
import subprocess32 as subprocess
import random
import socket
import time


class TestServerSession(unittest.TestCase):
    server_status = None

    @classmethod
    def setUpClass(cls):
        """
        Start the server once before all tests
        """
        cls.server_port = random.randint(32768, 61000)
        try:
            cls.server_process = subprocess.Popen(
                ["/autograder/source/server/tcp_server", str(cls.server_port)], stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            # Wait for the server to be ready
            cls.wait_for_server_start(cls.server_port)
        except Exception as e:
            cls.server_process = None
            cls.server_status = False
            print("Error starting the server:", e)

    @classmethod
    def wait_for_server_start(cls, port, timeout=5):
        """
        Wait for the server to start by attempting to connect to it.
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.connect(("localhost", port))
                    # set a class variable to indicate the server is running
                    cls.server_status = True
                    return True
            except socket.error:
                time.sleep(0.2)  # Wait a bit before trying again

        # If the server did not start, set the class variable to indicate the server is not running
        cls.server_status = False
        return False

    @classmethod
    def tearDownClass(cls):
        """
        Stop the server after all tests
        """
        if cls.server_process:
            cls.server_process.terminate()
            cls.server_process.wait()

    def send_command(self, command):
        """Helper method to send a command to the server and return the response."""
        if not self.server_status:
            self.fail("Server did not start")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(("localhost", self.server_port))
            command_line = f"{command}\n\0"  # Ensure command ends with \n\0
            s.sendall(command_line.encode())
            data = s.recv(256)
            # Strip the trailing newline and null characters if present
            return data.decode().rstrip('\n\0')

    @weight(10)  # Assigns a score weight to this test
    @visibility("visible")  # Makes the test result visible to students
    def test_multiple_commands(self):
        """Test that the server can handle multiple commands in one session."""
        if not self.server_status:
            self.fail("Server did not start")
        # Use the helper method to send 'help' command and read the response
        help_response = self.send_command("help")
        self.assertIn("Available commands:", help_response, "The 'help' response should list available commands.")

        # Use the helper method to send 'calc 2+3' command and check the response
        calc_response = self.send_command("calc 2+3")
        self.assertEqual("5", calc_response, "The 'calc 2+3' response should be '5'.")

        # Example: Test 'sort' command
        sort_response = self.send_command("sort 3 2 1")
        self.assertEqual("1 2 3", sort_response, "The 'sort 3 2 1' response should be '1 2 3'.")

        # Test 'calc' with subtraction
        calc_sub_response = self.send_command("calc 5-3")
        self.assertEqual("2", calc_sub_response, "The 'calc 5-3' response should be '2'.")

        # Test 'calc' with multiplication
        calc_mul_response = self.send_command("calc 2*4")
        self.assertEqual("8", calc_mul_response, "The 'calc 2*4' response should be '8'.")

        # Test 'calc' with division
        calc_div_response = self.send_command("calc 8/4")
        self.assertEqual("2", calc_div_response, "The 'calc 8/4' response should be '2'.")

        # Test 'help' with specific command (e.g., 'calc')
        help_calc_response = self.send_command("help calc")
        self.assertTrue("usage: calc" in help_calc_response.lower(), "'help calc' should mention usage.")

        # Add any additional commands you wish to test here, following the same pattern

        # Assert their responses as needed, using either assertEqual or assertIn


if __name__ == "__main__":
    unittest.main()