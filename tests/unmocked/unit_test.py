import unittest
import os
import sys

sys.path.append(os.path.abspath('../../'))
from app import add_user, set_winner, check_move

USER_INPUT = "input"
USER_EXPECTED = "expected"
USER_BOOL = True

class AddUserTestCase(unittest.TestCase):
    def setUp(self):
        self.success_test_params = [
            {
                USER_INPUT: "Dave",
                USER_EXPECTED: 'Player X Dave',
            }
        ]
        
        self.failure_test_params = [
            {
                USER_INPUT: "Dave",
                USER_EXPECTED: 'Dave',
            },
            {
                USER_INPUT: "Dave",
                USER_EXPECTED: 'Spectator Dave',
            }
            ]
            
    def test_split_success(self):
        for test in self.success_test_params:
            actual_result = add_user(test[USER_INPUT])
            
            expected_result = test[USER_EXPECTED]
            
            self.assertEqual(len(actual_result), len(expected_result))
            self.assertEqual(actual_result[0], expected_result[0])
            
    def test_split_failure(self):
        for test in self.failure_test_params:
            actual_result = add_user(test[USER_INPUT])
            
            expected_result = test[USER_EXPECTED]
            
            self.assertNotEqual(len(actual_result), len(expected_result))
            self.assertNotEqual(actual_result[0], expected_result[0])

class CheckWinnerTestCase(unittest.TestCase):
    def setUp(self):
        self.success_test_params = [
            {
                USER_INPUT: [["Dave","Larry"],False],
                USER_EXPECTED: ["Dave","Larry"],
            },
            {
                USER_INPUT: [["Dave","Larry"],True],
                USER_EXPECTED: ["Larry","Dave"],
            }
        ]
        
        self.failure_test_params = [
            {
                USER_INPUT: [["Dave","Larry"],False],
                USER_EXPECTED: ["Larry","Dave"],
            }
            ]
            
    def test_split_success(self):
        for test in self.success_test_params:
            actual_result = set_winner(test[USER_INPUT][0], test[USER_INPUT][1])
            
            expected_result = test[USER_EXPECTED]
            
            self.assertEqual(len(actual_result), len(expected_result))
            self.assertEqual(actual_result[0], expected_result[0])
            
    def test_split_failure(self):
        for test in self.failure_test_params:
            actual_result = set_winner(test[USER_INPUT][0], test[USER_INPUT][1])
            
            expected_result = test[USER_EXPECTED]
            
            self.assertNotEqual(actual_result[0], expected_result[0])
            self.assertNotEqual(actual_result[1], expected_result[1])
            
class CheckMoveTestCase(unittest.TestCase):
    def setUp(self):
        self.success_test_params = [
            {
                USER_INPUT: {'i': 8, 'xNext': True},
                USER_EXPECTED: {'i': 8, 'xNext': True},
            },
            {
                USER_INPUT: {'i': 3, 'xNext': False},
                USER_EXPECTED: {'i': 3, 'xNext': False},
            }
        ]
        
        self.failure_test_params = [
            {
                USER_INPUT: {'i': 8, 'xNext': True},
                USER_EXPECTED: {'i': 7, 'xNext': False},
            }
            ]
            
    def test_split_success(self):
        for test in self.success_test_params:
            actual_result = check_move(test[USER_INPUT])
            
            expected_result = test[USER_EXPECTED]
            
            self.assertEqual(len(actual_result), len(expected_result))
            self.assertEqual(actual_result['i'], expected_result['i'])
            
    def test_split_failure(self):
        for test in self.failure_test_params:
            actual_result = check_move(test[USER_INPUT])
            
            expected_result = test[USER_EXPECTED]
            
            self.assertNotEqual(actual_result['i'], expected_result['i'])
            self.assertNotEqual(actual_result['xNext'], expected_result['xNext'])
            
if __name__ == '__main__':
    unittest.main()
    