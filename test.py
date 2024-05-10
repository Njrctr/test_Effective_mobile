from datetime import datetime
import unittest

from main2 import main as user_input
from balancer import AppendType, Balanсer, TypeSearch

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
            "bysum -13" : Task(TaskType.search, ["bysum", "-13"]),
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
    "-100" : [[-100.0, '', 1, date_now, AppendType.consumption]],
    "-100.14" : [[-100.14, '', 1, date_now, AppendType.consumption]],
    "-100 -d 20.09.2023" : [[-100.0, '', 1, '2023-09-20', AppendType.consumption]],
    "-100 -d 20.09.2023 qwe 123" : [[-100.0, 'qwe 123', 1, '2023-09-20', AppendType.consumption]],
    "100" : [[100.0,"",1, date_now, AppendType.income]],
    "100.30" : [[100.3,"",1, date_now, AppendType.income]],
    "100 -d 20.09.2023" : [[100.0,"",1,"2023-09-20", AppendType.income]],
    "100 -d 20.09.2023 qwe 123" : [[100.0,"qwe 123",1,"2023-09-20", AppendType.income]],
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


    

    def test_positive_user_search(self):
    
        
        predict_user_data = {
            
    "bydate 10.05.2024" : [[-10.0, '', 1, '2024-05-10', 'consumption'], [-10.0, 'qwe', 2, '2024-05-10', 'consumption'], [10.0, '', 4, '2024-05-10', 'income']],
    "bycat income" : [[10.0, 'nefor', 3, '1999-07-12', 'income'], [10.0, '', 4, '2024-05-10', 'income'], [11.0, 'nefor', 5, '1999-07-12', 'income']],
    "bycat in" : [[10.0, 'nefor', 3, '1999-07-12', 'income'], [10.0, '', 4, '2024-05-10', 'income'], [11.0, 'nefor', 5, '1999-07-12', 'income']],
    "bycat Доход" : [[10.0, 'nefor', 3, '1999-07-12', 'income'], [10.0, '', 4, '2024-05-10', 'income'], [11.0, 'nefor', 5, '1999-07-12', 'income']],
    "bycat consum" : [[ -10.0, '', 1, '2024-05-10', 'consumption'], [ -10.0, 'qwe', 2, '2024-05-10', 'consumption'],[-11.0, 'nefor', 6, '1999-07-12', 'consumption']],
    # 'wtf' :       [[-10.0, '', 1, '2024-05-10', 'consumption'], [-10.0, 'qwe', 2, '2024-05-10', 'consumption'], [-11.0, 'nefor', 6, '1999-07-12', 'consumption']],
    'bycat con' : [[-10.0, '', 1, '2024-05-10', 'consumption'], [-10.0, 'qwe', 2, '2024-05-10', 'consumption'], [-11.0, 'nefor', 6, '1999-07-12', 'consumption']],
    'bycat расход' : [[-10.0, '', 1, '2024-05-10', 'consumption'], [-10.0, 'qwe', 2, '2024-05-10', 'consumption'], [-11.0, 'nefor', 6, '1999-07-12', 'consumption']],
    'bysum -10' : [[-10.0, '', 1, '2024-05-10', 'consumption'],[-10.0, 'qwe', 2, '2024-05-10', 'consumption']],
    'bysum 10' : [[10.0,'nefor', 3, '1999-07-12', 'income'],[10.0, '', 4, '2024-05-10','income']],
    'bydate 12.07.1999' : [[10.0,'nefor', 3,'1999-07-12','income'], [11.0,'nefor', 5,'1999-07-12','income'], [-11.0,'nefor', 6,'1999-07-12','consumption']],
}

        
         
        for search_string in predict_user_data:
            default_user_data = {
    'user_settings': {
        'balanse' : 10000,
        "income": 0,
        "consumption": 0,
        "increment": 0
    },
    'tranzaction': [
        [ -10.0, '', 1, '2024-05-10', 'consumption'],
        [ -10.0, 'qwe', 2,"2024-05-10",'consumption'],
        [10.0, "nefor", 3,"1999-07-12","income"],
        [10.0, "", 4,"2024-05-10","income"],
        [11.0,"nefor", 5,"1999-07-12","income"],
        [-11.0,"nefor", 6,"1999-07-12",'consumption'],
    ]
}  
            self.assertEqual(user_input(default_user_data, search_string), predict_user_data[search_string])


if __name__ == "__main__":
    
    unittest.main()