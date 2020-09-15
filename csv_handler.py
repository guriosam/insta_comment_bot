import csv
import os


class CSVHandler:

    def __init__(self):
        pass

    def open_csv(self, path):
        csv_file = []
        with open(path, 'r') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                csv_file.append(row)
        return csv_file

    def write_csv(self, path, name, lines):
        if not os.path.exists(path):
            os.makedirs(path)
        f = open(path + name, 'w', newline='', encoding="utf-8")
        with f:
            writer = csv.writer(f)
            for row in lines:
                if row:
                    writer.writerow(row)
