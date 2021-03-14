import unittest
import unittest.mock as mock
from unittest.mock import patch
import os
import sys

sys.path.append(os.path.abspath('../../'))
from app import query_db, update_db, add_db
import models

DB_INPUT = "input"
DB_EXPECTED = "expected"
INITIAL_DB1 = 'Jerry'
INITIAL_DB2 = 'Peter'

class QueryTestCase(unittest.TestCase):
    def setUp(self):
        self.success_test_params = [
            {
                DB_EXPECTED: [INITIAL_DB1]
            }
        ]
        self.failure_test_params = [
             {
                DB_EXPECTED: [INITIAL_DB2, INITIAL_DB2]
            },
            {
                DB_EXPECTED: [INITIAL_DB2,'larry']
            }
            ]
        
        initial_db = models.Player(username=INITIAL_DB1, score=100)
        self.initial_db_mock = [initial_db]
    
    def mocked_person_query_all(self):
        return self.initial_db_mock
        
    def mocked_db_session_commit(self):
        pass
    
    def test_success(self):
        for test in self.success_test_params:
            with patch('models.Player.query') as mocked_query:
                print(self.initial_db_mock)
                mocked_query.all = self.mocked_person_query_all
                actual_result = query_db()
                expected_result = test[DB_EXPECTED]
                
                self.assertEqual(len(actual_result), len(expected_result))
                self.assertEqual(actual_result[0], expected_result[0])
    
    def test_failure(self):
        for test in self.failure_test_params:
            with patch('models.Player.query') as mocked_query:
                mocked_query.all = self.mocked_person_query_all
                actual_result = query_db()
                expected_result = test[DB_EXPECTED]
                
                self.assertNotEqual(len(actual_result), len(expected_result))
                self.assertNotEqual(actual_result[0], expected_result[0])

class AddTestCase(unittest.TestCase):
    def setUp(self):
        self.success_test_params = [
            {
                DB_INPUT: 'Kyle',
                DB_EXPECTED: [INITIAL_DB1 , 'Kyle']
            }
        ]
        self.failure_test_params = [
             {
                DB_INPUT: 'Kyle',
                DB_EXPECTED: [INITIAL_DB1, 'Peter', 'steve']
            },
            {
                DB_INPUT: 'larry',
                DB_EXPECTED: [INITIAL_DB1 , 'steve' , 'kyle', 'larry']
            }
            ]
        
        initial_db = models.Player(username=INITIAL_DB1, score=100)
        self.initial_db_mock = [initial_db]
        
    def mocked_db_session_add(self, username):
        self.initial_db_mock.append(username)
    
    def mocked_db_session_commit(self):
        pass
    
    def mocked_person_query_all(self):
        return self.initial_db_mock
    
    def test_success(self):
        for test in self.success_test_params:
            with patch('app.DB.session.add', self.mocked_db_session_add):
                with patch('app.DB.session.commit', self.mocked_db_session_commit):
                    with patch('models.Player.query') as mocked_query:
                        mocked_query.all = self.mocked_person_query_all
                        actual_result = add_db(test[DB_INPUT])
                        expected_result = test[DB_EXPECTED]
                
                        self.assertEqual(len(actual_result), len(expected_result))
                        self.assertEqual(actual_result[1], expected_result[1])
    
    def test_failure(self):
        for test in self.failure_test_params:
            with patch('app.DB.session.add', self.mocked_db_session_add):
                with patch('app.DB.session.commit', self.mocked_db_session_commit):
                    with patch('models.Player.query') as mocked_query:
                        mocked_query.all = self.mocked_person_query_all
                        actual_result = add_db(test[DB_INPUT])
                        expected_result = test[DB_EXPECTED]

                        self.assertNotEqual(len(actual_result), len(expected_result))
                        self.assertNotEqual(actual_result[1], expected_result[1])

if __name__ == '__main__':
    unittest.main()