from datetime import datetime
from typing import Union, List

import pandas as pd
from pandas import DataFrame
from streamlit.runtime.uploaded_file_manager import UploadedFile

from src.clear_file import BaseClearDataFile
from src.views.FilterMessagesViewModel import FilterMessagesViewModel
from src.views.InforAmountOfDatesViewModel import InforAmountOfDatesViewModel


class SearchWhatsappStreamlit(BaseClearDataFile):
    def __init__(self, file_data: Union[UploadedFile, List[UploadedFile], None]):
        file_data: List[str] = file_data.getvalue().decode("utf-8").split("\n")
        super().__init__(file_data)

        self.__df_messages: DataFrame = pd.DataFrame([m.__dict__ for m in self.messages])
        self.__df_info_messages: DataFrame = pd.DataFrame([m.__dict__ for m in self.info_messages])

    @property
    def df_messages(self) -> DataFrame:
        return self.__df_messages

    @property
    def df_info_messages(self) -> DataFrame:
        return self.__df_info_messages

    @property
    def amount_of_messages(self) -> int:
        return len(self.df_messages)

    @property
    def amount_of_info_messages(self) -> int:
        return len(self.df_info_messages)

    @property
    def amount_of_numbers(self) -> int:
        return len(self.df_messages['phone'].unique())

    @property
    def init_date(self) -> datetime:
        return self.df_messages['date'].min()

    @property
    def end_date(self) -> datetime:
        return self.df_messages['date'].max()

    def get_init_date_format(self, strftime: str) -> str:
        return self.df_messages['date'].min().strftime(strftime)

    def get_end_date_format(self, strftime: str) -> str:
        return self.df_messages['date'].max().strftime(strftime)

    @property
    def amount_of_media(self) -> int:
        return len(self.df_messages[self.df_messages['message'].str.contains('<Arquivo de mídia oculto>')])

    @property
    def list_of_numbers(self) -> List[str]:
        return self.df_messages['phone'].unique()

    def get_contains_in_message(self, message: str) -> DataFrame:
        return self.df_messages[self.df_messages['message'].str.contains(message)]

    def get_contains_isin_message(self, message: List[str]) -> DataFrame:
        return self.df_messages[self.df_messages['message'].isin(message)]

    def filter_messages(self, message: str, numbers: int, init_date: datetime,
                        end_date: datetime) -> FilterMessagesViewModel:
        df_filter = self.df_messages

        amount_filter = 0
        qtd_numbers = 0

        if message:
            df_filter = self.get_contains_in_message(message)
            amount_filter = len(df_filter)

        if numbers:
            df_filter = df_filter[df_filter['phone'].isin(numbers)]
            amount_filter = len(df_filter)

        if init_date and end_date:
            df_filter['date'] = pd.to_datetime(df_filter['date'])

            df_filter = df_filter[
                (df_filter['date'] >= init_date.strftime('%Y-%m-%d')) &
                (df_filter['date'] <= end_date.strftime('%Y-%m-%d'))
                ]

            amount_filter = len(df_filter)

        df_filter.rename(columns={'phone': 'Contato', 'date': 'Data', 'message': 'Mensagem'})
        return FilterMessagesViewModel(
            amount_filter=amount_filter,
            amount_numbers=qtd_numbers,
            data_frame=df_filter)

    @classmethod
    def graphic_filter_messages(cls, filter_dataframe: DataFrame) -> DataFrame:
        filter_dataframe.loc[:, 'just_hour_int'] = filter_dataframe['date'].apply(lambda x: x.hour)
        filter_dataframe.loc[:, 'just_hour'] = filter_dataframe['date'].apply(lambda x: x.time().strftime('%H:%M:%S'))

        df_data = filter_dataframe.groupby('just_hour_int')['just_hour'].count().reset_index()
        df_data['just_hour_int'] = df_data['just_hour_int'].apply(lambda x: str(x) + 'h')
        df_data.rename(columns={'just_hour_int': 'Horário', 'just_hour': 'Mensagens'}, inplace=True)
        return df_data

    def get_info_amount_dates(self) -> InforAmountOfDatesViewModel:
        """
        Este método retorna um objeto com informações sobre a quantidade de mensagens por tempo(Em geral, por dia)
        """
        df_messages = self.df_messages

        # Cria uma nova coluna com a data sem a hora
        df_messages["just_date"] = df_messages.apply(lambda x: x['date'].date(), axis=1)
        # Transforma a coluna just_date em datetime
        df_messages['just_date'] = pd.to_datetime(df_messages['just_date'])
        # Cria um novo dataframe com a soma das mensagens por dia
        df_data = df_messages.groupby('just_date')['message'].count().reset_index()

        df_data.rename(columns={'just_date': 'Data', 'message': 'Quantidade de mensagens'}, inplace=True)

        avg_per_day: int = df_data['Quantidade de mensagens'].mean()
        avg_per_week: int = avg_per_day * 7
        avg_per_month: int = avg_per_day * 30
        amount_of_days: int = len(df_data)

        day_with_more_messages: str = df_data["Data"][df_data["Quantidade de mensagens"].idxmax()].strftime("%d/%m/%Y")
        day_with_less_messages: str = df_data["Data"][df_data["Quantidade de mensagens"].idxmin()].strftime("%d/%m/%Y")

        amout_day_more_messages: int = df_data["Quantidade de mensagens"].max()
        amout_day_less_messages: int = df_data["Quantidade de mensagens"].min()

        return InforAmountOfDatesViewModel(
            data_frame=df_data,
            amount_od_days=amount_of_days,
            day_with_more_messages=day_with_more_messages,
            day_with_less_messages=day_with_less_messages,
            average_per_day=round(avg_per_day),
            average_per_week=round(avg_per_week),
            average_per_month=round(avg_per_month),
            amout_day_more_messages=round(amout_day_more_messages),
            amout_day_less_messages=round(amout_day_less_messages),
        )

    def get_message_rating_by_person(self) -> DataFrame:
        df_data = self.df_messages.groupby('phone')['message'].count().reset_index()

        df_data.rename(columns={'phone': 'Pessoa', 'message': 'Quantidade de mensagens'}, inplace=True)

        df_data = df_data.sort_values(by='Quantidade de mensagens', ascending=True)
        return df_data

    @classmethod
    def rename_column_data_frame(cls, df: DataFrame, renames: dict) -> DataFrame:
        df.rename(columns=renames, inplace=True)
        return df
