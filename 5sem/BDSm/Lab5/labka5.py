import json
import urllib.request
import xml.dom.minidom as minidom


def get_data(xml_url):
    try:
        web_file = urllib.request.urlopen(xml_url)
        return web_file.read()
    except:
        pass


def get_currencies_dictionary(xml_content, filter):
    dom = minidom.parseString(xml_content)
    dom.normalize()

    elements = dom.getElementsByTagName("Valute")
    currency_dict = {}

    if filter == 1:
        # Вывод полной информации по валюте
        for node in elements:
            for child in node.childNodes:
                # print(child) - данные из Valute
                # print(child.firstChild.data)
                if child.nodeType == 1:

                    if child.tagName == 'NumCode':
                        if child.firstChild.nodeType == 3:
                            num_code = child.firstChild.data

                    if child.tagName == 'CharCode':
                        if child.firstChild.nodeType == 3:
                            char_code = child.firstChild.data

                    if child.tagName == 'Nominal':
                        if child.firstChild.nodeType == 3:
                            nominal = child.firstChild.data

                    if child.tagName == 'Name':
                        if child.firstChild.nodeType == 3:
                            name = child.firstChild.data
                            arname = []
                            for i in name:
                                arname.append(i)
                            strname = "".join(arname)

                    if child.tagName == 'Value':
                        if child.firstChild.nodeType == 3:
                            value = float(child.firstChild.data.replace(',', '.'))

            currency_dict[num_code] = {
                'Name': strname,
                'CharCode': char_code,
                'Value': value,
                'Nominal': nominal
            }
    else:
        # Вывод данных по валюте по фильтру: "Валюта - стоимость"
        # Наполнение массива данными
        for node in elements:
            # print(node) - Valute
            for child in node.childNodes:
                # print(child) - данные из Valute
                if child.nodeType == 1:
                    if child.tagName == 'Value':
                        if child.firstChild.nodeType == 3:
                            value = float(child.firstChild.data.replace(',', '.'))
                    if child.tagName == 'CharCode':
                        if child.firstChild.nodeType == 3:
                            char_code = child.firstChild.data
                    if child.tagName == 'Nominal':
                        if child.firstChild.nodeType == 3:
                            nominal = child.firstChild.data
            currency_dict[char_code] = value
    return currency_dict


if __name__ == '__main__':

    while True:
        try:
            filter = int(input('Введите число '))
            if (filter == 1) or (filter == 2):
                break
            else:
                print('Неверное число!!!!\n')
        except:
            print("Ошибка - это не число")

    url = 'https://www.cbr.ru/scripts/XML_daily.asp'
    currency_dict = get_currencies_dictionary(get_data(url), filter)
    currency_JSON = json.dumps(currency_dict, indent=4, ensure_ascii=False)
    print(currency_JSON)
