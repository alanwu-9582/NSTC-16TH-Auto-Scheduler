import tkinter as tk
import json
import os
from tkinter import ttk, filedialog
from Constants import *
from Scheduler import Scheduler
from ScheduleWriter import ScheduleWriter

with open(f'libs/keyword_zhtw2en.json', 'r', encoding='utf-8') as jfile:
    keyword_zhtw2en = json.load(jfile)

with open(f'libs/keyword_en2zhtw.json', 'r', encoding='utf-8') as jfile:
    keyword_en2zhtw = json.load(jfile)

class AutoSchedulerGUI:
    def __init__(self, master):
        self.master = master
        self.intitializeUI()

        self.members_file = 'members.json'
        self.schedule_file = 'schedule.json'
        self.intitializeData()

    def intitializeUI(self):
        self.master.geometry('575x495')
        self.master.title("NSTC-S2 Auto Scheduler")
        self.master.iconbitmap("assets/icon.ico")
        self.master.config(bg="#eeeeee", padx = 5, pady = 5)

        self.createFrames()
        self.createObject()
        self.createEditingZone()
        self.createFunctionButtons()

    def intitializeData(self):
        with open(f'data/{self.members_file}', 'r', encoding='utf-8') as f:
            self.members = json.load(f)

        self.members_data = self.members['students']
        self.students_name = [student['name'] for student in self.members_data]
        self.students.config(values=self.students_name)
        self.config_editing_btns(tk.DISABLED)
        self.current_student_index = -1

    def createFrames(self):
        self.top_frame = tk.Frame(self.master)
        self.top_frame.grid(row=0, column=0)
        self.top_frame.config(bg="#cccccc", padx=5, pady=5)

        #left top
        self.editing_frame = tk.Frame(self.top_frame) 
        self.editing_frame.grid(row=0, column=0)
        self.editing_frame.config(bg="#cccccc", padx=5, pady=5)

        #left top top
        self.editing_top_frame = tk.Frame(self.editing_frame) 
        self.editing_top_frame.grid(row=0, column=0)
        self.editing_top_frame.config(bg="#cccccc", padx=5, pady=5)

        #left top middle
        self.editing_middle_frame = tk.Frame(self.editing_frame) 
        self.editing_middle_frame.grid(row=2, column=0)
        self.editing_middle_frame.config(bg="#cccccc", padx=5, pady=2)

        #left top bottom
        self.editing_bottom_frame = tk.Frame(self.editing_frame) 
        self.editing_bottom_frame.grid(row=3, column=0)
        self.editing_bottom_frame.config(bg="#cccccc", padx=5, pady=2)
        
        self.right_top_frame = tk.Frame(self.top_frame)
        self.right_top_frame.grid(row=0, column=1)
        self.right_top_frame.config(bg="#cccccc", padx=5, pady=5)

        self.bottom_frame = tk.Frame(self.master)
        self.bottom_frame.grid(row=1, column=0)
        self.bottom_frame.config(bg="#eeeeee", padx=5, pady=5)

        self.bottom_top_input_frame = tk.Frame(self.bottom_frame)
        self.bottom_top_input_frame.grid(row=0, column=0)
        self.bottom_top_input_frame.config(bg="#eeeeee", padx=5, pady=5)

        self.bottom_middle_input_frame = tk.Frame(self.bottom_frame)
        self.bottom_middle_input_frame.grid(row=1, column=0)
        self.bottom_middle_input_frame.config(bg="#eeeeee", padx=5, pady=5)

        self.bottom_bottom_input_frame = tk.Frame(self.bottom_frame)
        self.bottom_bottom_input_frame.grid(row=2, column=0)
        self.bottom_bottom_input_frame.config(bg="#eeeeee", padx=5, pady=5)

    def createObject(self):
        self.log = tk.Text(self.right_top_frame, width=25,  height=16, font=("System", 10), relief="solid", state=tk.DISABLED)
        self.log.grid(pady=5, columnspan=40)
        self.log_count = 0

        self.students = ttk.Combobox(self.bottom_top_input_frame, width=35)
        self.students.grid(row=0, column=0, padx=1, pady=2)

        Label = tk.Label(self.bottom_middle_input_frame, bg="#eeeeee", font = "MicrosoftJhengHeiUI 12", text = "最大值勤次數")
        Label.config(width=13) 
        Label.grid(row=0, column=0)

        self.max_duties_count = tk.StringVar()
        Spinbox = tk.Spinbox(self.bottom_middle_input_frame, from_=1, to=20, textvariable=self.max_duties_count, wrap=True)
        Spinbox.config(width=15)
        Spinbox.grid(row=0, column=1)
        self.max_duties_count.set(4)

        Label = tk.Label(self.bottom_middle_input_frame, bg="#eeeeee", font = "MicrosoftJhengHeiUI 12", text = "最大早班次數")
        Label.config(width=13) 
        Label.grid(row=0, column=2)

        self.max_morning_duties_count = tk.StringVar()
        Spinbox = tk.Spinbox(self.bottom_middle_input_frame, from_=1, to=20, textvariable=self.max_morning_duties_count, wrap=True)
        Spinbox.config(width=15)
        Spinbox.grid(row=0, column=3)
        self.max_morning_duties_count.set(2)

        Label = tk.Label(self.bottom_middle_input_frame, bg="#eeeeee", font = "MicrosoftJhengHeiUI 12", text = "錯誤迭代次數")
        Label.config(width=13) 
        Label.grid(row=1, column=0)

        self.max_error_depth = tk.StringVar()
        Spinbox = tk.Spinbox(self.bottom_middle_input_frame, from_=0, to=10, textvariable=self.max_error_depth, wrap=True)
        Spinbox.config(width=15)
        Spinbox.grid(row=1, column=1)
        self.max_error_depth.set(10)

    def createEditingZone(self):
        self.editing_zone = tk.Text(self.editing_top_frame, width=30,  height=9, font=("Microsoft JhengHei UI", 12, "bold"), relief="solid")
        self.editing_zone.grid(pady=5, columnspan=40)

        self.clear_all_option_btn = ttk.Button(self.editing_middle_frame, text="刪除全部", width=20, command=self.clear_all_option)
        self.clear_all_option_btn.grid(row=0, column=0, padx=5, pady=1)

        self.clear_last_option_btn = ttk.Button(self.editing_middle_frame, text="刪除最後", width=20, command=self.clear_last_option)
        self.clear_last_option_btn.grid(row=0, column=1, padx=5, pady=1)

        self.day_editing = ttk.Combobox(self.editing_bottom_frame, width=13)
        self.day_editing.grid(row=0, column=0, padx=1, pady=1)
        self.day_editing.config(value=DAYS_EDiting)

        self.time_editing = ttk.Combobox(self.editing_bottom_frame, width=10)
        self.time_editing.grid(row=0, column=1, padx=1, pady=1)
        self.time_editing.config(value=TIMES_EDiting)

        self.add_time_btn = ttk.Button(self.editing_bottom_frame, text="添加時間", width=12, command=self.add_time)
        self.add_time_btn.grid(row=0, column=2, padx=4, pady=1)

        self.duty_editing = ttk.Combobox(self.editing_bottom_frame, width=13)
        self.duty_editing.grid(row=1, column=0, padx=1, pady=1)
        self.duty_editing.config(value=DUTIES_EDiting)

        self.add_duty_btn = ttk.Button(self.editing_bottom_frame, text="添加工作", width=12, command=self.add_duty)
        self.add_duty_btn.grid(row=1, column=2, padx=4, pady=1)

    def createFunctionButtons(self):
        self.select_student_btn = ttk.Button(self.bottom_top_input_frame, text="編輯隊員", width=15, command=self.select_student)
        self.select_student_btn.grid(row=0, column=1, padx=1, pady=2)

        self.save_editon_btn = ttk.Button(self.bottom_top_input_frame, text="儲存編輯", width=15, command=self.save_editon)
        self.save_editon_btn.grid(row=0, column=2, padx=1, pady=2)

        DEAFULT_BUTTON_WIDTH = 15

        self.start_scheduler_btn = ttk.Button(self.bottom_bottom_input_frame, text="開始排班", width=DEAFULT_BUTTON_WIDTH, command=self.start_scheduler)
        self.start_scheduler_btn.grid(row=0, column=0, padx=1, pady=2)

        self.tutorial_btn = ttk.Button(self.bottom_bottom_input_frame, text="使用教學", width=DEAFULT_BUTTON_WIDTH, command=self.tutorial)
        self.tutorial_btn.grid(row=0, column=1, padx=1, pady=2)

        self.attachFile_member_btn = ttk.Button(self.bottom_bottom_input_frame, text="匯入名單", width=DEAFULT_BUTTON_WIDTH, command=self.attachFile_member)
        self.attachFile_member_btn.grid(row=0, column=2, padx=1, pady=2)

        self.attachFile_schedule_btn = ttk.Button(self.bottom_bottom_input_frame, text="匯入班表模板", width=DEAFULT_BUTTON_WIDTH, command=self.attachFile_schedule)
        self.attachFile_schedule_btn.grid(row=0, column=3, padx=1, pady=2)

        self.export_schedule_btn = ttk.Button(self.bottom_bottom_input_frame, text="匯出班表", width=DEAFULT_BUTTON_WIDTH, command=self.export_schedule)
        self.export_schedule_btn.grid(row=1, column=3, padx=1, pady=2)

    def config_editing_btns(self, state):
        self.save_editon_btn.config(state=state)
        self.add_time_btn.config(state=state)
        self.add_duty_btn.config(state=state)

    def select_student(self):
        selected_student_index = self.students.current()
        if selected_student_index >= 0:
            self.editing_zone.delete("1.0", "end")

            for keywords in self.members_data[selected_student_index]['unable']:
                keywords_splited = keywords.split()
                translated_word = ''
                for keyword in keywords_splited:
                    translated_word += keyword_en2zhtw[keyword]
                    translated_word += " "
                
                self.editing_zone.insert("end", f"{translated_word}\n")

            self.config_editing_btns(tk.NORMAL)
            self.current_student_index = selected_student_index

        else:
            self.updateLog("請選擇一個人類 D:")

    def add_time(self):
        added_day_index = self.day_editing.current()
        added_time_index = self.time_editing.current()
        
        if added_day_index != -1 and added_day_index != -1:
            translated_word = f"{DAYS_EDiting[added_day_index]} {TIMES_EDiting[added_time_index]}"
            self.editing_zone.insert("end", f"{translated_word}\n")

        else:
            self.updateLog("請選擇完整時間")

    def add_duty(self):
        added_duty_index = self.duty_editing.current()
        
        if added_duty_index != -1:
            translated_word = DUTIES_EDiting[added_duty_index]
            self.editing_zone.insert("end", f"{translated_word}\n")

        else:
            self.updateLog("請選擇工作")

    def clear_last_option(self):
        editing_data = self.editing_zone.get('0.0', 'end').split('\n')
        last_option_index = 0
        for i, option in enumerate(editing_data):
            last_option_index = i if option not in [None, ' ', ''] else last_option_index

        self.editing_zone.delete(f"{last_option_index+1}.0", "end")
        if last_option_index != 0: self.editing_zone.insert("end", "\n")

    def clear_all_option(self):
        self.editing_zone.delete("1.0", "end")
        
    def save_editon(self):
        editing_data = self.editing_zone.get('0.0', 'end').split('\n')
        unable_setting = []
        for keywords in editing_data:
            if keywords != '':
                keywords_splited = keywords.split()
                translated_word = ''
                for keyword in keywords_splited:
                    if keyword in keyword_zhtw2en:
                        
                        translated_word += keyword_zhtw2en[keyword]
                        translated_word += " "

                    else:
                        break

                if translated_word != '':
                    unable_setting.append(translated_word)
        
        if self.current_student_index != -1:
            self.members_data[self.current_student_index]['unable'] = unable_setting
            self.updateLog(f'已經記住了 {self.members_data[self.current_student_index]["name"]} 的設定~')

        with open(f'data/{self.members_file}', 'w', encoding='utf-8') as jfile:
            json.dump(self.members, jfile, ensure_ascii=False, indent=4)

    def start_scheduler(self):
        self.start_scheduler_btn.config(state=tk.DISABLED)
        scheduler = Scheduler(self.schedule_file, self.members_file)
        max_duties_count = int(self.max_duties_count.get())
        max_morning_duties_count = int(self.max_morning_duties_count.get())
        feedback = scheduler.run_scheduler(max_duties_count, max_morning_duties_count)
        
        max_error_depth = int(self.max_error_depth.get())
        depth_count = 0
        while feedback and depth_count < max_error_depth:
            scheduler = Scheduler(self.schedule_file, self.members_file)
            feedback = scheduler.run_scheduler(max_duties_count, max_morning_duties_count)
            self.master.update()
            depth_count += 1
        
        if feedback:
            self.updateLog(feedback)

        else:
            self.updateLog("好欸! 完成排班 ouo")

        self.start_scheduler_btn.config(state=tk.NORMAL)

    def tutorial(self):
        os.startfile(r'assets\NSTC-S2 Docs.pdf')

    def attachFile_member(self):
        file_path = filedialog.askopenfilename(title="Import Members", filetypes= [("Json Files","*.json")])

        if file_path:
            with open(file_path, 'r', encoding="utf8") as jfile:
                member_file = json.load(jfile)

            if "format" in member_file:
                if member_file["format"] == "Scheduler_member":
                    with open(f'data/{self.members_file}', 'w', encoding='utf-8') as jfile:
                        json.dump(member_file, jfile, ensure_ascii=False, indent=4)
                    
                    self.intitializeData()
                    self.updateLog("成功匯入名單!")
                    return

            self.updateLog("這是啥呢>< 好像不是對的格式")

    def attachFile_schedule(self):
        file_path = filedialog.askopenfilename(title="Import Schedule Template", filetypes= [("Json Files","*.json")])

        if file_path:
            with open(file_path, 'r', encoding="utf8") as jfile:
                member_file = json.load(jfile)

            if "format" in member_file:
                if member_file["format"] == "Scheduler_schedule":
                    with open(f'data/{self.schedule_file}', 'w', encoding='utf-8') as jfile:
                        json.dump(member_file, jfile, ensure_ascii=False, indent=4)

                    self.updateLog("成功匯入班表模板!")
                    return

            self.updateLog("這是啥呢>< 好像不是對的格式")

    def export_schedule(self):
        schedule_writer = ScheduleWriter(f'NEW_{self.schedule_file}')
        feedback = schedule_writer.write_to_csv()
        self.updateLog(feedback if feedback else "班表已用表格格式匯出~")
        os.startfile(r'NEW_schedule.csv')

    def updateLog(self, arg: str):
        self.log.config(state=tk.NORMAL)
        if self.log_count >= MAX_LOG_COUNT:
            self.log.delete("1.0", "end")
            self.log_count = 0

        self.log.insert("end", f"{arg}\n")
        self.log_count += 1
        self.log.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    gui = AutoSchedulerGUI(root)
    root.mainloop()