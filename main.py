import datetime as dt


class Record:
    def __init__(self, amount, comment, date=''):
        self.amount = amount
        self.date = (
            dt.datetime.now().date() if
            not
            # Строковые литералы принято выносить из кода на случай, 
            # если вдруг поменяют ТЗ и нужно будет менять формат даты.
            # Легче же формат поменять в одном месте, верно? :)
            date else dt.datetime.strptime(date, '%d.%m.%Y').date())
        self.comment = comment


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []
    
    # Для нетривиальных функций стоит написать пояснение.
    # Полезно будет по этой теме изучить статью: 
    # https://habr.com/ru/post/499358/
    def add_record(self, record):
        self.records.append(record)

    # Давай еще добавим аннотации :)
    # С ними код станет понятнее другим разработчикам.
    def get_today_stats(self):
        today_stats = 0
        # 1) Record - это класс. Не имеет смысла в записях (self.records) его искать.
        # Логичнее будет элемент последовательности назвать, например, record.
        # 2) Попробуй здесь использовать list comprehension ("составление списков"). 
        # Вместо того, чтобы проходить циклом по всем событиям, можно собрать отдельный список из только тех событий, 
        # которые подходят нам по условию.
        for Record in self.records:
            # Дату dt.datetime.now().date() лучше вынести из кода (как константу).
            # По pep-8 константам нужно давать говорящие названия и именовать в верхнем регистре.
            if Record.date == dt.datetime.now().date():
                # Сумму поможет оператор sum().
                # В качестве аргумента получает любую перечислимую коллекцию (список, кортеж и т.д.)
                # и возвращает сумму элементов.
                today_stats = today_stats + Record.amount
        return today_stats

    def get_week_stats(self):
        week_stats = 0
        # Константу лучше вынести из кода (так как она используется в нескольких методах),
        # также назвать ее нужно в верхнем регистре.
        today = dt.datetime.now().date()
        for record in self.records:
            if (
                # Попробуй использовать двойное неравенство :)
                # Это упростит выражение.
                (today - record.date).days < 7 and
                (today - record.date).days >= 0
            ):
                # Также попробуй использовать оператор sum(). 
                week_stats += record.amount
        return week_stats


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):  # Получает остаток калорий на сегодня
        # Лучше подсчет оставшихся калорий или денег вынести в отдельный метод родительского класса.
        x = self.limit - self.get_today_stats()
        if x > 0:
            # pep-8 не рекомендует использовать бэкслэши для переноса строк. 
            # https://tirinox.ru/new-line/
            return f'Сегодня можно съесть что-нибудь' \
                   f' ещё, но с общей калорийностью не более {x} кКал'
        # Можно обойтись без лишнего else :)
        # https://medium.com/lemon-code/guard-clauses-3bc0cd96a2d3
        else:
            return('Хватит есть!')


class CashCalculator(Calculator):
    USD_RATE = float(60)  # Курс доллар США.
    EURO_RATE = float(70)  # Курс Евро.

    def get_today_cash_remained(self, currency,
                                USD_RATE=USD_RATE, EURO_RATE=EURO_RATE):
        currency_type = currency
        cash_remained = self.limit - self.get_today_stats()
        # Попробуй для выбора валюты использовать словарь
        # Это избавит от лишних if/else
        if currency == 'usd':
            cash_remained /= USD_RATE
            currency_type = 'USD'
        elif currency_type == 'eur':
            cash_remained /= EURO_RATE
            currency_type = 'Euro'
        elif currency_type == 'rub':
            # константу лучше вынести из кода (RUB_RATE)
            cash_remained == 1.00
            currency_type = 'руб'
        if cash_remained > 0:
            return (
                # Это строковой литерал, который лучше вынести в константу.
                # Выносить нужно вместе с конструкциями '...{}...' (если они есть), 
                # тогда вычисленные значения сможем подставить в строку при помощи '.format'
                # Это нужно для поддерживаемости кода. Например, если нужно будет
                # поменять тексты или форматы в одном месте.
                # Код может и в несколько тысяч строк, в которых, например, 50 литералов и 
                # они на русском, а завтра будет задача выкатить версию на английском.
                # Пример:
                # CASH_BALANCE = 'На сегодня осталось {balance} {currency_name}'
                # ......
                # if today_remained > 0: 
                #            return CASH_BALANCE.format(balance=cash_remained_str, 
                #                                       currency_name=currency_name)
                f'На сегодня осталось {round(cash_remained, 2)} '
                f'{currency_type}'
            )
        elif cash_remained == 0:
            # Также лучше вынести в константу.
            return 'Денег нет, держись'
        # Лучше использовать else, так как осталось одно условие.
        elif cash_remained < 0:
            return 'Денег нет, держись:' \
                   ' твой долг - {0:.2f} {1}'.format(-cash_remained,
                                                     currency_type)
    
    # Нет смысла определять этот метод, так как он уже есть в родительском классе
    # и при наследовании автоматически имеется у дочернего класса.
    def get_week_stats(self):
        super().get_week_stats()
