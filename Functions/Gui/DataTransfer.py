class DataTransfer():

    def __init__(self):
        self.__value = 0

    def setValue(self, value):
        self.__value = value

    def getValue(self):
        return self.__value

    def whileValue(self):
        while True:
            self.getValue()
