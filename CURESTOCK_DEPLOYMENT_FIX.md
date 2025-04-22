# CureStock Deployment Fix Guide

Follow these steps to fix the database connection issue for your CureStock app on Render.

## The Issue

Your application is showing: `Error: no such table: myapp_call` because:
1. **No environment variables were defined** on your Render service
2. The database connection couldn't be established
3. Migrations weren't applied to your PostgreSQL database

## Step-by-Step Fix

### 1. Add Essential Environment Variables

1. Log in to your [Render Dashboard](https://dashboard.render.com/)
2. Select your `curestock-app` web service
3. Go to the **Environment** tab
4. You need to **add all** of the following environment variables:
   - `DATABASE_URL`: `postgresql://curestock_1_user:30ojM7FOojsrncsOMGJcmkaZ9icLuN2Y@dpg-d03trh6uk2gs73cldm1g-a.oregon-postgres.render.com/curestock_1`
   - `RENDER`: `true`
   - `RUN_MIGRATIONS_ON_STARTUP`: `true`
   - `SECRET_KEY`: (generate a random string or use Render's secret generator)
   - `DEBUG`: `False` 
5. Click **Save Changes**

### 2. Run Manual Migration Script (via Render Shell)

1. Go to your `curestock-app` web service in the Render dashboard
2. Select the **Shell** tab
3. Run the fix script:
   ```
   python fix_curestock_db.py
   ```
4. This script will:
   - Verify your database connection
   - Run migrations automatically
   - Check if tables were created properly

### 3. Restart Your Service

1. Go back to the main page of your web service
2. Click **Manual Deploy** 
3. Select **Clear build cache & deploy**
4. Wait for the service to rebuild and restart

### 4. Verify the Fix

1. After deployment completes, visit your app URL
2. The error should be gone, and your app should work properly
3. If you still see the error, check the logs in the Render dashboard

## Alternative Fix Options

If adding environment variables doesn't work, you have these alternatives:

### Direct Command Line Fix

In the Render shell:

```bash
# Set environment variables manually
export DATABASE_URL="postgresql://curestock_1_user:30ojM7FOojsrncsOMGJcmkaZ9icLuN2Y@dpg-d03trh6uk2gs73cldm1g-a.oregon-postgres.render.com/curestock_1"
export RENDER="true"

# Run migrations
python manage.py migrate
```

### Update Your render.yaml File

If you're using GitHub deployment, update your `render.yaml` file:

```yaml
services:
  - type: web
    name: curestock-app
    env: python
    region: oregon
    buildCommand: chmod +x build.sh && ./build.sh
    startCommand: gunicorn myproject.wsgi:application
    runtime: python3.11
    envVars:
      - key: SECRET_KEY
        generateValue: true
      - key: OPENAI_API_KEY
        sync: false
      - key: DATABASE_URL
        value: postgresql://curestock_1_user:30ojM7FOojsrncsOMGJcmkaZ9icLuN2Y@dpg-d03trh6uk2gs73cldm1g-a.oregon-postgres.render.com/curestock_1
      - key: DEBUG
        value: "False"
      - key: RENDER
        value: "true"
      - key: RUN_MIGRATIONS_ON_STARTUP
        value: "true"
    autoDeploy: true
```

Then push this change to your repository.

## Troubleshooting Common Issues

1. **No environment variables defined**: This is the primary issue you were facing
2. **Connection refused errors**: Make sure the database exists and is accessible
3. **Migration errors**: Check if there are any issues with your migration files
4. **Permissions issues**: Ensure your database user has proper permissions 