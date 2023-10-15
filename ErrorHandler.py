
ERROR_LIBRARY = {
    "ValueError": "數值錯誤! 沒有可以排班的人類\n請重試..\n或者條整最大值勤次數",
    "PermissionError": "錯誤! 無法輸出班表\n請關掉開啟的班表再試一次"
} 

class ErrorHandler:
    def handle(self, error):
        if error in ERROR_LIBRARY:
            return ERROR_LIBRARY[error]
        
        else:
            return error