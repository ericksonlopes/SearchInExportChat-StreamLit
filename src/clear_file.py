import re
from datetime import datetime
from typing import List

from loguru import logger

from src.models import MessageModel, InfoMessageModel


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

                logger.info(f"line: {line}")

            logger.info(f"messages len: {len(self.messages)}")
        except Exception as error:
            logger.error(f"Error in __read_file: {error}")
            raise error


if __name__ == '__main__':
    import pandas as pd
    x = open('../python.txt', 'r', encoding='utf-8').read().split('\n')
    base = BaseClearDataFile(file_data=x)

    df_messages = pd.DataFrame([m.__dict__ for m in base.messages])

    df_messages['date'] = pd.to_datetime(df_messages['date'])

    df_messages["newdate"] = df_messages.apply(lambda x: x['date'].date(), axis=1)

    print(df_messages['newdate'].groupby(df_messages['newdate']).count())