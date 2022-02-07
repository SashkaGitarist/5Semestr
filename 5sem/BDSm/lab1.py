import sys

from mysql.connector import MySQLConnection, Error

from pth_mysql_config import read_db_config

from collections import namedtuple, deque

Fact = namedtuple('Fact', 'Fact valueTrue valueFalse idTrue idFalse idRules priceTrue priceFalse')


def query_get_idRules(idRules):
    try:
        dbconfig = read_db_config('config.ini')
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        query = "SELECT * FROM facts WHERE idRules=" + str(idRules)
        cursor.execute(query)
        rows_fact = cursor.fetchall()

        facts = [Fact(row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]) for row in rows_fact]
        # print(facts)
    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()
    return facts


def query_with_fetchall():
    try:
        dbconfig = read_db_config('config.ini')
        connect = MySQLConnection(**dbconfig)
        cursor = connect.cursor()
        cursor.execute("SELECT DISTINCT(idRules) FROM facts")
        rows_fact = cursor.fetchall()
        print('Доступные правила: ')
        print([row[0] for row in rows_fact])

    except Error as e:
        print(e)

    finally:
        cursor.close()
        connect.close()


def get_result(results_list, price_list):
    # print(results_list)
    sum = 0
    for price in price_list:
        sum += price
    print("\nИсходя из Ваших решений, система говорит, что эта работа: ")
    if 40 <= sum < 80:
        print("✍не шик, но под пиво сойдет✍")
    elif sum >= 80:
        print("ШЕДЕЕЕЕЕВР!")
    elif 40 > sum >= 20:
        print("Более менее, но лучше найти другую")
    elif sum < 20:
        print("Ужас полный...")

    print("\nСистема сделала данный выбор на основе: \nОбщее количество набранных баллов = " + str(sum))
    for result in results_list:
        for i in range(len(result) - 1):
            print("Выбранное правило " + str(result[0]) + "\nВаш ответ: " + str(result[i + 1]) + "\n")


def main():
    facts_q = deque()  # Рабочая память - храним текущие факты из правил
    result_remove = list()  # блок учёта выбивших
    results_answer = list()  # блок учёта ответов
    numbers = list()  # список с номерами правил которые были использованы при анализе
    result_answer = list()  # список с набором ответов для одного правила
    price_list = list()  # список с набором оценок для каждого факта
    try:
        # print("Факты: ")
        query_with_fetchall()
        idRules = int(input('Введите номер правила с которого хотите начать: '))
        facts = query_get_idRules(idRules)  # Рабочая память - храним все факты правила
        for fact in facts:
            facts_q.append(fact)
        while (facts_q):
            fact = facts_q.popleft()
            if fact.idRules not in numbers:
                numbers.append(fact.idRules)
                results_answer.append(result_answer)
                result_answer = list()
                result_answer.append(fact.idRules)

            print("\nНеобходимо ли Вам на работе " + fact.Fact + "? Варианты: {" + fact.valueTrue + ", " + fact.valueFalse + "}")
            answer_value = input('Введите Ваш ответ (True - если да, False - если нет):')

            if fact not in result_remove:
                result_remove.append(fact)
                if fact.valueTrue == answer_value:
                    if fact.idTrue != None:
                        facts_new = query_get_idRules(fact.idTrue)
                        for fact_new in facts_new:
                            if fact_new not in result_remove:
                                facts_q.append(fact_new)
                    result_answer.append(str(fact.Fact) + "=" + str(answer_value) + " его \"вес\"=" + str(fact.priceTrue))
                    price_list.append(fact.priceTrue)

                elif fact.valueFalse == answer_value:
                    if fact.idFalse != None:
                        facts_new = query_get_idRules(fact.idFalse)
                        for fact_new in facts_new:
                            if fact_new not in result_remove:
                                facts_q.append(fact_new)
                    result_answer.append(str(fact.Fact) + "=" + str(answer_value) + " его \"вес\"=" + str(fact.priceFalse))
                    price_list.append(fact.priceFalse)
                else:
                    print("Error")
            # print(result_remove, " remove")
        results_answer.append(result_answer)
        results_answer.pop(0)
        get_result(results_answer, price_list)

    except KeyboardInterrupt:
        sys.exit()


if __name__ == '__main__':
    main()

    input("Нажмите любую клавишу: ")
