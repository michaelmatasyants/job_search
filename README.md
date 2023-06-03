# Programming vacancies compare

This project allows you to get information on all vacancies from [superjob.ru](https://www.superjob.ru/) and [hh.ru](https://hh.ru/):
- on the specified list of programming languages
- in the region of Moscow
- in the field of programming (IT)

The obtained data is presented in the form of a table, where for each programming language is indicated:
- number of found vacancies;
- amount of processed vacancies, i.e. vacancies with salaries different from 0 and in rubles currency;
- predicted average salary for all vacancies in this programming language in rubles.

The predicted value is calculated as follows:
1. if only salary from, the given value is multiplied by 1.2
2. if only salary to is specified, this value is multiplied by 0.8
3. if the salary from and to is specified, the average value is chosen 

### How to install

1. Firstly, you have to install python and pip (package-management system) if they haven't been already installed.

2. Create a virtual environment with its own independent set of packages using [virtualenv/venv](https://docs.python.org/3/library/venv.html). It'll help you to isolate the project from the packages located in the base environment.

3. Install all the packages used in this project, in your virtual environment which you've created on the step 2. Use the `requirements.txt` file to install dependencies:
    ```console
    pip install -r requirements.txt
    ```
4. Tokens and other keys:
   You need to [register an aplication](https://www.superjob.ru/auth/login/?returnUrl=https://api.superjob.ru/register/) to get superjob token which would be used in api.


5. Create an `.env` file and locate it in the same directory where your project is. Copy and append your access token to `.env` file like this:
    ```
    TOKEN_SUPERJOB=paste_here_your_token_from_step_4
    ```
6. Remember to add `.env` to your `.gitignore` if you are going to put the project on GIT.

### How to run

Run in your console:

```Console
>>> python3 main.py
```

Output:
    
```Console
+HeadHunter Moscow------+------------------+---------------------+------------------+
| Язык программирования | Вакансий найдено | Вакансий обработано | Средняя зарплата |
+-----------------------+------------------+---------------------+------------------+
| TypeScript            | 1100             | 484                 | 162659           |
| Swift                 | 400              | 124                 | 179032           |
| Scala                 | 196              | 22                  | 240454           |
| Objective-C           | 112              | 24                  | 205000           |
| Shell                 | 168              | 40                  | 200300           |
| Go                    | 600              | 180                 | 204400           |
| C++                   | 1200             | 588                 | 191712           |
| C#                    | 900              | 378                 | 156721           |
| PHP                   | 1200             | 864                 | 126490           |
| Ruby                  | 164              | 32                  | 260687           |
| Python                | 1500             | 690                 | 129826           |
| Java                  | 1600             | 688                 | 179872           |
| JavaScript            | 2100             | 1176                | 118625           |
+-----------------------+------------------+---------------------+------------------+

+SuperJob Moscow--------+------------------+---------------------+------------------+
| Язык программирования | Вакансий найдено | Вакансий обработано | Средняя зарплата |
+-----------------------+------------------+---------------------+------------------+
| TypeScript            | 2                | 2                   | 224000           |
| Swift                 | 0                | 0                   | 0                |
| Scala                 | 1                | 1                   | 240000           |
| Objective-C           | 0                | 0                   | 0                |
| Shell                 | 0                | 0                   | 0                |
| Go                    | 1                | 1                   | 300000           |
| C++                   | 12               | 10                  | 169400           |
| C#                    | 7                | 4                   | 131500           |
| PHP                   | 10               | 9                   | 148444           |
| Ruby                  | 1                | 0                   | 0                |
| Python                | 14               | 10                  | 113507           |
| Java                  | 5                | 2                   | 224000           |
| JavaScript            | 20               | 14                  | 134505           |
+-----------------------+------------------+---------------------+------------------+
```

### Project Goals
The code is written for educational purposes.