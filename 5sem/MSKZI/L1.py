from collections import Counter

WORDD = 'УИРГЯОЕШЭИРОЦРУИРЫЩЭЧОРЩЭМЕГЧЭЮРЙЖЗЩТУЕЭИЙЮУЦЫРЩЭРЯВИУЦЫРАУЧСРЬЩМИФЭМЯЖПЧЫРЩРГИЙЩМЩШРЧРЕГОЧУЧФЭ ЕЭЧМУЩШРНЧТУЧРЬЯФЭЮРВЧЭЕЖЭРИФЙЧРМЩФЬ ЧОЯЭРЧЫРАЕАРВЧФЭЦШРМЦОЦФИЙРМРЩГУЩОР ЛГЯРФР ЩОЕУЕОЧРЫЕССЕ ГЕРЧРЯДЙЙФЕРФЩВЧУИУЧЛОЧРЩРАЩФОЩФИРЧРЩРЬИПИ УЩОРВИЙЩМИАИРАУЧСЧРДЭЧРУЧАЩОЯРУИРЬЩМ ИГЛЭ'

wordd = 'УИ ГЯОЕШЭИ ОЦ УИ ЫЩЭЧО ЩЭМЕГЧЭЮ ЙЖЗЩТУЕЭИЙЮУЦЫ ЩЭ ЯВИУЦЫ АУЧС ЬЩМИФЭМЯЖПЧЫ Щ ГИЙЩМЩШ Ч ЕГОЧУЧФЭ_ЕЭЧМУЩШ ' \
        'НЧТУЧ ЬЯФЭЮ ВЧЭЕЖЭ ИФЙЧ МЩФЬ_ЧОЯЭ ЧЫ АЕА ВЧФЭЦШ МЦОЦФИЙ М ЩГУЩО _ЛГЯ Ф _ЩОЕУЕОЧ ЫЕССЕ_ГЕ Ч ЯДЙЙФЕ ' \
        'ФЩВЧУИУЧЛОЧ Щ АЩФОЩФИ Ч Щ ЬИПИ_УЩО ВИЙЩМИАИ АУЧСЧ ДЭЧ УЧАЩОЯ УИ ЬЩМ_ИГЛЭ '

fr_r_list = ['  ', 'О', 'Е', 'А', 'И', 'Н', 'Т', 'С', 'Р', 'В', 'Л', 'К', 'М', 'Д', 'П', 'У', 'Я', 'Ы', 'Ь', 'Г', 'З',
             'Б', 'Ч', 'Й', 'Х', 'Ж', 'Ш', 'Ю', 'Ц', 'Щ', 'Э', 'Ф']


def calculate_frequency(dd: dict, ll: list):
    freqs = Counter(''.join(WORDD.splitlines()))
    for symbol, count in freqs.most_common():
        print(symbol, " - ", count)
        dd[symbol] = count
        ll.append(symbol)


def find_normal_string(freq_word: list, text: str):
    text.replace()


def main():
    freq_rus_word = []
    # Словарь, где используется способ записи: "буква: кол-во букв в слове"
    word_dict = dict()
    # Список, в котором написаны буквы с их популярностью в слове
    word_list = list()
    # Создание списка по слову, который мы получаем на вход
    wordd_list = list(WORDD)
    # Обращение к функции для подсчета популярности
    calculate_frequency(word_dict, word_list)

    flag = True
    print(word_list)
    while flag:
        # print(freq_rus_let[i], end="")

        # Фигня для замены букв в входящем слове
        # Работа состоит в том, что мы заменяем
        for i in range(len(word_list)):
            # Если текущий символ совпадает
            if word_list[i] == wordd_list:
                print("Dsd")

        output = "".join(wordd_list)
        print(output)
        flag = False


if __name__ == '__main__':
    main()
