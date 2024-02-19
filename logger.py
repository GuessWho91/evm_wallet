import os
import time
from datetime import date
from pathlib import Path


class W3Logger:

    def __init__(self):

        script_location = Path(__file__).absolute().parent
        today = date.today()

        folder_path = f'{script_location}/logs'
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        folder_path_results = f'{script_location}/results'
        if not os.path.exists(folder_path_results):
            os.makedirs(folder_path_results)

        self.file_path = f'{folder_path}/{today}.txt'
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w', encoding='utf-8') as file:
                file.write('')

        self.file_path_results = f'{folder_path_results}/{today}.txt'
        if not os.path.exists(self.file_path_results):
            with open(self.file_path_results, 'w', encoding='utf-8') as file:
                file.write('')

    def success(self, msg):
        with open(self.file_path, 'a+', encoding='utf-8') as file:
            msg = self.get_message(msg, 'SUCCESS')
            file.write(msg)
            print(msg)

    def error(self, msg):
        with open(self.file_path, 'a+', encoding='utf-8') as file:
            msg = self.get_message(msg, 'ERROR')
            file.write(msg)
            print(msg)

    def info(self, msg):
        with open(self.file_path, 'a+', encoding='utf-8') as file:
            msg = self.get_message(msg, 'INFO')
            file.write(msg)
            print(msg)

    def warning(self, msg):
        with open(self.file_path, 'a+', encoding='utf-8') as file:
            msg = self.get_message(msg, 'WARNING')
            file.write(msg)
            print(msg)

    def skip(self):
        with open(self.file_path, 'a+', encoding='utf-8') as file:
            file.write('\n')

    def result(self, msg, msg_type):
        with open(self.file_path_results, 'a+', encoding='utf-8') as file:
            msg = self.get_message(msg, msg_type)
            file.write(msg)
            print(msg)

    @staticmethod
    def get_message(msg, msg_type):
        return '{} | {} | {}\n'.format(time.strftime("%H:%M:%S"), msg_type.ljust(8), msg)
