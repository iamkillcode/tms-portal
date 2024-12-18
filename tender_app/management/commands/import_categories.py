import pandas as pd
from django.core.management.base import BaseCommand
from tender_app.models import Category

class Command(BaseCommand):
    help = 'Import category data from Excel into the database'

    def handle(self, *args, **kwargs):
        file_path = './tender_app/src/static/categorylist.xlsx'  # Path to the Excel file

        try:
            # Load data from Excel
            df = pd.read_excel(file_path)

            # Iterate over rows and save them in the database
            for _, row in df.iterrows():
                Category.objects.update_or_create(
                    code=row['Category Code'],
                    defaults={'name': row['Category Name']}
                )

            self.stdout.write(self.style.SUCCESS('Successfully imported categories.'))

        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error: {str(e)}"))
