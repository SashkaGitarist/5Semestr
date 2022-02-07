import MySQLdb

visited_rules = []

# TODO перелистывание на другое право, когда право уже использовалось


def obrabotka(dict: dict, rule):

    global visited_rules
    print(f"Вы выбрали правило - {rule} и он относится к факту на тему: \"{dict[rule][0]}\"")
    visited_rules.append(rule)

    print(f"Посещенные правила: {visited_rules}")

    tr_or_fal = int(input("1 или 0: "))
    if tr_or_fal == 1:
        tr_or_fal = True
    else:
        tr_or_fal = False

    if tr_or_fal and not(rule in visited_rules):
        print(f"Вы выбрали {tr_or_fal} и он переназначает в {dict[rule][1][0]} правило")
        obrabotka(dict_rule, dict[rule][1][0])

    elif tr_or_fal == False and not(rule in visited_rules):
        print(f"Вы выбрали {tr_or_fal} и он переназначает в {dict[rule][2][0]} правило")
        obrabotka(dict_rule, dict[rule][2][0])
    else:
        print(rule in visited_rules)
        print("Я вышла из цикла")

        pass


#  подключение к БД
db = MySQLdb.connect("localhost", "root", "", "labka")
res = db.cursor()
print("Даешь подсоединение к БД!!\n")

sqlquery = "select * from facts"

res.execute(sqlquery)
#  db.commit()

dict_rule = {}
for row in res:
    # row[0] - id
    # row[1] - fact
    # row[2] - valTrue
    # row[3] - valFalse
    # row[4] - idTrue
    # row[5] - idFalse
    # row[6] - idRules
    # row[7] - priceTrue
    # row[8] - priceFalse

    # Создаем словарь с правилами, где ключ - rule,
    # val[0] - fact, val[1] - переход по true, val[2] - переход по false
    dict_rule[row[6]] = [row[1], [row[4], row[7]], [row[5], row[8]]]
    print(row)

key_choise = dict_rule.keys()
print(key_choise)
flag = True
attempt = 0
while flag:
    rule_choice = int(input("\nВведите номер правила с которого хотите начать: "))
    if rule_choice == 1:
        obrabotka(dict_rule, rule_choice)
        flag = False

    elif rule_choice == 2:
        obrabotka(dict_rule, rule_choice)
        flag = False

    elif rule_choice == 3:
        obrabotka(dict_rule, rule_choice)
        flag = False

    elif rule_choice == 4:
        obrabotka(dict_rule, rule_choice)
        flag = False

    elif rule_choice == 5:
        obrabotka(dict_rule, rule_choice)
        flag = False

    else:
        break
"""

# sqlinsert = "insert into facts (id, fact, valueTrue, valueFalse, idTrue, idFalse, idRules, priceTrue, priceFalse) " \
            # "values (5, 'cleaning', 'True', 'False', 3, 1, 5, 30, 0)"
# res.execute(sqlinsert)
# db.commit()

db.close()

