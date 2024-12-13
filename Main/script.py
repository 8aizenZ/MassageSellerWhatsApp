import os
import time
import webbrowser
import tkinter as tk
from threading import Thread


class MessageSenderApp:
    def __init__(self,master):
        self.master = master
        self.master.geometry("300x300")



        self.timer_seconds = 15  # Set your timer duration in seconds
        self.timer_label = tk.Label(root, text="Time left: " + str(self.timer_seconds), font=("Helvetica", 16))
        self.timer_label.pack(pady=20)

        self.start_timer()

        # Define UI components for file selection and message sending (not included here)
        # ...

    def start_timer(self):
        self.update_timer()  # Start the timer update process

    def update_timer(self):
        if self.timer_seconds > 0:
            self.timer_seconds -= 1
            self.timer_label.config(text="Time left: " + str(self.timer_seconds))
            self.timer_label.after(1000, self.update_timer)  # call this function every second
        else:
            self.timer_label.config(text="Time is up! Restarting timer...")
            self.timer_seconds = 30  # Reset the timer
            self.start_timer()  # Restart the timer

    def send_messages_from_file(self, file_path, sent_numbers_file):
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
                print(f"Skipping {number}")
                continue

            try:
                phone_numbers_url = f'https://wa.me/{number}'
                webbrowser.open(phone_numbers_url)
                print(f"Redirecting to {number}")
                sent_numbers.append(number)

                # Update the GUI with the message (this assumes you have a method to update the UI)
                # self.update_message(number, success=True)

                with open(sent_numbers_file, 'a', encoding='utf-8') as file:
                    file.write(number + '\n')
                time.sleep(1)  # Delay to avoid opening too many tabs at once

            except Exception as e:
                print(f"An error occurred: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = MessageSenderApp(root)
    root.mainloop()