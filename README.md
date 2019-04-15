# ricommender
Multi-context Music Recommender System Project

## Music Extractor

### Dependencies
- LibROSA
- Numpy
- EyeD3

### Required Folders
*musics* with mp3 files inside

### Extracting Features
```
python music_extractor.py <extraction_type> <folder_name> <csv_filename>
```

Args:
- `extraction_type` with either *extract_music* or *extract_music_frame*
- `folder_name` with the name of to-be-extracted folder
- `csv_filename` with the file name of csv file

## Ricommender Backend

### Dependencies

#### PyPI Dependencies

- Django
- Django REST Framework
- Pandas
- Django Pandas
- Djongo (for MongoDB)

#### Software Dependencies
- MongoDB (`sudo apt-get install -y mongodb-org`)

### MongoDB Service Operations
- Starting MongoDB
    ```
    sudo service mongod start
    ```

- Stopping MongoDB
    ```
    sudo service mongod stop
    ```




### How to Install

1. Enter the following command
    ```pipenv install```

2. Edit `.env` file as necessary, use a shortcut by entering the following command
    ```cp .env.example .env```

3. Enter the shell of pipenv
    ```pipenv shell```

4. Turn on MongoDB database
    ```mongod --dbpath <path_to_db>```

5. Run migrations
    ```python manage.py migrate```

6. (OPTIONAL) Import music metadata CSV to MongoDB
    ```mongoimport -d <database_name> -c <collection> --type csv --file <csv_file> --headerline```

7. Run the Django server
    ```python manage.py runserver```

### Creating admin
1. Enter this command
    ```python manage.py createsuperuser```

2. Enter the required credentials

## Author
Ferdinandus Richard
