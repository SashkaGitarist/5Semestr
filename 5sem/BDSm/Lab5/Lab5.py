def get_filter(filter):
    try:
        if filter == 1:
            return print(11)
        elif filter == 2:
            return print(22)
    except:
        return print("Ввели некорректное число")


if __name__ == "__main__":
    get_filter(int(input("№ фильтра: ")))
