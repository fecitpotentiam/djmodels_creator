# djmodels_creator
Makes models.py file for Django ORM from csv files

## How to use
```
from main import DjangoModelsCreator
creator = DjangoModelsCreator('path_to_your_folder_with_csv_files')
creator.create_models()
```