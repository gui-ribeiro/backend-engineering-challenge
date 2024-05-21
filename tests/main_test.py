import unittest
import json
from pathlib import Path

from src import main


class MyProgramTest(unittest.TestCase):
    def test_write_to_json(self):
        main.calculate_moving_average("tests/input.json", 10)

        # Load data from output and expected output files
        with open(Path("tests/output.json"), 'r') as f:
            output_data = json.load(f)
        with open(Path("tests/expected_output.json"), 'r') as f:
            expected_output_data = json.load(f)

        # Compare output to expected output
        self.assertListEqual(output_data, expected_output_data)
