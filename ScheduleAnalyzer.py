import json
import csv
from Constants import *
from ErrorHandler import ErrorHandler

class ScheduleAnalyzer:
    def __init__(self, member_file):
        with open(f'data/{member_file}', 'r', encoding='utf-8') as jfile:
            self.members_data = json.load(jfile)

        with open('libs/keyword_en2zhtw.json', 'r', encoding='utf-8') as jfile:
            self.keyword_en2zhtw = json.load(jfile)

        self.members = self.members_data['students']

    def translate_sentence(self, sentence):
        letters = sentence.split()
        tran_letters = []
        for letter in letters:
            tran_letters.append(self.keyword_en2zhtw[letter] if letter in self.keyword_en2zhtw else letter)
        
        return ' '.join(tran_letters)


    def analyze(self):
        with open('Analyze_report.txt', 'w', encoding='utf-8') as file:
            for i, member_data in enumerate(self.members):
                file.write(f'{member_data["name"]}\n')

                file.write(f'\t無法值勤:\n')
                for unable in member_data['unable']:
                    file.write(f'\t\t{self.translate_sentence(unable)}\n')

                file.write(f'\n')
                file.write(f'\t總值勤次數: {member_data["morning_duties_count"] + member_data["evening_duties_count"]}\n')

                file.write(f'\t早上值勤次數: {member_data["morning_duties_count"]}\n')
                for morning_duty in member_data['morning_duties']:
                    file.write(f'\t\t{self.translate_sentence(morning_duty)}\n')

                file.write(f'\t晚上值勤次數: {member_data["evening_duties_count"]}\n')
                for evening_duty in member_data['evening_duties']:
                    file.write(f'\t\t{self.translate_sentence(evening_duty)}\n')

                file.write(f'\n')
        


