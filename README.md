# CureStock App

A Django application for inventory management of medicines and related services.

## Deployment on Render

### Prerequisites
- Render account
- Git repository with your application code

### Deployment Steps

1. Fork or clone this repository to your GitHub account
2. In the Render dashboard, select "New Web Service"
3. Connect your GitHub repository
4. Select the "Python" environment
5. Configure the following:
   - **Name**: Choose a name for your service (e.g., curestock-app)
   - **Region**: Choose a region close to your users
   - **Branch**: main (or your preferred branch)
   - **Build Command**: `chmod +x build.sh && ./build.sh`
   - **Start Command**: `gunicorn app:app`
   - **Runtime**: Python 3.11

6. Add the following environment variables:
   - `SECRET_KEY`: Generate a secure random key
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `DATABASE_URL`: Your PostgreSQL connection string (e.g., postgresql://username:password@host/database)
   - `DEBUG`: False
   - `RENDER`: true
   - `MIGRATION_SECRET`: A secret key for the migration endpoint

7. Click "Create Web Service"

### Database Migrations

After deployment, run migrations by visiting:
```
https://your-app-name.onrender.com/migrate?secret=your_migration_secret
```
Replace `your_migration_secret` with the value you set in your environment variables.

## Local Development

1. Clone the repository
2. Create and activate a virtual environment
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up environment variables in `.env` file
5. Run migrations:
   ```bash
   python manage.py migrate
   ```
6. Start the development server:
   ```bash
   python manage.py runserver
   ```

## Database Setup

The application uses SQLite for local development and PostgreSQL in production on Render. The PostgreSQL database connection is automatically configured when deployed to Render using the DATABASE_URL environment variable.

You don't need to manually create database tables - Django migrations will handle the schema creation automatically when you run migrations.

### Local PostgreSQL Setup (Optional)

If you want to use PostgreSQL locally as well:

1. Install PostgreSQL on your machine
2. Create a database
3. Set the DATABASE_URL environment variable in your local `.env` file:
   ```
   DATABASE_URL=postgresql://username:password@localhost/database
   ```
4. Run migrations:
   ```bash
   python manage.py migrate
   ```