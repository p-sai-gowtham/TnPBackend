from django.core.management.base import BaseCommand
from user.models import User
from django.contrib.auth.hashers import make_password
import os
import pandas as pd


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "directory", type=str, help="Directory containing mock test XLSX files"
        )

    def handle(self, *args, **options):
        directory = options["directory"]

        if not os.path.exists(directory):
            self.stdout.write(
                self.style.ERROR(f"The directory {directory} does not exist")
            )
            return

        students_created = 0
        students_updated = 0

        for filename in os.listdir(directory):
            if filename.endswith(".xlsx"):
                file_path = os.path.join(directory, filename)
                self.stdout.write(self.style.NOTICE(f"Processing file: {file_path}"))

                try:
                    data = pd.read_excel(file_path)
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f"Error reading file {filename}: {e}")
                    )
                    continue

                if data.empty:
                    self.stdout.write(
                        self.style.WARNING(f"The file {filename} is empty")
                    )
                    continue

                required_columns = [
                    "Name",
                    "Email",
                    "ID No.",
                    # "Batch Year",
                    # "Branch",
                ]
                missing_columns = [
                    col for col in required_columns if col not in data.columns
                ]

                if missing_columns:
                    self.stdout.write(
                        self.style.ERROR(
                            f'Missing required columns in file {filename}: {", ".join(missing_columns)}'
                        )
                    )
                    continue

                for index, row in data.iterrows():
                    self.stdout.write(
                        self.style.WARNING(
                            f"Student with ID {row['ID No.']} "
                        )
                    )
                    student= User.objects.get(
                        reg_no=row["ID No."].upper(),
                    )
                    students_updated += 1
                    # Ensure student.tests is not None
                    if student.tests is None:
                        student.tests = {}

                    if "Accenture Full Length Mock Test" not in student.tests:
                        student.tests["Accenture Full Length Mock Test"] = []

                    required_test_columns = [
                        "Status",
                        "Time Spent",
                        "Ques Count",
                        "Attempted Ques",
                        "Total",
                        "Max Marks",
                        "Percentage",
                        "Qualified",
                        "Accuracy",
                        "Tab Switches",
                        "Cognitive Ability Total",
                        "Cognitive Ability Percentage",
                        "Technical Ability Total",
                        "Technical Ability Percentage",
                        "Coding Total",
                        "Coding Percentage",
                    ]

                    dictionary = {row["Assessment Name"]: {}}
                    for col in required_test_columns:
                        # Check if the column exists in the DataFrame
                        if col in row:
                            if row[col] == " " or pd.isna(row[col]) or row[col] == "-":
                                row[col]=0
                            else:
                                dictionary[row["Assessment Name"]][col.lower()] = row[col]
                        else:
                            # Handle missing columns by setting a default value
                            dictionary[row["Assessment Name"]][col.lower()] = None
                    if dictionary not in student.tests["Accenture Full Length Mock Test"]:
                        student.tests["Accenture Full Length Mock Test"].append(dictionary)
                    student.save()

        if students_created > 0:
            self.stdout.write(
                self.style.SUCCESS(f"{students_created} students added successfully")
            )

        if students_updated > 0:
            self.stdout.write(
                self.style.SUCCESS(f"{students_updated} students updated successfully")
            )

        if students_created == 0 and students_updated == 0:
            self.stdout.write(self.style.WARNING("No students were added or updated"))