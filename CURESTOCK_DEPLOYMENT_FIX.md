# CureStock Deployment Fix Guide

Follow these steps to fix the database connection issue for your CureStock app on Render.

## The Issue

Your application is showing: `Error: no such table: myapp_call` because the database migrations haven't been applied to your PostgreSQL database on Render.

## Step-by-Step Fix

### 1. Update Environment Variables

1. Log in to your [Render Dashboard](https://dashboard.render.com/)
2. Select your `curestock-app` web service
3. Go to the **Environment** tab
4. Add/Update the following environment variables:
   - `DATABASE_URL`: `postgresql://curestock_1_user:30ojM7FOojsrncsOMGJcmkaZ9icLuN2Y@dpg-d03trh6uk2gs73cldm1g-a.oregon-postgres.render.com/curestock_1`
   - `RENDER`: `true`
   - `RUN_MIGRATIONS_ON_STARTUP`: `true`
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

If the above steps don't work, try these alternatives:

### SSH Into Your Service and Run Django Migrate Directly

```bash
# Connect to your service shell
python manage.py showmigrations  # Check migration status
python manage.py migrate         # Apply migrations
```

### Update Your Render Config (render.yaml)

If you're using GitHub deployment, update your `render.yaml` file to use the correct database URL:

```yaml
services:
  - type: web
    name: curestock-app
    # ...other settings...
    envVars:
      - key: DATABASE_URL
        value: postgresql://curestock_1_user:30ojM7FOojsrncsOMGJcmkaZ9icLuN2Y@dpg-d03trh6uk2gs73cldm1g-a.oregon-postgres.render.com/curestock_1
      # ...other env vars...
```

Then redeploy your application.

## Troubleshooting

If you're still having issues:

1. Check Render logs for error messages
2. Verify your database exists and is accessible
3. Try both internal and external database URLs
4. Make sure your PostgreSQL plan on Render is active 