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
   - **Build Command**: `pip install -r requirements.txt && python manage.py collectstatic --noinput`
   - **Start Command**: `gunicorn myproject.wsgi:application`

6. Add the following environment variables:
   - `SECRET_KEY`: Generate a secure random key
   - `OPENAI_API_KEY`: Your OpenAI API key
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

The application uses SQLite in both development and production environments. The database file is stored in the project root as `db.sqlite3`. Django migrations will handle the schema creation automatically when you run migrations.