import os
import time
import webbrowser
import tkinter as tk
from threading import Thread


def send_messages_from_file(file_path, sent_numbers_file, interface):
    with open(file_path, 'r', encoding='utf-8') as file:
        phone_numbers = file.readlines()

    phone_numbers = [number.strip() for number in phone_numbers]

    if os.path.exists(sent_numbers_file):
        with open(sent_numbers_file, 'r', encoding='utf-8') as file:
            sent_numbers = file.read().splitlines()
    else:
        sent_numbers = []

    for number in phone_numbers:
        if number in sent_numbers:
            print(f"пропускаем {number}")
            continue

        try:
            phone_numbers_url = f'https://wa.me/{number}'
            webbrowser.open(phone_numbers_url)
            print(f"перенаправлен на {number}")
            sent_numbers.append(number)

            # Update the GUI with the message
            interface.update_message(number, success=True)

            with open(sent_numbers_file, 'a', encoding='utf-8') as file:
                file.write(number + '\n')

            time.sleep(15)  # Delay for the user

        except Exception as e:
            print(f"ошибка при отправке на {number}: {e}")
            # Update the GUI with an error message
            interface.update_message(number, success=False)


class SimpleInterface:
    def __init__(self, master):
        self.master = master

        self.master.title("Простой интерфейс")
        self.master.geometry("600x600")
        self.output_label = tk.Label(master, text="", font=("Helvetica", 14))
        self.output_label.pack(pady=10)

        self.timer_seconds = 15  # Set your timer duration in seconds
        self.timer_label = tk.Label(master, text="Time left: " + str(self.timer_seconds), font=("Helvetica", 16))
        self.timer_label.pack(pady=20)

        self.start_timer()

    def start_timer(self):
        self.update_timer()

    def update_timer(self):
        if self.timer_seconds > 0:
            self.timer_seconds -= 1
            self.timer_label.config(text="Time left: " + str(self.timer_seconds))
            self.timer_label.after(1000, self.update_timer)  # call this function every second
        else:
            self.timer_label.config(text="Time is up! Restarting timer...")
            self.timer_seconds = 30  # Reset the timer
            self.start_timer()  # Restart the timer

    def update_message(self, number, success=True):
        if success:
            message = f"перенаправлен на {number}"
        else:
            message = f"ошибка при перенаправлении на {number}"
        self.output_label.config(text=message)


def start_sending_messages(file_path, sent_numbers_file):
    root = tk.Tk()
    app = SimpleInterface(root)

    # Start a separate thread to run the message sending function
    thread = Thread(target=send_messages_from_file, args=(file_path, sent_numbers_file, app))
    thread.start()

    root.mainloop()


if __name__ == "__main__":
    file_path = 'phone_numbers.txt'
    sent_numbers_file = 'sent_numbers.txt'
    start_sending_messages(file_path, sent_numbers_file)