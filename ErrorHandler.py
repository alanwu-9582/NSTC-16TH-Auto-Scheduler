ERROR_LIBRARY = {
    "IndexError": "沒有可以排班的人類了\n請重試..\n或條整最大值勤次數",
    "Commanders_ValueError": "沒有可以排班的總指揮了\n請重試..\n或增加總指揮的人數",
    "Commanders_KeyError": "請提供總指揮的名單..",
    "PermissionError": "無法輸出班表\n請關掉開啟的班表再試一次"
} 

class ErrorHandler:
    def handle(error):
        if error in ERROR_LIBRARY:
            return ERROR_LIBRARY[error]
        
        else:
            return error