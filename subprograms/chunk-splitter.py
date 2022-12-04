import csv
def csv_splitter(file_name, save_path):
    f = open(file_name, mode="r", encoding="utf-8-sig")
    reader = csv.reader(f)
    data = list(reader)
    print(data[0])
    field_names = data[0]
    years = set()
    curr_year = data[1][-1][0:4]
    years.add(curr_year)
    lastindex = 1
    for i, row in enumerate(data):
        if len(row) != len(field_names):
            continue
        if i == 0:
            continue
        year = row[-1][0:4]
        if (year not in years):
            newfile = open(save_path + curr_year + ".csv", "w", encoding="utf-8-sig", newline='')
            writer = csv.writer(newfile)
            writer.writerow(field_names)
            writer.writerows(data[lastindex:i])
            lastindex = i
            years.add(year)
            curr_year = year
    newfile = open(save_path + curr_year + ".csv", "w", encoding="utf-8-sig", newline='')
    writer = csv.writer(newfile)
    writer.writerow(field_names)
    writer.writerows(data[lastindex:len(data)])

csv_splitter("vacancies_by_year.csv", "./chunks/")