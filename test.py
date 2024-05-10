from datetime import datetime
from typing import Any
import unittest
import json

from main2 import main as user_input
from balanser import AppendType, Balanser, TypeSearch

from filter import FilterByContext, Task, TaskType, get_date


class TestFilter(unittest.TestCase):
    positive_search_input = {
            "bydate 24.12.2024" : Task(TaskType.search, ["bydate", "24.12.2024"]),
            "bycat income" : Task(TaskType.search, ["bycat", "income"]),
            "bycat in" : Task(TaskType.search, ["bycat", "in"]),
            "bycat Доход" : Task(TaskType.search, ["bycat", "Доход"]),
            "bycat consum" : Task(TaskType.search, ["bycat", "consum"]),
            "bycat con" : Task(TaskType.search, ["bycat", "con"]),
            "bycat расход" : Task(TaskType.search, ["bycat", "расход"]),
            "bysumm -13" : Task(TaskType.search, ["bysumm", "-13"]),
            "bydate 12:03:1995" : Task(TaskType.search, ["bydate", "12:03:1995"]),
            "bydate 11.02.1995" : Task(TaskType.search, ["bydate", "11.02.1995"]),
        }
    def test_positive_search_data(self):
        for x in self.positive_search_input:
            self.assertEqual(FilterByContext(x).return_task().__dict__, self.positive_search_input[x].__dict__)

    def test_negative_search_data(self):
        self.assertRaises(ValueError, FilterByContext("bydate").return_task)

    def test_positive_append_data(self):
        self.assertEqual(FilterByContext("123").return_task().__dict__, Task(TaskType.append, "123").__dict__)
        self.assertEqual(FilterByContext("-123 123").return_task().__dict__, Task(TaskType.append, "-123 123").__dict__)
        self.assertEqual(FilterByContext("123 qwe wer 123").return_task().__dict__, Task(TaskType.append, "123 qwe wer 123").__dict__)

    def test_getdate_positive(self):
        self.assertEqual(get_date("24-12-2024"), '2024-12-24')
        self.assertEqual(get_date("13:12.2024"), '2024-12-13')
        self.assertEqual(get_date("24:12-2024"), '2024-12-24')


        
    def test_get_date(self):
        self.assertEqual(get_date("12:07:1999"), "1999-07-12")
        self.assertEqual(get_date("12.07.1999"), "1999-07-12")
    


class TestMainPreRelease(unittest.TestCase):
    date_now = str(datetime.today()).partition(' ')[0]
    predict_user_data = {
    "-100" : {'user_settings': {'balanse': 9900.0, 'income': 0, 'consumption': -100.0, 'increment': 1}, 'tranzaction': [[-100.0, '', 1, date_now, 'consumption']]},
    "-100 -d 20.09.2023" : {'user_settings': {'balanse': 9900.0, 'income': 0, 'consumption': -100.0, 'increment': 1}, 'tranzaction': [[-100.0, '', 1, '2023-09-20', 'consumption']]},
    "-100 -d 20.09.2023 qwe 123" : {'user_settings': {'balanse': 9900.0, 'income': 0, 'consumption': -100.0, 'increment': 1}, 'tranzaction': [[-100.0, 'qwe 123', 1, '2023-09-20', 'consumption']]},
    "100" : {'user_settings': {"balanse" : 10100.0,"income": 100.0,"consumption": 0,"increment": 1},'tranzaction': [[100.0,"",1, date_now,"income"]]},
    "100 -d 20.09.2023" : {'user_settings': {"balanse" : 10100.0,"income": 100.0,"consumption": 0,"increment": 1},'tranzaction': [[100.0,"",1,"2023-09-20","income"]]},
    "100 -d 20.09.2023 qwe 123" : {'user_settings': {"balanse" : 10100.0,"income": 100.0,"consumption": 0,"increment": 1},'tranzaction': [[100.0,"qwe 123",1,"2023-09-20","income"]]},
}
    default_user_data = {
    'user_settings': {
        "balanse" : 10000,
        "income": 0,
        "consumption": 0,
        "increment": 0
    },
    'tranzaction': []
}
    def test_negative_user_input(self):
        
        self.assertIsNone(user_input(self.default_user_data, ""))
        self.assertIsNone(user_input(self.default_user_data, "123 -d"))

    def test_positive_user_input(self):
        for trans in self.predict_user_data:
            default_user_data = {
    'user_settings': {
        "balanse" : 10000,
        "income": 0,
        "consumption": 0,
        "increment": 0
    },
    'tranzaction': []
}
            self.assertEqual(user_input(default_user_data, trans), self.predict_user_data[trans], trans)



if __name__ == "__main__":
    
    unittest.main()