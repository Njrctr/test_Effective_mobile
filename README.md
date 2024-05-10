# Balanсer
## About
`Balanсer` - это приложения для личного учёта расходов и доходов в вашей командной строке.
## Download/Установка
## Первый запуск
При первом запуске программа попросит вас ввести свой текущий баланс. Создаст [файл](test_user_data.json) пользовательских настроек в формате json, из которого будут браться имеющиеся данные о транзакциях и балансе.
Пример файла с данными - [Файл хранения](test_user_data.json)

## Использование программы
### Создание транзакций:
##### Например:
+ `115.15` - Создаст запись о доходе, установив локальное время транзакции! Описание транзакции останется пустым.
+ + `115.15 Купил дорогой пакетик` - Создаст запись о доходе, установив локальное время транзакции! В качестве описания будет установлено `Купил дорогой пакетик`.
+ `115.20 -d 10.01.2020` - Создаст запись о доходе, установив переданную вами дату в качестве времени транзакции! 
+ `115.20 -d 10.01.2020 Купил сливы` - Создаст запись о доходе, установив переданную вами дату в качестве времени транзакции! В качестве описания транзакции будет установлено `Купил сливы`.
> #### Имейте ввиду что параметр времени передаётся сразу после флага `-d`, который может быть указан только на втором месте в команде и никак иначе!

### Поиск по транзакциям:
##### Например:
+ `bydate 11.09.2010` - Выведет список всех транзакций совершённых за указанную дату.
+ `bysum 115` - Выведет список всех транзакций на указанную сумму.
+ `bycat Доход` - Выведет список всех транзакций удовлетворяющих категории транзакции. Можно указывать следующие параметры: Доход - `доход / income / in`, Расход - `расход / consum / out / con`.

### Редактирование транзакций:
+ `-e 3` - Редактирование транзакции, где номер транзакции = `3`. Позволяет изменить Дату/Сумму/Описание транзакции.

> ## Вы также можете ввести `-h` или `--help` для справки в самой программе.