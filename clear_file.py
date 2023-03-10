import os
import re
from datetime import datetime
from typing import List

from loguru import logger

from models import MessageModel, InfoMessageModel


class BaseClearDataFile:
    def __init__(self, pathfile: str = "", file_data=None):
        super().__init__()

        self.__path_file: str = pathfile
        self.__name_file: str = self.__get_base_name_file()
        self.__messages: List[MessageModel] = []
        self.__info_messages: List[InfoMessageModel] = []

        if file_data:
            self.__file_data = file_data
        else:
            self.__verify_if_file_exists()
            self.__file_data = self.__open_file()

        self.__read_file()

    @property
    def messages(self) -> List[MessageModel]:
        """get messages"""
        return self.__messages

    @property
    def info_messages(self) -> List[InfoMessageModel]:
        """get info messages"""
        return self.__info_messages

    @property
    def path_file(self) -> str:
        """get file path"""
        return self.__path_file

    @property
    def name_file(self) -> str:
        """get name file"""
        return self.__name_file

    def __get_base_name_file(self) -> str:
        """get base name file"""
        return os.path.basename(self.__path_file)

    def __get_absolute_path_file(self) -> str:
        """get absolute path file"""
        return os.path.abspath(self.__path_file)

    def __verify_if_file_exists(self) -> None:
        """verify if file exists"""
        if not os.path.exists(self.__path_file):
            logger.warning(f'File {self.__path_file} not found')
            raise FileNotFoundError(f'File {self.__path_file} not found')

    def __open_file(self) -> List[str]:
        """open file"""
        with open(self.__get_absolute_path_file(), encoding='utf-8') as file:
            lines = file.readlines()
        return lines

    def __read_file(self) -> None:
        """perform file datas cleanup"""

        try:
            lines = self.__file_data

            for line in lines:
                find_message_phone = re.compile(r'(\d{2}/\d{2}/\d{4} \d{2}:\d{2}) - (.*?): (.*)',
                                                flags=re.MULTILINE)
                find = find_message_phone.findall(line)

                if find:
                    message = MessageModel(phone=find[0][1], message=' '.join(find[0][2].split()),
                                           date=datetime.strptime(f"{find[0][0]}", '%d/%m/%Y %H:%M'))
                    self.messages.append(message)
                    continue

                find_regex_system = re.compile(r'(\d{2}/\d{2}/\d{4} \d{2}:\d{2}) - (.*)', flags=re.MULTILINE)
                find2 = find_regex_system.findall(line)

                if find2:
                    info_message = InfoMessageModel(date=datetime.strptime(f"{find2[0][0]}", '%d/%m/%Y %H:%M'),
                                                    message=find2[0][1])
                    self.info_messages.append(info_message)
                    continue

                self.messages[-1].concatenate(f" {' '.join(line.split())}")
                logger.info(f'Successfully read {self.__path_file}')

        except Exception as error:
            logger.error(error)
            raise error


if __name__ == '__main__':
    x = open('../tests/test_file_folder/test_group.txt', 'r')
    file = BaseClearDataFile(file_data=x)
    print(file.messages)
    print(file.info_messages)
