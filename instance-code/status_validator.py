class status_validate:
    def __init__(self):
        self.counter = 0
        self.state = {
        "connected":self.__connected(),
        "disconnected":self.__disconnected(),
        "ok":self.__ok(),
        "error":self.__error()
        }

    def is_valid(self, recieved_list):
        return self.state.get(recieved_list["status"], False)

    def __connected(self):
        self.counter += 1
        return True if self.counter == 1 else False

    def __disconnected(self):
        if self.counter > 0:
            self.counter -= 1
            return True if self.counter == 0 else False
        else:
            return False

    def __ok(self):
        return True

    def __error(self):
        return True

    def __is_on(self):
        self.counter += 1
        return True if self.counter == 1 else False

    def __is_off(self):
        if self.counter > 0:
            self.counter -= 1
            return True if self.counter == 0 else False
        else:
            return False