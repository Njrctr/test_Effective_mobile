from datetime import datetime
from strenum import StrEnum
import datefinder

class TypeSearch(StrEnum):
    """Строковые перечисления вариантов поиска"""

    by_category = "bycat"
    by_summ = "bysumm"
    by_date = "bydate"


class TaskType(StrEnum):
    """Строковые перечисления типов задач"""

    append = "append"
    search = "search"
    edit = "edit"


class AppendType(StrEnum):
    """Строковые перечисления вариантов транзакции"""

    consumption = "consumption"
    income = "income"


class Task:
    """Класс отражающий тип задачи и её контекстные данные"""

    def __init__(self, task_type, context) -> None:
        self.task_type: TaskType = task_type
        self.context: list[str] | str = context
    


class FilterByContext:
    """Этот класс отвечает за распределение и фильтрацию пользовательского ввода"""

    def __init__(self, user_input: str) -> None:
        self.user_input = user_input

    def return_task(self) -> Task:
        """Вовзращает экземпляр Задачи в зависимости от аргументов переданных пользователем"""
        
        splited_user_input = self.user_input.split()
        if splited_user_input[0] in ["bydate", "bysumm", "bycat"]:
            if len(splited_user_input) == 2:
                return Task(TaskType.search, splited_user_input)
            else:
                raise ValueError('[---] Ошибка при вводе поискового запроса.')
        elif splited_user_input[0] == '-e':
            if len(splited_user_input) == 2:
                return Task(TaskType.edit, splited_user_input)
            elif len(splited_user_input) > 2:
                raise ValueError(f'[---] Ошибка при вводе id транзакции. недопустимые аргументы: {splited_user_input[2:]}')
            else:
                raise ValueError('[---] Ошибка при вводе id транзакции.')

        else:
            return Task(TaskType.append, self.user_input)
        
        
    def return_correct_trans(self) -> list:
        """Собирает список исходя из количества и состава переданных пользователем аргументов"""

        summ: int 
        date: str = str(datetime.today()).partition(' ')[0]
        category: AppendType 
        description: str = ''
        command = self.user_input.split(maxsplit=3)

        summ = get_summ(command[0])
        category = AppendType.consumption if summ < 0 else AppendType.income

        if len(command) == 1:
            pass

        elif (len(command) == 2) and (command[1] != '-d'):
            description = command[1]
        
        elif (len(command) == 2) and (command[1] == '-d'):
            raise ValueError("Ошибка, не указана дата.") # "-123 -d"

        elif (len(command) >= 3) and (command[1] == '-d'): # "-123 -d 20.12.2024"
            try:
                date = get_date(command[2])
            except Exception as e:
                raise e
                
        
            
        if len(command) > 3: # "-123 -d 20.12.2024 comment qwe"

            description =command[3]
            print('description: ', description)

        return [summ, date, category, description]
    


def get_date(nocorrect: str) -> str:
    """Пробует получить валидную строку даты из введённых пользователем данных"""

    try:
        nocorrect = nocorrect.replace(":", ".").replace("-", ".").replace("/", ".")
        date = datetime.strptime(nocorrect, '%d.%m.%Y').isoformat().split(sep="T")[0]
        return date
    except ValueError:
        raise ValueError("[---]Неверный формат ввода даты, попробуйте снова.\nТребуемый формат даты: dd.mm.yyyy (Пример: 25.12.1998)\n")


def get_summ(nocorrect: str) -> float:
    """Пробует получить валидное число float из введённых пользователем данных"""
    nocorrect = nocorrect.replace(",", ".")

    if len(nocorrect.split(sep='.')) > 1 and len(nocorrect.split(sep='.')[1]) > 2:
        raise ValueError("[---]Недопустимое количество знаков после точки.") 
    try:
        summ = float(nocorrect)

        return summ
    except ValueError:
        # print("[---]Неверный формат ввода суммы, попробуйте снова.")
        raise ValueError("[---]Неверный формат ввода суммы, попробуйте снова.")