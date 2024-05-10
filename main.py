import json
import os
from art import tprint

from balancer import Balanсer
from filter import AppendType, FilterByContext, TaskType, TypeSearch, get_date, get_summ


#consumption - расход
#income - доход


def main(user_data: dict, user_input: str):
    
    split_user_input = user_input.split()
    if len(user_input) == 0:
        return
    if split_user_input[0] in ['-h', '--help']:
        print("""
Создание записи о расходе/доходе:
    [сумма] [-d [дата] : опционально. По умолчанию - сегодняшнее число] [Описание записи : опционально]    Например: -100500 -d 12.01.2024 Купил кофе в Старбакс.

Редактирование записи дохода/расхода:
    [-e] [id|номер транзакции]    Например: -e 1 . Далее выбираете пункт, который будете редактировать.

Поиск транзакций:
    [bydate] [дата транзакц(ии/ий)]    Выводит список всех транзакций по указанной дате. 
    [bycat] [категория транзакц(ии/ий)]    Выводит список всех транзакций из указанной категории. 
    [bysum] [сумма транзакц(ии/ий)]    Выводит список всех транзакций по указанной сумме. 
""")
        return
    try:
        task = FilterByContext(user_input).return_task()
    except ValueError as ex:
        print(ex)
        return

    match task.task_type:
        case TaskType.search:
            if task.context[0] == TypeSearch.by_date:
                try:
                    search = get_date(task.context[1])
                except Exception as ex:
                    print(ex)
                    return

            elif task.context[0] == TypeSearch.by_category:
                search = task.context[1]

            elif task.context[0] == TypeSearch.by_summ:
                search = get_summ(task.context[1])

            else:
                print("Неверно указана поисковая команда команда! Воспользуйтесь опцией --help или -h")
                return 
            
            content = Balanсer(user_data).search(task.context[0], search)

            if len(content) == 0:
                print("Нет транзакций удовлетворяющих поиску.\n")
                return
                
        case TaskType.edit:
            try:
                task_id = int(split_user_input[1])
                content = Balanсer(user_data).edit(task_id)
            except ValueError as ex:
                print(ex)
                return
        case TaskType.append:
            try:
                correct_command = FilterByContext(task.context).return_correct_trans()
                content = Balanсer(user_data).make_tranzaction(correct_command)
            except ValueError as ex:
                print(ex)   
                return
    for trans in content:
            print(f"""
--------------------------------------------
Дата: {trans[3]} (Номер транзакции: {trans[2]})
Категория: {"Доход" if trans[4] == AppendType.income else "Расход"}
Сумма: {trans[0]}
Описание: {trans[1] if trans[1] is not None else ''}
--------------------------------------------""")
    return content
            
      
default_user_data = {
    'user_settings': {
        "balanse" : 10000,
        "income": 0,
        "consumption": 0,
        "increment": 0
    },
    'tranzaction': []
}

if __name__ == "__main__":
    tprint("Balancer\nby xrnze")
    try: 
        with open(r"user_data.json", 'r') as file:
            user_data = json.load(file)
    except FileNotFoundError:
        user_data = {
    'user_settings': {
        "balanse" : float(input("Укажите текущий баланс: ")),
        "income": 0,
        "consumption": 0,
        "increment": 0
    },
    'tranzaction': []
}
    try:
        while True:
            print("Справка по командам: -h или --help")
            print(f"Текущий баланс: {user_data["user_settings"]['balanse']} | Доходы: {user_data["user_settings"]['income']} | Расходы: {user_data["user_settings"]['consumption']}\n")
            user_input = input("Выберите действие: ")
            
            os.system('cls' if os.name == 'nt' else 'clear')
            main(user_data, user_input)
    except KeyboardInterrupt:
        print("\nВыход из программы...")
    finally:
        with open(r"user_data.json", 'w') as file:
            json.dump(user_data, file, indent=2)
        