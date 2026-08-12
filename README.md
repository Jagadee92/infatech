# Company Peers Django Application

A simple fresher-level Django application that searches for a company and
displays companies from the same industry in a peer comparison grid.

## How the page works

1. Type a keyword such as `tata` in the search box.
2. Matching company names appear in a dropdown below the box.
3. Click a company name (or press Search) to open it.
4. The page shows the company details card (price, market cap, P/E, book
   value, dividend yield, ROCE, ROE, face value) and the `Peers` grid with
   every company from the same industry.

The dropdown calls `/search-suggestions/`, a small Django view that returns
matching company names as JSON.

## Run with SQLite

SQLite is the default database, so MySQL is not needed for local testing.

1. Install Python 3.11 or newer from https://www.python.org/downloads/
2. Open PowerShell in this folder.
3. Create and activate a virtual environment:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

4. Install the packages and prepare the database:

   ```powershell
   python -m pip install -r requirements.txt
   python manage.py migrate
   ```

5. Start the application:

   ```powershell
   python manage.py runserver
   ```

6. Open http://127.0.0.1:8000/ and search for `tata`, `NCC`, or `Infosys`.

The migrations automatically add sample companies from several industries
(civil construction, iron & steel, IT, power, telecom, packaged foods,
investment companies and automobiles).

## Run the tests

```powershell
python manage.py test
```

## Sample / test data

Yes — sample company data is added in the migrations:

- `companies/migrations/0001_initial.py` — first set of construction companies
- `companies/migrations/0002_company_details_and_more_companies.py` — more
  companies and extra detail fields

When you run `python manage.py migrate`, Django creates the tables and also
inserts this sample data. That is why the Peers grid works without Excel yet.
Later you can replace it with Excel → MySQL import.

## Switch to MySQL

1. Install MySQL and create a database:

   ```sql
   CREATE DATABASE finance_db CHARACTER SET utf8mb4;
   ```

2. Open `finance_project/settings.py` and update these lines near the top:

   ```python
   USE_SQLITE = False
   MYSQL_DATABASE = "finance_db"
   MYSQL_USER = "root"
   MYSQL_PASSWORD = "your_password"
   MYSQL_HOST = "127.0.0.1"
   MYSQL_PORT = "3306"
   ```

3. Run migrations so Django creates tables in MySQL and loads sample data:

   ```powershell
   python manage.py migrate
   python manage.py runserver
   ```

Keep `USE_SQLITE = True` until MySQL is ready. The website code stays the same.
