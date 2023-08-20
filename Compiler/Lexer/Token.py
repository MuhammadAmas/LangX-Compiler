class Token ():
    def __init__(self, value, line):
        self.type = "undefined"
        self.value = value
        self.line = line

    def displayToken(self):
        showToken = "\t(" + self.type + ", " + self.value + \
            ", " + str(self.line) + ")"
        return showToken