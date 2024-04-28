import unittest
from gradescope_utils.autograder_utils.decorators import weight, visibility

class TestServerClientCompiles(unittest.TestCase):
    """
    Tests here check that the server and client files compile without errors.
    """
    
    def setUp(self):
        # No setup required for this test class
        pass

    @weight(6)
    @visibility("visible")
    def test_tcp_server_compiles(self):
        """Test that tcp_server components compile"""
        try:
            with open("/autograder/source/server/tcp_server_compilation_log.txt", "r") as f:
                log = f.read()
                if "error" in log:  # Check for the word "error" in the log
                    self.fail("tcp_server compilation failed. See log for details:\n\n" + log)
        except FileNotFoundError:
            pass

    @weight(6)
    @visibility("visible")
    def test_tcp_client_c_compiles(self):
        """Test that tcp_client.c compiles"""
        try:
            with open("/autograder/source/clients/tcp_client_compilation_log.txt", "r") as f:
                log = f.read()
                if "error" in log:  # Check for the word "error" in the log
                    self.fail("tcp_client.c compilation failed. See log for details:\n\n" + log)
        except FileNotFoundError:
            pass

    
    # didn't test tcp_client.py as its python file