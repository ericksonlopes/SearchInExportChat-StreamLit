import re
from datetime import datetime
from typing import List

from models import MessageModel, InfoMessageModel


class BaseClearDataFile:
    def __init__(self, file_data):
        super().__init__()

        self.__messages: List[MessageModel] = []
        self.__info_messages: List[InfoMessageModel] = []

        self.__file_data = file_data
        self.__read_file()

    @property
    def messages(self) -> List[MessageModel]:
        """get messages"""
        return self.__messages

    @property
    def info_messages(self) -> List[InfoMessageModel]:
        """get info messages"""
        return self.__info_messages

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

        except Exception as error:
            raise error


if __name__ == '__main__':
    x = open('../tests/test_file_folder/test_group.txt', 'r')
    file = BaseClearDataFile(file_data=x)
    print(file.messages)
    print(file.info_messages)
