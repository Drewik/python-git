import csv
def csv_splitter(file_name, save_path):
    f = open(file_name, mode="r", encoding="utf-8-sig")
    reader = csv.reader(f)
    data = list(reader)
    print(data[0])
    field_names = data[0]
    years = set()

    years.add(data[1][-1][0:4])
    lastindex = 1
    for i, row in enumerate(data):
        if len(row) != len(field_names):
            continue
        if i == 0:
            continue
        year = row[-1][0:4]

        if (year not in years):
            current_year = str(int(year) - 1)
            newfile = open(save_path + current_year + ".csv", "w", encoding="utf-8-sig", newline='')
            writer = csv.writer(newfile)
            writer.writerow(field_names)
            writer.writerows(data[lastindex:i])
            lastindex = i+1
            years.add(year)
        if row == data[-1]:
            newfile = open(save_path + str(int(year)) + ".csv", "w", encoding="utf-8-sig", newline='')
            writer = csv.writer(newfile)
            writer.writerow(field_names)
            writer.writerow(data[lastindex:i])

csv_splitter("vacancies_by_year.csv", "./chunks/")