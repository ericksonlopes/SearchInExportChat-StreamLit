from typing import Union, List

from streamlit.runtime.uploaded_file_manager import UploadedFile


class SearchStreamlit:
    def __init__(self, data: Union[UploadedFile, List[UploadedFile], None]):
        self.data = data

