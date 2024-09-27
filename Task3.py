import csv
import os
from datetime import datetime
import matplotlib.pyplot as plt


def calculate_age(birth_date_str):
    try:
        birth_date = datetime.strptime(birth_date_str, '%d.%m.%Y')
        today = datetime.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        return age
    except ValueError:
        return None


def read_csv_file(file_path):
    if not os.path.exists(file_path):
        print("Повідомлення про відсутність або проблеми при відкритті файлу CSV.")
        return None

    try:
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            data = list(reader)
        print("Ok")
        return data
    except Exception as e:
        print(f"Повідомлення про відсутність або проблеми при відкритті файлу CSV: {e}")
        return None


def count_by_gender(data):
    gender_counts = {'male': 0, 'female': 0}
    for row in data:
        gender = row.get('Стать')
        if gender in gender_counts:
            gender_counts[gender] += 1
    return gender_counts


def count_by_age_group(data):
    age_groups = {
        'younger_18': 0,
        '18-45': 0,
        '45-70': 0,
        'older_70': 0
    }
    for row in data:
        birth_date_str = row.get('Дата народження')
        age = calculate_age(birth_date_str)
        if age is None:
            continue
        if age < 18:
            age_groups['younger_18'] += 1
        elif 18 <= age <= 45:
            age_groups['18-45'] += 1
        elif 45 < age <= 70:
            age_groups['45-70'] += 1
        elif age > 70:
            age_groups['older_70'] += 1
    return age_groups


def count_by_gender_and_age_group(data):
    gender_age_counts = {
        'younger_18': {'male': 0, 'female': 0},
        '18-45': {'male': 0, 'female': 0},
        '45-70': {'male': 0, 'female': 0},
        'older_70': {'male': 0, 'female': 0}
    }
    for row in data:
        birth_date_str = row.get('Дата народження')
        age = calculate_age(birth_date_str)
        if age is None:
            continue
        gender = row.get('Стать')
        if gender not in ['male', 'female']:
            continue
        if age < 18:
            gender_age_counts['younger_18'][gender] += 1
        elif 18 <= age <= 45:
            gender_age_counts['18-45'][gender] += 1
        elif 45 < age <= 70:
            gender_age_counts['45-70'][gender] += 1
        elif age > 70:
            gender_age_counts['older_70'][gender] += 1
    return gender_age_counts


def plot_bar_chart(categories, values, title, xlabel, ylabel, file_name):
    plt.figure(figsize=(10, 6))
    bars = plt.bar(categories, values, color=['skyblue', 'salmon', 'lightgreen', 'violet', 'gold'])
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.tight_layout()
    plt.savefig(file_name)
    plt.show()


def plot_gender_age_chart(gender_age_counts, title, file_name):
    categories = list(gender_age_counts.keys())
    males = [gender_age_counts[cat]['male'] for cat in categories]
    females = [gender_age_counts[cat]['female'] for cat in categories]

    x = range(len(categories))
    width = 0.35

    plt.figure(figsize=(12, 7))
    plt.bar(x, males, width, label='Чоловіки', color='blue')
    plt.bar([i + width for i in x], females, width, label='Жінки', color='pink')

    plt.xlabel('Вікові категорії')
    plt.ylabel('Кількість співробітників')
    plt.title(title)
    plt.xticks([i + width / 2 for i in x], categories)
    plt.legend()
    plt.tight_layout()
    plt.savefig(file_name)
    plt.show()


def main():
    csv_file = 'generated_people.csv'

    data = read_csv_file(csv_file)
    if data is None:
        return

    gender_counts = count_by_gender(data)
    male_count = gender_counts.get('male', 0)
    female_count = gender_counts.get('female', 0)
    print(f"Кількість співробітників чоловічої статі: {male_count}")
    print(f"Кількість співробітників жіночої статі: {female_count}")

    plot_bar_chart(
        categories=['Чоловіки', 'Жінки'],
        values=[male_count, female_count],
        title='Розподіл співробітників за статтю',
        xlabel='Стать',
        ylabel='Кількість',
        file_name='gender_distribution.png'
    )

    age_groups = count_by_age_group(data)
    print("\nКількість співробітників за віковими категоріями:")
    for group, count in age_groups.items():
        print(f"{group}: {count}")

    age_group_labels = {
        'younger_18': 'Молодше 18',
        '18-45': '18-45',
        '45-70': '45-70',
        'older_70': 'Старше 70'
    }
    age_categories = [age_group_labels[group] for group in age_groups.keys()]
    age_values = list(age_groups.values())

    plot_bar_chart(
        categories=age_categories,
        values=age_values,
        title='Розподіл співробітників за віковими категоріями',
        xlabel='Вікові категорії',
        ylabel='Кількість',
        file_name='age_distribution.png'
    )

    gender_age_counts = count_by_gender_and_age_group(data)
    print("\nКількість співробітників за статтю та віковими категоріями:")
    for group, counts in gender_age_counts.items():
        print(f"{age_group_labels[group]}: Чоловіки - {counts['male']}, Жінки - {counts['female']}")

    plot_gender_age_chart(
        gender_age_counts=gender_age_counts,
        title='Розподіл співробітників за віковими категоріями та статтю',
        file_name='gender_age_distribution.png'
    )

    print("\nВсі операції виконані успішно.")


if __name__ == "__main__":
    main()
