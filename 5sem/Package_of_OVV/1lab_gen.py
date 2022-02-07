import random
import csv

word = ''
word_length = int(input("Введите длину слова: "))
for i in range(word_length):
    word += str(random.randint(0, 1))

with open("DSM_word", "w") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(word)
