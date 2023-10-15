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
        self.commanders = self.members["commanders"]

        # 初始化成員的值班次數
        for student in self.students:
            student["morning_duties_count"] = 0
            student["evening_duties_count"] = 0

        self.new_schedule = self.schedule
        self.new_classes = self.new_schedule["classes"]

    def assign_commanders_duties(self):
        random.shuffle(self.commanders)

        for i, commander in enumerate(self.commanders[:5]):
            morning_duty = random.choice(MORNING_DUTIES)
            evening_duty = random.choice([EVENING_FULL_DUTIES, EVENING_HALF_DUTIES][DAYS[i] in ["Wednesday", "Friday"]])
            duties = [morning_duty, evening_duty]

            self.new_classes[TIMES[0]][DAYS[i]]["commander"] = commander["name"]

            for j, time in enumerate(TIMES):
                if duties[j] in GUANGFU_DUTIES:
                    self.new_classes[time][DAYS[i]]["guangfu"][duties[j]] = commander["name"]

                elif duties[j] == "zhonghe":
                    self.new_classes[time][DAYS[i]][duties[j]][0] = commander["name"]

                else:
                    self.new_classes[time][DAYS[i]][duties[j]] = commander["name"]

                student_index = self.students_name.index(commander["name"])
                self.students[student_index][f"{time}_duties_count"] += 1

    def filter_worktime_available_students(self, duties, day, time):
        default_human = self.create_default_human(duties)
        available_students = [name for name in self.students_name if self.is_worktime_available(name, default_human, day, time)]
        return available_students

    def is_worktime_available(self, name, default_human, day, time):
        student = self.students[self.students_name.index(name)]
        unable = student["unable"]

        for keyword in unable:
            keywords = keyword.split()
            if keywords[0] == "Time" and len(keywords) >= 3:
                if keywords[1] == day and keywords[2] == time:
                    return False
                
                elif keywords[1] == "Everyday" and keywords[2] == time:
                    return False
                
                elif keywords[1] == day and keywords[2] == "full":
                    return False

        total_duties_count = student["morning_duties_count"] + student["evening_duties_count"]
        morning_duties_count = student["morning_duties_count"]
        return (total_duties_count < self.max_duties_count and morning_duties_count < self.max_morning_duties_count) and not(name in default_human)

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
            if keywords[0] == "Work" and len(keywords) >= 2:
                if keywords[1] == duty:
                    return False
                
        return True
    
    def create_default_human(self, duties):
        default_human = []

        for duty in duties:
            if duty == "guangfu":
                default_human += list(duties["guangfu"].values())

            elif duty == "zhonghe":
                default_human += duties[duty]
                
            else:
                default_human.append(duties[duty])

        default_human = list(filter(lambda name: name != "", default_human))
        return default_human

    def reorganize_duties(self):
        for time in TIMES:
            for day in DAYS:
                duties = self.new_classes[time][day]
                self.worktime_available_students = self.filter_worktime_available_students(duties, day, time)
                random.shuffle(self.worktime_available_students)

                for duty in duties:
                    if duty == "guangfu":
                        for guangfu_duty in duties[duty]:
                            selected_student, self.worktime_available_students = self.assign_student_to_duty(
                                self.new_classes[time][day][duty][guangfu_duty], 
                                ['guangfu', guangfu_duty], 
                                self.worktime_available_students
                            )

                            if selected_student == -1:
                                return ErrorHandler.handle(ErrorHandler, self.worktime_available_students)

                            elif selected_student:
                                self.new_classes[time][day][duty][guangfu_duty] = selected_student
                                student_index = self.students_name.index(selected_student)
                                self.students[student_index][f"{time}_duties_count"] += 1

                    elif duty == "zhonghe":
                        for i in range(len(self.new_classes[time][day]["zhonghe"])):
                            selected_student, self.worktime_available_students = self.assign_student_to_duty(
                                self.new_classes[time][day][duty][i], 
                                ['zhonghe', i], 
                                self.worktime_available_students
                            )

                            if selected_student == -1:
                                return ErrorHandler.handle(ErrorHandler, self.worktime_available_students)
                            
                            elif selected_student:
                                self.new_classes[time][day][duty][i] = selected_student
                                student_index = self.students_name.index(selected_student)
                                self.students[student_index][f"{time}_duties_count"] += 1

                    else:
                        selected_student, self.worktime_available_students = self.assign_student_to_duty(
                            self.new_classes[time][day][duty], 
                            [duty], 
                            self.worktime_available_students
                        )

                        if selected_student == -1:
                            return ErrorHandler.handle(ErrorHandler, self.worktime_available_students)

                        elif selected_student:
                            self.new_classes[time][day][duty] = selected_student
                            student_index = self.students_name.index(selected_student)
                            self.students[student_index][f"{time}_duties_count"] += 1

        return 0

    def assign_student_to_duty(self, current_member, pecise_duty_dict, worktime_available_students):
        try:
            if current_member == "":
                duty_available_students = self.filter_duty_available_students(worktime_available_students, pecise_duty_dict)
                selected_student = duty_available_students[random.randint(0, len(duty_available_students) - 1)]
                worktime_available_students.remove(selected_student)
                return selected_student, worktime_available_students
            
            return None, worktime_available_students
        
        except ValueError:
            return -1, "ValueError"

    def run_scheduler(self, max_duties_count: int, max_morning_duties_count: int):
        self.max_duties_count = max_duties_count
        self.max_morning_duties_count = max_morning_duties_count
        self.assign_commanders_duties()
        feedback = self.reorganize_duties()

        with open(f'data/NEW_{self.schedule_file}', 'w', encoding='utf-8') as jfile:
            json.dump(self.schedule, jfile, ensure_ascii=False, indent=4)

        with open(f'data/NEW_{self.members_file}', 'w', encoding='utf-8') as jfile:
            json.dump(self.members, jfile, ensure_ascii=False, indent=4)

        return feedback