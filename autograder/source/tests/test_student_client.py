import unittest
import subprocess
import socket
import time
from gradescope_utils.autograder_utils.decorators import weight, visibility
import random

class TestStudentClient(unittest.TestCase):
    """
    This class contains unit tests for testing student-implemented TCP clients (both C and Python versions).
    It ensures that clients can successfully establish a connection with a TCP server and perform expected interactions.
    """
    used_ports = []

    def setUp(self):
        """
        Start the student's server before each client test.
        """
        server_port = random.randint(32768, 61000)
        while server_port in TestStudentClient.used_ports:
            server_port = random.randint(32768, 61000)
        TestStudentClient.used_ports.append(server_port)

        self.server_process = subprocess.Popen(
            ["/autograder/source/server/tcp_server", str(server_port)],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

        if not self.wait_for_server_start("localhost", server_port):
            self.server_process.terminate()
            raise Exception("Server did not start within the expected time.")
        
        self.server_port = server_port

    def tearDown(self):
        """
        Kill the student's server after each test.
        """
        if self.server_process:
            self.server_process.terminate()
            self.server_process.wait()

    def wait_for_server_start(self, host, port, timeout=5):
        """
        Wait for the server to start by attempting to connect to it.
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.connect((host, port))
                    return True
            except socket.error:
                time.sleep(0.1)
        return False

    @weight(3)
    @visibility("visible")
    def test_c_client_connection(self):
        """
        Test C client can successfully connect to the server.
        """
        # Attempt to start the C client and connect to the server
        client_process = subprocess.Popen(
            ["/autograder/source/clients/tcp_client", "localhost", str(self.server_port)],
            stdin=subprocess.PIPE,  # Even if not used, just for the sake of completeness
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        try:
            # Wait for the client process to complete with a timeout
            stdout, stderr = client_process.communicate(timeout=10)

            # If the client process exits with a non-zero exit code, it means there was an error
            self.assertEqual(client_process.returncode, 0, "C client did not exit cleanly. It might not have connected successfully.")
            
            # Optional: Log any output for debugging purposes
            if stderr:
                print("C client stderr:", stderr.decode())

        except subprocess.TimeoutExpired:
            client_process.kill()
            self.fail("C client timed out, which may indicate it failed to connect or interact with the server within the expected time.")

    @weight(3)
    @visibility("visible")
    def test_python_client_connection(self):
        """
        Test Python client can successfully connect to the server.
        """
        input_data = b"some input\n"  # Example input data to send to the client
        client_process = subprocess.Popen(
            ["python3", "/autograder/source/clients/tcp_client.py", "localhost", str(self.server_port)],
            stdin=subprocess.PIPE,  # Enable writing to the client's stdin
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        try:
            # Wait for the client process to complete with a timeout
            stdout, stderr = client_process.communicate(input=input_data, timeout=10)

            # Check if the client process exits cleanly (i.e., without errors)
            self.assertEqual(client_process.returncode, 0, "Python client did not exit cleanly. It might not have connected successfully.")
            
            # Optional: Log any output for debugging purposes
            if stderr:
                print("Python client stderr:", stderr.decode())

        except subprocess.TimeoutExpired:
            client_process.kill()
            self.fail("Python client timed out, which may indicate it failed to connect or interact with the server within the expected time.")


if __name__ == '__main__':
    unittest.main()
