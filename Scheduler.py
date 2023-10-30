from collections import Counter
import json
import random
from Constants import *
from ErrorHandler import ErrorHandler

class Scheduler:
    def __init__(self, schedule_file, members_file):
        self.schedule_file = schedule_file
        self.members_file = members_file

        with open(f'data/{self.schedule_file}', 'r', encoding='utf-8') as jfile:
            self.schedule = json.load(jfile)

        with open(f'data/{self.members_file}', 'r', encoding='utf-8') as jfile:
            self.members = json.load(jfile)

        self.students = self.members["students"]
        self.students_name = [student["name"] for student in self.students]

        # 初始化成員的值班次數
        for student in self.students:
            student["morning_duties_count"] = 0
            student["evening_duties_count"] = 0
            student["morning_duties"] = []
            student["evening_duties"] = []

        self.new_schedule = self.schedule
        self.new_classes = self.new_schedule["classes"]

    def assign_commanders_duties(self):
        try:
            commanders = [commander["name"] for commander in self.members["commanders"]]
            for day in DAYS:
                available_commanders = self.filter_worktime_available_commanders(commanders, day)
                selected_commander = available_commanders[random.randint(0, len(available_commanders)-1)]
                
                evening_duties = self.filter_commander_available_duties(selected_commander, list(self.new_classes['evening'][day].keys()))
                morning_duties = self.filter_commander_available_duties(selected_commander, list(self.new_classes['morning'][day].keys()))

                evening_duty = evening_duties[random.randint(0, len(evening_duties)-1)]
                morning_duty = morning_duties[random.randint(0, len(morning_duties)-1)]

                self.new_classes['morning'][day]['commander'] = selected_commander
                self.new_classes['morning'][day][morning_duty][0] = selected_commander
                self.new_classes['evening'][day][evening_duty][0] = selected_commander

                selected_commander_index = self.students_name.index(selected_commander)
                self.students[selected_commander_index]['morning_duties_count'] += 1
                self.students[selected_commander_index]['evening_duties_count'] += 1
                self.students[selected_commander_index][f"morning_duties"].append(f'{day} {TIMES[0]} {evening_duty}')
                self.students[selected_commander_index][f"evening_duties"].append(f'{day} {TIMES[1]} {morning_duty}')

                commanders.remove(selected_commander)
            return 0

        except ValueError:
            return ErrorHandler.handle("Commanders_ValueError")
        
        except KeyError:
            return ErrorHandler.handle("Commanders_KeyError")


    def filter_worktime_available_commanders(self, commanders, day):
        available_commanders = []
        for commander in commanders:
            if self.is_commander_worktime_available(commander, day):
                available_commanders.append(commander)

        return available_commanders

    def is_commander_worktime_available(self, commander, day):
        student = self.students[self.students_name.index(commander)]
        unable = student["unable"]

        for keyword in unable:
            keywords = keyword.split()
            if len(keywords) >= 2:
                if keywords[0] in ["Everyday", day]:
                    return False

        return True
    
    def filter_commander_available_duties(self, commander, duties):
        available_duties = []
        for duty in duties:
            if self.is_duty_available(commander, duty) and duty != 'commander':
                available_duties.append(duty)

        return available_duties

    def filter_worktime_available_students(self, duties, day, time):
        default_human = self.create_default_human(duties)
        available_students = [name for name in self.students_name if self.is_worktime_available(name, default_human, day, time)]
        return available_students

    def is_worktime_available(self, name, default_human, day, time):
        student = self.students[self.students_name.index(name)]
        unable = student["unable"]

        for keyword in unable:
            keywords = keyword.split()
            if len(keywords) >= 2:
                if keywords == ["Everyday", "full"]:
                    return False
            
                if keywords[0] == day or keywords[0] == "Everyday" and keywords[1] == time or keywords[1] == "full":
                    return False
                
        total_duties_count = student["morning_duties_count"] + student["evening_duties_count"]
        morning_duties_count = student["morning_duties_count"]
        
        if name not in default_human:
            if time == 'morning':
                return morning_duties_count < self.max_morning_duties_count
            
            if time == 'evening':
                return total_duties_count < self.max_duties_count
        else:
            return False

    def filter_duty_available_students(self, students, duty_dict):
        for duty in duty_dict:
            if isinstance(duty, str):
                pecise_duty = duty  
            
        available_students = [student for student in students if self.is_duty_available(student, pecise_duty)]
        return available_students

    def is_duty_available(self, name, duty):
        student = self.students[self.students_name.index(name)]
        unable = student["unable"]

        for keyword in unable:
            keywords = keyword.split()
            if keywords[0] == duty:
                return False
                
        return True
    
    def create_default_human(self, duties):
        default_human = []

        for duty in duties:
            default_human += duties[duty]

        default_human = list(filter(lambda name: name != "", default_human))
        return default_human

    def reorganize_duties(self):
        for time in TIMES:
            for day in DAYS:
                duties = self.new_classes[time][day]
                self.worktime_available_students = self.filter_worktime_available_students(duties, day, time)
                random.shuffle(self.worktime_available_students)

                for duty in duties:
                    for i in range(len(self.new_classes[time][day][duty])):
                        selected_student, self.worktime_available_students = self.assign_student_to_duty(
                            time,
                            self.new_classes[time][day][duty][i], 
                            [duty, i], 
                            self.worktime_available_students
                        )

                        if selected_student == -1:
                            return ErrorHandler.handle(self.worktime_available_students)
                        
                        elif selected_student:
                            self.new_classes[time][day][duty][i] = selected_student
                            student_index = self.students_name.index(selected_student)
                            self.students[student_index][f"{time}_duties_count"] += 1
                            self.students[student_index][f"{time}_duties"].append(f'{day} {time} {duty}')
        return 0

    def assign_student_to_duty(self, time, current_member, pecise_duty_dict, worktime_available_students):
        try:
            if current_member == "":
                duty_available_students = self.filter_duty_available_students(worktime_available_students, pecise_duty_dict)
                students_data = [self.students[self.students_name.index(duty_available_student)] for duty_available_student in duty_available_students]

                weights_formula = lambda x: pow(1/10, x)
                students_choices_weights  = [weights_formula(student_data[f'{time}_duties_count']) for student_data in students_data]
                selected_students = random.choices(duty_available_students, weights=students_choices_weights, k=100)
                counter = Counter(selected_students)
                most_common = counter.most_common(1)
                selected_student = most_common[0][0]                
                worktime_available_students.remove(selected_student)

                return selected_student, worktime_available_students
            
            return None, worktime_available_students
        
        except IndexError:
            return -1, "IndexError"

    def run_scheduler(self, max_duties_count: int, max_morning_duties_count: int):
        self.max_duties_count = max_duties_count
        self.max_morning_duties_count = max_morning_duties_count
        
        assign_commanders_duties_feedback = self.assign_commanders_duties() if self.schedule['grade'] == 'eleven' else None
        reorganize_duties_feedback = self.reorganize_duties()
        
        if reorganize_duties_feedback:
            return reorganize_duties_feedback
        
        if assign_commanders_duties_feedback:
            return assign_commanders_duties_feedback

        with open(f'data/NEW_{self.schedule_file}', 'w', encoding='utf-8') as jfile:
            json.dump(self.schedule, jfile, ensure_ascii=False, indent=4)

        with open(f'data/NEW_{self.members_file}', 'w', encoding='utf-8') as jfile:
            json.dump(self.members, jfile, ensure_ascii=False, indent=4)

        return 0