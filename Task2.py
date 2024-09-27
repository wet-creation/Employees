import csv
import os
from datetime import datetime
from openpyxl import Workbook


def calculate_age(birth_date):
    birth_date = datetime.strptime(birth_date, '%d.%m.%Y')
    today = datetime.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age


def read_csv_file(file_path):
    if not os.path.exists(file_path):
        print("Повідомлення про відсутність або проблеми при відкритті файлу CSV.")
        return None

    try:
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            header = next(reader)
            data = [row for row in reader]
        return header, data
    except Exception as e:
        print(f"Помилка при читанні файлу CSV: {e}")
        return None


def create_xlsx_file(header, data, file_path):
    try:
        wb = Workbook()

        ws_all = wb.active
        ws_all.title = "all"
        ws_all.append(header + ["Вік"])

        for row in data:
            age = calculate_age(row[4])
            ws_all.append(row + [age])

        sheets_info = [
            ("younger_18", lambda age: age < 18),
            ("18-45", lambda age: 18 <= age <= 45),
            ("45-70", lambda age: 45 < age <= 70),
            ("older_70", lambda age: age > 70)
        ]

        for sheet_name, condition in sheets_info:
            ws = wb.create_sheet(title=sheet_name)
            ws.append(["№", "Прізвище", "Ім’я", "По батькові", "Дата народження", "Вік"])
            index = 1
            for row in data:
                age = calculate_age(row[4])
                if condition(age):
                    ws.append([index] + row[:3] + [row[4], age])
                    index += 1

        wb.save(file_path)
        print("Ok")
    except Exception as e:
        print(f"Повідомлення про неможливість створення XLSX файлу: {e}")


def main():
    csv_file = 'generated_people.csv'
    xlsx_file = 'employee_data.xlsx'

    csv_data = read_csv_file(csv_file)
    if csv_data is None:
        return

    header, data = csv_data

    create_xlsx_file(header, data, xlsx_file)


if __name__ == "__main__":
    main()
