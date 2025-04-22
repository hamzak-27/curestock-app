# CureStock Deployment Checklist

Use this checklist when deploying CureStock to Render.

## Before Deployment

- [ ] Run tests locally to ensure everything works
- [ ] Check that all database models have migrations
- [ ] Ensure `.gitattributes` file is properly set for line endings
- [ ] Make sure `render.yaml` is updated with the correct settings
- [ ] Verify `build.sh` has LF line endings (not CRLF)
- [ ] Set `DEBUG=False` for production

## Initial Deployment

- [ ] Create a new Render account if you don't have one
- [ ] Connect your GitHub repository to Render
- [ ] Deploy using the "Blueprint" option to use `render.yaml`
- [ ] Wait for all services to be created and deployed
- [ ] Check the logs for any errors during build or startup
- [ ] Manually set sensitive environment variables like `OPENAI_API_KEY`

## Database Setup

- [ ] Verify database was created properly
- [ ] Check logs to make sure migrations ran successfully
- [ ] If migrations failed, SSH into the instance and run `./run_migrations.sh`

## Post-Deployment Checks

- [ ] Visit the application URL to verify it's running
- [ ] Check that the database connection is working
- [ ] Test key functionality like adding/viewing calls
- [ ] Verify static files are being served correctly

## Troubleshooting Common Issues

- **Migrations not applied**: Run `python deploy_helpers.py migrate`
- **Shell scripts failing**: Check line endings and permissions
- **Database connection issues**: Verify `DATABASE_URL` environment variable
- **Static files not loading**: Check `STATIC_ROOT` and `STATIC_URL` settings

## Useful Commands

```bash
# View logs
render logs

# SSH into your instance
render ssh

# Run migrations manually
./run_migrations.sh

# Check migration status
python manage.py showmigrations

# Reset database tables (caution: destroys data)
python deploy_helpers.py reset_tables
``` 