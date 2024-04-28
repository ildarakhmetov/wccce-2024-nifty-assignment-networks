from gradescope_utils.autograder_utils.decorators import weight, visibility
from gradescope_utils.autograder_utils.files import check_submitted_files

import unittest

class FilesExistTest(unittest.TestCase):
    """
    Tests here check that the required files exist in both the server
    and clients directories.
    """

    # A list of expected filenames with paths relative to the /solution directory
    expected_filenames = [
        "server/commands.c", 
        "server/commands.h", 
        "server/tcp_server.c", 
        "server/Makefile",
        "clients/tcp_client.c", 
        "clients/tcp_client.py"
    ]

    @weight(4)
    @visibility("visible")
    def test_submitted_files(self):
        """Check all submitted files exist in their respective directories"""
        missing_files = check_submitted_files(self.expected_filenames)
        if len(missing_files) > 0:
            msg = "Missing required files:\n\t"
            msg += "\n\t".join(missing_files)  # Format the missing file paths for readability
            self.fail(msg)