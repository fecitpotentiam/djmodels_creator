import pandas as pd

from utils.service import is_max_int, roundup


class ModelCreator:
    """
    Model creator class
    """
    def __init__(self, file_path: str, file_name: str):
        """
        :param file_path: Path to csv file
        :param file_name: CSV_file's name
        """
        self.file_path = file_path
        self.file_name = file_name
        self.model_name = str()
        self.df = None

    @staticmethod
    def __refactor_name(value: str) -> str:
        """
        :param value: Raw csv-table name
        :return: Table name refactored to Django ORM standard style
        """
        value = value.title()
        delimiter = str()

        if '-' in value:
            delimiter = '-'
        if '_' in value:
            delimiter = '_'

        if delimiter:
            splitted_value = value.split(delimiter)
            value = ''.join([split.title() for split in splitted_value])

        return value

    def __create_model_name(self):
        """
        Create Django ORM standard model name from csv-filename
        """
        self.model_name = self.file_name.replace('.csv', '')
        self.model_name = self.__refactor_name(self.model_name)

    def __get_nullable_columns(self) -> list:
        """
        :return: Get list of columns containing nullable values from dataframe
        """
        return list(self.df.columns[self.df.isnull().any()])

    def __get_column_types(self) -> dict:
        """
        :return: Get a dictionary {column_name:column_type} from dataframe
        """
        return {column: str(value) for column, value in self.df.dtypes.to_dict().items()}

    @staticmethod
    def __is_date(column_name: str) -> bool:
        """
        :return: is column "DateField" type
        """
        if 'date' in column_name or 'birthday' in column_name:
            return True

        return False

    @staticmethod
    def __is_datetime(column_name: str, values: list) -> False:
        """
        :return: is column "DateTimeField" type
        """
        if 'created' in column_name or 'updated' in column_name:
            return True

        datetime_columns = [True for value in values if str(value)[-1] == 'Z' and ':' in str(value)]
        if datetime_columns:
            return True

        return False

    def __get_object_field(self, column_name) -> str:
        """
        Handle "object" type columns
        :return: Django ORM field
        """
        values = self.df[column_name].values
        values_lengths = [len(str(value)) for value in values if str(value) != 'nan']
        max_value = max(values_lengths)

        if self.__is_date(column_name):
            field = 'DateField()'
        elif self.__is_datetime(column_name, values):
            field = 'DateTimeField()'
        else:
            field = 'TextField()' if max_value > 300 else f'CharField(max_length={roundup(max_value)})'

        return field

    def __get_digit_field(self, column_name: str) -> str:
        """
        Handle "int64" and "float64" type columns
        :return: Django ORM field
        """
        values = self.df[column_name].values

        field = 'BigIntegerField()' if is_max_int(values) else 'IntegerField()'

        for value in values:
            if str(value.item()) != 'nan' and isinstance(value.item(), float):
                field = 'FloatField'

        return field

    def create_model(self) -> str:
        """
        Create Django model from csv-file
        :return: Django ORM model
        """
        self.__create_model_name()
        self.df = pd.read_csv(self.file_path)

        null_columns = self.__get_nullable_columns()
        column_types = self.__get_column_types()

        model_code = f"class {self.model_name}(models.Model):\n"

        for column_name, column_type in column_types.items():
            if column_type == 'object':
                field_type = self.__get_object_field(column_name)
            elif column_type == 'int64' or column_type == 'float64':
                field_type = self.__get_digit_field(column_name)
            else:
                field_type = 'Unknown'

            if column_name in null_columns:
                field_type = (field_type.replace('()', '(null=True)') if '()' in field_type
                              else field_type.replace(')', ', null=True)'))

            model_field = f'    {column_name} = {field_type}\n'
            model_code += model_field

        model_code += '\n\n'
        return model_code
