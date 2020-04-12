from os import listdir

from .model_creator import ModelCreator
from templates.models_header import header


class DjangoModelsCreator:
    """
    General creator class
    """
    def __init__(self, folder_path: str):
        """
        folder_path: string
        Path to folder with csv-files
        """
        self.folder_path = folder_path
        self.file_code = header

    def __handle_csv(self):
        """
        Parse csv-files and creates models for Django ORM
        """
        files = listdir(self.folder_path)

        if files:
            print(f'Found {len(files)} files')
            file_names = [file for file in files if '.csv' in file]

            if file_names:
                for file_name in file_names:
                    file_path = f'{self.folder_path}{file_name}'
                    model_creator = ModelCreator(file_path, file_name)
                    self.file_code += model_creator.create_model()
                    print(f'Model from {file_name} has been created')

            else:
                raise FileNotFoundError('Cannot find csv-files in specified folder. Please check your folder_path')

    def __export_models(self):
        """
        Export created models to models.py file
        """
        print('Exporting...')

        with open('models.py', 'w') as f:
            f.write(self.file_code)

        print('Finished!')

    def create_models(self):
        """
        Parse csv-files and export models to models.py file
        """
        self.__handle_csv()
        self.__export_models()
