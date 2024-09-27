import csv
import random
from faker import Faker
from datetime import datetime

fake = Faker(locale='uk_UA')

male_patronymics = [
    'Олександрович', 'Вікторович', 'Іванович', 'Петрович', 'Андрійович',
    'Миколайович', 'Сергійович', 'Володимирович', 'Григорович', 'Дмитрович',
    'Юрійович', 'Олегович', 'Васильович', 'Степанович', 'Михайлович',
    'Федорович', 'Ілліч', 'Євгенович', 'Анатолійович', 'Богданович'
]

female_patronymics = [
    'Олександрівна', 'Вікторівна', 'Іванівна', 'Петрівна', 'Андріївна',
    'Миколаївна', 'Сергіївна', 'Володимирівна', 'Григорівна', 'Дмитрівна',
    'Юріївна', 'Олегівна', 'Василівна', 'Степанівна', 'Михайлівна',
    'Федорівна', 'Іллівна', 'Євгенівна', 'Анатоліївна', 'Богданівна'
]

patronymics = {
    "male": male_patronymics,
    "female": female_patronymics
}


def generate_birth_date():
    year = random.randint(1938, 2008)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    return datetime(year, month, day).strftime('%d.%m.%Y')


def generate_record(gender):
    if gender == 'male':
        first_name = fake.first_name_male()
        patronymic = random.choice(patronymics["male"])
    else:
        first_name = fake.first_name_female()
        patronymic = random.choice(patronymics["female"])

    last_name = fake.last_name()
    birth_date = generate_birth_date()
    job = fake.job()
    city = fake.city()
    address = fake.address()
    phone_number = fake.phone_number()
    email = fake.email()

    return [last_name, first_name, patronymic, gender, birth_date, job, city, address, phone_number, email]

def main():
    records = []
    num_records = 2000
    num_female = int(num_records * 0.4)
    num_male = num_records - num_female

    for _ in range(num_male):
        records.append(generate_record('male'))

    for _ in range(num_female):
        records.append(generate_record('female'))

    random.shuffle(records)

    csv_file = 'generated_people.csv'
    header = ['Прізвище', 'Ім’я', 'По батькові', 'Стать', 'Дата народження', 'Посада', 'Місто проживання',
              'Адреса проживання', 'Телефон', 'Email']

    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(records)

    print(f"Файл '{csv_file}' успішно створений з {num_records} записами.")

if __name__ == '__main__':
    main()