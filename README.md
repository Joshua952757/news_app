## Installation & setup

## Description

This is a news application built using Django framework. It allows user to register with different types, which allocates multiple features. Such as admin, editors, journalists and readers. The news app presents articles and newsletters written by journalists and approved by editors, they can be found through the publishers. Readers are given access to view and subscribe to not only publishers but individual journalists as well.

### Inital setup
1. Clone the repo 
- using HTTPS
```bash
git clone https://github.com/Joshua952757/news_app.git
```

- using SSH
```bash
git clone git@github.com:Joshua952757/news_app.git
```

2. Change directory
```bash
cd news_app
```

### Configure the envionmental variables:
1. Rename `.env.template` to `.env`.
2. Populate the `.env` with values.

### Setup with virtual environments
1. Create virtual environment
```bash
python3 -m venv venv
```

2. Activate the virtual environment
```bash
.\venv\Scripts\activate
```

3. Install the dependencies
```bash
pip install -r requirements.txt
```

4. Apply migrations to the databse
```bash
python manage.py migrate
```

5. Run the server
```bash
python manage.py runserver
``` 

### Setup with Docker

1. Build your and run you containers
```bash
docker compose up -d --build
```

2. Apply migration to the container's database 
```bash
docker compose run django-web python manage.py migrate
```

### Usage
1. Navigate to `127.0.0.1:8000` to view the home page.