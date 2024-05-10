from filter import AppendType, TypeSearch, get_date, get_summ


    



class Balanсer:
    """Класс Balanser используется для управления транзакциями
    
    Atrrributes
    ----------
    user_data: dict
        json словарь загруженный из файла настроек

    Methods
    --------
    make_tranzaction([список данных для транзакции])
        Совершает добавление транзакции в базу пользователя
    search()
        Возвращает список транзакций удовлетворяющих поиску
    edit()
        Редактирует определённую транзакцию
    """

    def __init__(self, user_data: dict) -> None:
        self.user_data = user_data
        



    def make_tranzaction(self, tranzaction: list) -> list[list[float, str, int, str, str]]:
        """Метод для совершения транзакции в общий пул транзакций"""

        summ: float = round(tranzaction[0], 2)
        date: str = tranzaction[1]
        category: AppendType = tranzaction[2]
        description: str | None = tranzaction[3]
        if (self.user_data['user_settings']['balanse'] + summ) < 0:
            raise ValueError("[-] Ошибка: После выполнения операции ваш баланс будет отрицательным, это недопустимо!")

        self.user_data["user_settings"][category] += summ
        self.user_data["user_settings"]['balanse'] += summ

        self.user_data["user_settings"]['increment'] += 1

        correct_trans = [summ, description, self.user_data["user_settings"]['increment'], date, category.lower()]

        self.user_data['tranzaction'].append(correct_trans)

        print(f"Совершена транзакция:")
        return [correct_trans]




    def search(self, by: TypeSearch, search: str) -> list[float, str, int, str, str] | None:
        """Метод для поиска транзакций по определённым параметрам описанным в классе TypeSearch"""

        ll = []
        match by:

            case TypeSearch.by_date:
                print(f"Транзакции по Дате {search}:\n")
                ll += list(filter(lambda s: s[3] == search, self.user_data['tranzaction']))
                
                
            case TypeSearch.by_category:
                if search.lower() in ["доход", 'income', 'in']:
                    search = AppendType.income
                elif search.lower() in ["расход", 'consum', 'out', 'con']:
                    search = AppendType.consumption

                print(f"Транзакции по Категории {'Доход' if search == AppendType.income else 'Расход'}:\n")
                ll +=  list(filter(lambda s: s[4] == search, self.user_data['tranzaction']))
                
                        
            case TypeSearch.by_summ:
                print(f"Транзакции по сумме {search}:\n")
                ll +=  list(filter(lambda s: s[0] == search, self.user_data['tranzaction']))

        return ll
    
    
    def edit(self, id: int) -> list[list[float, str, int, str, str]]:
        """Метод для редактирования выбранной транзакции"""

        if id > self.user_data["user_settings"]['increment']:
            raise ValueError("Отсутствует транзакция удовлетворяющая id.")
        
        print(f"Изменение транзакции с id = {id}:\n")
        
        for index, trans in enumerate(self.user_data['tranzaction']):
        
            if trans[2] == id: 
                category = 'Доход' if trans[4] == AppendType.income else 'Расход'
                description = trans[1] if trans[1] is not None else ''
                print(f"Текущие данные по транзакции:\n\nДата: {trans[3]} (Номер транзакции: {trans[2]})\nКатегория: {category}\nСумма: {trans[0]}\nОписание: {description}\n")
                match input("Дата - 1. Сумма - 2. Описание - 3.\nВыберите что хотите изменить, введите число:"):
                    case "1":
                        
                        new_date = get_date(input("Введите дату: "))
                        trans[3] = new_date
                    case "2":
                        new_summ = get_summ(input("Введите сумму: "))
                        if new_summ < 0:
                            new_category = AppendType.consumption
                        else: 
                            new_category = AppendType.income

                        self.user_data['user_settings'][trans[4]] -= trans[0]
                        self.user_data['user_settings'][new_category] += new_summ
                        self.user_data["user_settings"]['balanse'] -= trans[0]
                        self.user_data["user_settings"]['balanse'] += new_summ
                        trans[4] = new_category
                        trans[0] = new_summ
                        
                    case "3":
                        new_description = input("Введите описание: ")
                        trans[1] = new_description
                    case _:
                        raise ValueError("Некоректный ввод опции.")

                
                self.user_data['tranzaction'][index] = trans
                print("Новые данные о траназкции:\n")
                return [trans]