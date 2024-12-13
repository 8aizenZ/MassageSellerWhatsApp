import pywhatkit as kit
import time
import os
import random


def send_messages_from_file(file_path, sent_numbers_file):
    with open(file_path, 'r', encoding='utf-8') as file:
        phone_numbers = file.readlines()

    phone_numbers = [number.strip() for number in phone_numbers]

    if os.path.exists(sent_numbers_file):
        with open(sent_numbers_file, 'r', encoding='utf-8') as file:
            sent_numbers = file.read().splitlines()
    else:
        sent_numbers = []

    now = time.localtime()
    hour = now.tm_hour
    minute = now.tm_min + 1

    for number in phone_numbers:
        if number in sent_numbers:
            print(f"пропускаем {number}")
            continue

        try:
            kit.sendwhatmsg(number, "куку", hour, minute)
            print(f"отправлено на {number}")
            sent_numbers.append(number)

            with open(sent_numbers_file, 'a', encoding='utf-8') as file:
                file.write(number + '\n')

            time.sleep(10)
        except Exception as e:
            print(f"ошибка при отправке на {number}: {e}")