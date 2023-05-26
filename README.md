# Programming vacancies compare

This project allows you to get information on all vacancies from superjob.ru and hh.ru:
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

## Project Goals
The code is written for educational purposes.