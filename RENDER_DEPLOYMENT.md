# Deploying CureStock on Render

This guide covers how to deploy the CureStock application on Render with a proper PostgreSQL database setup.

## Automatic Deployment

The project is configured for automatic deployment on Render using the `render.yaml` blueprint file. When you push changes to your repository, Render will automatically:

1. Create/update a web service for the application
2. Create/connect a PostgreSQL database
3. Run the build script which installs dependencies, collects static files, and runs migrations
4. Start the application with the correct WSGI configuration

## Manual Steps

### Setting up the Render project

1. Sign in to your Render account
2. Click "New" > "Blueprint"
3. Connect to your GitHub repository
4. Select the repository containing this project
5. Render will detect the `render.yaml` file and show you the resources it will create
6. Click "Apply" to create the services

### Database Setup

The database should be automatically created and connected to your application through the `render.yaml` blueprint.

- The `DATABASE_URL` environment variable will be automatically set
- Database migrations should run automatically during the build process

## Deploying from Windows

If you're developing on Windows and deploying to Render:

1. Make sure your line endings are set to LF (not CRLF) for `.sh` scripts:
   ```
   git config --global core.autocrlf input
   ```

2. Check shell scripts have LF line endings before committing:
   ```
   git add --renormalize .
   ```

3. Windows doesn't recognize the shebang (`#!/usr/bin/env bash`), but Render will use it correctly.

4. If you need to test shell scripts locally on Windows, consider using Git Bash or WSL.

## Troubleshooting

### Missing Database Tables

If you encounter errors like `relation "myapp_call" does not exist`, it means the migrations didn't run correctly. You can:

1. **SSH into your Render instance**:
   - Go to your web service in the Render dashboard
   - Navigate to the "Shell" tab
   - Run the migration script:
   ```
   ./run_migrations.sh
   ```

2. **Or use the helper script**:
   ```
   python deploy_helpers.py migrate
   ```

### Reset Migrations

If migrations are in a bad state, you can reset them:

```
python deploy_helpers.py reset_tables
```

This will reset all tables for the `myapp` app (warning: it will delete all data).

## Environment Variables

The following environment variables are used:

- `DATABASE_URL`: Connection string for the PostgreSQL database (set automatically)
- `SECRET_KEY`: Django secret key (generated automatically)
- `DEBUG`: Set to "False" for production
- `RENDER`: Set to "true" to identify the Render environment
- `OPENAI_API_KEY`: Your OpenAI API key (set manually in dashboard)

## Manual Database Management

You can connect to your Render PostgreSQL database from your local machine:

1. Find your database connection info in the Render dashboard under the database service
2. Use a tool like pgAdmin or DBeaver to connect
3. Manually inspect and modify database tables as needed

## Logs

Check logs in the Render dashboard under the "Logs" tab to diagnose any issues with the application or database. 