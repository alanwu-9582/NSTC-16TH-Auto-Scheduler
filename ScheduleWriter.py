import json
import csv
from Constants import *
from ErrorHandler import ErrorHandler

class ScheduleWriter:
    def __init__(self, schedule_file):
        with open(f'data/{schedule_file}', 'r', encoding='utf-8') as jfile:
            self.schedule_data = json.load(jfile)

        with open('libs/keyword_en2zhtw.json', 'r', encoding='utf-8') as jfile:
            self.keyword_en2zhtw = json.load(jfile)

        self.schedule = self.schedule_data['classes']
        self.schedule_file = schedule_file

    def write_commander(self, csv_writer):
        row = ['']
        row.append(self.keyword_en2zhtw['commander'])
        for day in DAYS:
            row.append(self.schedule['morning'][day]['commander'])

        csv_writer.writerow(row)

    def write_morning(self, csv_writer):
        for morning_duty in list(self.schedule['morning']['Monday'].keys()):
            if morning_duty == 'commander': continue
            row = ['早上']
            row.append(self.keyword_en2zhtw[morning_duty])
            for day in DAYS:
                row.append('\n'.join(self.schedule['morning'][day][morning_duty]))

            csv_writer.writerow(row)

    def write_evening(self, csv_writer):
        for evening_duty in list(self.schedule['evening']['Monday'].keys()):
            row = ['晚上']
            row.append(self.keyword_en2zhtw[evening_duty])
            for day in DAYS:
                if evening_duty in self.schedule['evening'][day]:
                    row.append('\n'.join(self.schedule['evening'][day][evening_duty]))

                else:
                    row.append('')

            csv_writer.writerow(row)

    def write_to_csv(self):
        try:
            with open(f'{self.schedule_file.split(".")[0]}.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(['', '', '星期一', '星期二', '星期三', '星期四', '星期五'])

                if self.schedule_data['grade'] == 'eleven': self.write_commander(csv_writer)
                self.write_morning(csv_writer)
                csv_writer.writerow(['' for i in range(7)])
                self.write_evening(csv_writer)

            return 0
        except PermissionError:
            return ErrorHandler.handle("PermissionError")
