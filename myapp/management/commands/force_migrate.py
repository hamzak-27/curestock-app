from django.core.management.base import BaseCommand
from django.db import connection
from django.core.management import call_command
import logging

class Command(BaseCommand):
    help = 'Force migrations and create required tables'

    def handle(self, *args, **options):
        self.stdout.write('Starting forced migrations...')
        
        # Check database connection
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                self.stdout.write(self.style.SUCCESS('Database connection successful'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Database connection failed: {e}'))
            return
            
        # Run migrate command
        try:
            call_command('migrate', interactive=False)
            self.stdout.write(self.style.SUCCESS('Migrations completed successfully'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Migration error: {e}'))
            
        # Create tables explicitly if needed
        try:
            with connection.cursor() as cursor:
                # Check if the problematic table exists
                cursor.execute("""
                SELECT EXISTS (
                   SELECT FROM information_schema.tables 
                   WHERE table_schema = 'public'
                   AND table_name = 'myapp_call'
                );
                """)
                table_exists = cursor.fetchone()[0]
                
                if not table_exists:
                    self.stdout.write('Table myapp_call does not exist, creating manually...')
                    # Create the table structure based on your model
                    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS myapp_call (
                        id SERIAL PRIMARY KEY,
                        created_at TIMESTAMP WITH TIME ZONE NOT NULL,
                        customer_name VARCHAR(255) NOT NULL,
                        phone_number VARCHAR(20) NOT NULL,
                        transcript TEXT,
                        recording_url VARCHAR(255)
                    );
                    """)
                    self.stdout.write(self.style.SUCCESS('Table myapp_call created manually'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error creating table manually: {e}'))
            
        self.stdout.write(self.style.SUCCESS('Forced migration process completed')) 