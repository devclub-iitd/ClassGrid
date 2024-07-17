# ClassGrid
ClassGrid is a web application for students of IIT Delhi to create their timetables for the semester as per the courses they have taken. The application is built using ReactJS and Django Rest Framework. The application is hosted and can be accessed [here](https://classgrid.devclub.in/).

## Setup
In this section, we will guide you through the setup of the project on your local machine.

### Prerequisites
- Python `3.12.1` or higher
- Node.js `v18.19.1` or higher
- npm `v9.2.0` or higher
- PostgreSQL `15` or higher

### Procedure

1. Create a fork of the `main` branch of this repository to your GitHub account and clone it to your local machine.

2. Navigate to the project directory
```bash
cd ClassGrid
```

3. Create a virtual environment and activate it
```bash
python3 -m venv env
source env/bin/activate
```

4. Install the dependencies for the client
```bash
cd client
npm install
```

5. Install the dependencies for the server
```bash
cd ../server
pip install -r requirements.txt
```

6. Create a PostgreSQL database and user
```bash
sudo -u postgres psql
```
```sql
CREATE DATABASE db_name;
CREATE USER
    db_user
WITH PASSWORD
    'db_password';
ALTER ROLE
    db_user
SET client_encoding TO 'utf8';
ALTER ROLE
    db_user
SET default_transaction_isolation TO 'read committed';
ALTER ROLE
    db_user
SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE
    db_name
TO
    db_user;
```

7. Create a `.env` file in the [`server`](server) directory and add the following environment variables
```bash
SECRET_KEY=your_secret_key
DB_NAME=db_name
DB_USER=db_user
DB_PASSWORD=db_password
DB_HOST=db_host
DB_PORT=db_port
```

8. Run the migrations
```bash
python manage.py migrate
```

9. Start the server
```bash
python manage.py runserver
```

10. Start the client
```bash
cd ../client
npm start
```

## Contributing
We welcome contributions to the project. To contribute, please follow the steps below:

1. Create a fork of the `main` branch of this repository to your GitHub account.

2. Clone the forked repository to your local machine.

3. Create a new branch for your feature or bug fix.
```bash
git checkout -b feature/your-feature
```

4. Make your changes and commit them.
```bash
git add .
git commit -m "Your commit message"
```

5. Push the changes to your forked repository.
```bash
git push origin feature/your-feature
```

6. Create a pull request to the `main` branch of this repository.

7. Wait for the maintainers to review your pull request.

## Copyright
&copy; 2024 Copyright : ClassGrid by DevClub IIT Delhi. All rights reserved.