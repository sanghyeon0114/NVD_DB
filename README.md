# CVE-parsing

### Setting
python3 -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt

### If you want to use the program, please enter the command below.
source .venv/bin/activate

### When running the program, status or errors are made to info.log.
vim info.log

### Setting 1. Load the latest cve, cpe and cpe_match files from the nvd homepage.
- linux command

./load_file.sh

- window command

.\window_command\load_file.bat

### Setting 2. load(or reload) database.
first, please install postgresql

second, please create .env

---------------example_start-----------------

DB_HOST=localhost

DB_PORT=5432

DB_USER=root

DB_NAME=postgres

DB_PASSWORD=1234

----------------example_end------------------

third, enter the command below

- linux command

./reload_database.sh

- window command

.\window_command\reload_database.bat

### + Setting 2. If you only want to create(or delete) a database, please enter the command below. ( If you have done Setting 2, you can skip it. )
- linux command

./create_database.sh

./delete_tables.sh

- window command

.\window_command\create_database.bat

.\window_command\delete_tables.bat

### Setting 3. insert data into database ( background execution )
- linux command

./insert.sh

- window command

.\window_command\create_database.bat

.\window_command\delete_tables.bat

### get CVE & CPE & CPE_MATCH count command ( you can see state of inserting data )
- linux command

./get_count.sh

- window command

.\window_command\get_count.bat

### find data by keyword
- linux command

./find.sh

- window command

.\window_command\find.bat

### How to use find command
When the program starts, a string appears as shown below.

"input keyword : "

Please enter a keyword

You can enter multiple keywords like below. If you want to stop typing keywords, just hit enter without typing anything.

--------------------program start--------------------

input keyword : medical

input keyword : medicine

input keyword : hospital

input keyword : 

---------------------program end---------------------