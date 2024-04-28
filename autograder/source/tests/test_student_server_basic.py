import unittest
from gradescope_utils.autograder_utils.decorators import weight, visibility
import subprocess32 as subprocess
import random
import socket
import sys
import time
import re



class TestStudentServer(unittest.TestCase):
    """
    Here we have basic unit tests that check the student's server.
    """
    # It takes some time to release the port after the server is killed
    # So we keep track of the ports we have used
    used_ports = []

    def __init__(self, *args, **kwargs):
        super(TestStudentServer, self).__init__(*args, **kwargs)
        self.server_port = None
        self.server_process = None

    def setUp(self):
        """
        Run the server before each test
        """
        # Random port between 32768 and 61000, should be no conflicts
        # This is a class variable, so it is shared between all tests
        while True:
            server_port = random.randint(32768, 61000)
            if server_port not in TestStudentServer.used_ports:
                TestStudentServer.used_ports.append(server_port)
                break

        # Start the server
        prog = subprocess.Popen(
            ["/autograder/source/server/tcp_server", str(server_port)], stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

        # Wait for the server to start
        server_ready = False
        for _ in range(5):  # Attempt up to 5 times with a 0.2-second wait between attempts
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect(("localhost", server_port))  # Use the local variable 'server_port'
                    server_ready = True
                    break  # Server is ready, break out of the loop
            except socket.error:
                time.sleep(0.2)  # Wait a bit before trying again
        
        if not server_ready:
            raise Exception("Server did not start within the expected time.")

        self.server_process = prog
        # print(f"Using server port: {server_port}")   // print out the port connected
        self.server_port = server_port

    def tearDown(self) -> None:
        """
        Kill the server after each test
        """
        if self.server_process is not None:
            self.server_process.terminate()
            self.server_process.wait()

    def _send_command(self, command):
        """Helper method to send a command to the server and return the response."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(("localhost", self.server_port))
            command_line = command[:256-2] + '\n\0'
            s.sendall(command_line.encode())
            data = s.recv(256)
            return data.decode()[:-2]  # Removing the last two characters assuming they are '\n\0'

    """
    All the basic socket handling
    """
    @weight(3)
    @visibility("visible")
    def test_server_listens(self):
        """Test the server is accepting connections on the correct port"""
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect(("localhost", self.server_port))
        except socket.error as e:
            self.fail(f"Server should be listening on the specified port. Error: {e}")
        finally:
            s.close()

    @weight(3)
    @visibility("visible")
    def test_control_d_closes_connection(self):
        """Test the server closes the connection when it receives a control-d"""
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("localhost", self.server_port))
        s.sendall(b"\x04")
        s.close()
        self.assertFalse(s.fileno() in [fp for fp in range(3, 256)], "Server should close the connection")

    """
    help command
    """
    @weight(3)
    @visibility("visible")
    def test_server_command_help(self):
        """Test 'help' with no arguments lists all available commands."""
        expected_prefix = "Available commands:" #only check the starting commands as student might add more diy commands
        response = self._send_command("help")
        self.assertTrue(response.startswith(expected_prefix), "'help' should list all available commands (see the requirements for the exact message).")

    @weight(3)
    @visibility("visible")
    def test_help_with_calc(self):
        """Test 'help calc' provides usage for the calc command."""
        # expected_response = "Calculates the result of a op b. Usage: calc a op b"
        response = self._send_command("help calc")
        # self.assertEqual(response.strip(), expected_response, "'help calc' should provide usage for the calc command.")
        self.assertTrue(re.search("usage: calc", response, re.IGNORECASE), "'help calc' should mention usage (see the requirements for the exact message).")

    @weight(3)
    @visibility("visible")
    def test_help_with_sort(self):
        """Test 'help sort' provides usage for the sort command."""
        # expected_response = "Sorts a list of numbers. Usage: sort n1 n2 n3 ..."
        response = self._send_command("help sort")
        # self.assertEqual(response.strip(), expected_response, "'help sort' should provide usage for the sort command.")
        self.assertTrue(re.search("usage: sort", response, re.IGNORECASE), "'help sort' should mention usage (see the requirements for the exact message).")

    @weight(3)
    @visibility("visible")
    def test_help_with_unrecognized_command(self):
        """Test 'help' with an unrecognized command returns an appropriate message."""
        # expected_response = "This command does not exist"
        response = self._send_command("help unknown")
        # self.assertEqual(response.strip(), expected_response, "'help unknown' should indicate the command does not exist.")
        self.assertTrue(re.search("this command does not exist", response, re.IGNORECASE), "'help' with an unknown command should indicate the command does not exist (see the requirements for the exact message).")

    """
    calc command
    """
    @weight(3)
    @visibility("visible")
    def test_calc_addition(self):
        """Test 'calc' the server correctly performs addition."""
        response = self._send_command("calc 2+3")
        self.assertEqual(response, "5", "Server should correctly add a and b.")

    @weight(3)
    @visibility("visible")
    def test_calc_subtraction(self):
        """Test 'calc' the server correctly performs subtraction."""
        response = self._send_command("calc 5-2")
        self.assertEqual(response, "3", "Server should correctly subtract b from a.")

    @weight(3)
    @visibility("visible")
    def test_calc_multiplication(self):
        """Test 'calc' the server correctly performs multiplication."""
        response = self._send_command("calc 2*9")
        self.assertEqual(response, "18", "Server should correctly multiply a by b.")

    @weight(3)
    @visibility("visible")
    def test_calc_division(self):
        """Test 'calc' the server correctly performs division."""
        response = self._send_command("calc 7/2")
        self.assertEqual(response, "3", "Server should correctly divide a by b.")

    # @weight(3)
    # @visibility("visible")
    # def test_calc_division_by_zero(self):
    #     """Test 'calc' the server handles division by zero appropriately."""
    #     response = self._send_command("calc 4/0")
    #     # print(f"Received response: '{response}'")  # print out the response
    #     self.assertEqual(response, "Invalid command", "Server should reply \'Invalid command\' for division by zero.")

    """
    sort command
    """
    @weight(3)
    @visibility("visible")
    def test_sort_command(self):
        """Test 'sort' the server sorts a list of numbers correctly."""
        # Example list of numbers to sort
        numbers = "1 9 0 9 2 3 -1 7 4"
        expected_sorted_numbers = "-1 0 1 2 3 4 7 9 9"

        # Send the sort command to the server
        response = self._send_command(f"sort {numbers}")

        # Assuming the server's response is a space-separated list of sorted numbers
        sorted_response = ' '.join(sorted(response.split(), key=int))

        # Verify the server's response matches the expected sorted list
        self.assertEqual(sorted_response, expected_sorted_numbers, "Server should return the numbers sorted in ascending order.")

    
