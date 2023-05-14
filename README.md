<div align="center">
    <h1>Coffee and Wi-fi ☕</h1>
    <div>
        <img src="docs/assets/website-demo.gif"  alt="Coffee and Wi-fi Website">
    </div>
</div>

## About

This project is a merge of projects from days 62 and 66 of 100 Days of Code.
- Day 62: A coffee shop review site where the user can add their review by filling out a form. This project uses **Flask**, **WTForms** and **Bootstrap** and persists the data to a csv.
- Day 66: REST API to manipulate cafe data.

New:
- Revamped front-end
- Stores the data in an **SQLite** database
- Uses **Peewee** micro ORM instead of **SQLAlchemy** ORM
- Uses **flask_restx** for REST API building and endpoint documentation using the **Swagger UI**
- Uses **Pytest** for testing
- Uses **Dynaconf** for per-environment configuration management (DEV, TEST, PROD)

## Tools used
<div>
    <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" width="40" alt="Python" title="Python">&ensp;
    <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/flask/flask-original.svg" width="40" alt="Flask" title="Flask">&ensp;
    <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/sqlite/sqlite-original.svg" width="40" alt="SQLite" title="SQLite">&ensp;
    <img src="docs/assets/peewee-logo.svg" width="60" alt="Peewee" title="Peewee">&ensp;
    <img src="docs/assets/dynaconf-logo.svg" width="40" alt="Dynaconf" title="Dynaconf">&ensp;
    <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/pytest/pytest-original.svg" width="40" alt="Pytest" title="Pytest">&ensp;
    <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/html5/html5-original.svg" width="40" alt="HTML5" title="HTML5">&ensp;
    <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/css3/css3-original.svg" width="40" alt="CSS3" title="CSS3">&ensp;
    <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/javascript/javascript-original.svg" width="40" alt="Javascript" title="Javascript">&ensp;
    <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/bootstrap/bootstrap-original.svg" width="40" alt="Bootstrap" title="Bootstrap">
</div>

## How to install and run

1. Clone the project.
2. Create an `.env` file in the root of the project and define the following variables:
    
    ```properties
    FLASK_ENV="development"
    FLASK_APP="coffee_and_wifi"
    FLASK_SECRET_KEY="your SECRET KEY here"
    ```
    Use the following command to create a **SECRET KEY**: `python -c 'import secrets; print(secrets.token_hex())'`
3. Open the terminal from the project folder and install by running:
    ```
    poetry install
    ```
4. Run the app:
   ```
   flask --debug run
   ```

## How to run the tests

Once you have installed the project, run:
``` 
task test
```

## Author

-   [Igor Ferreira](https://github.com/ig0r-ferreira)

## License

This project is under license from [MIT](LICENSE).