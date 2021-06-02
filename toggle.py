class Toggle:
    def __init__(self):
        self.val = 0
        self.lag = 0
        self.state = False
    
    def toggle(self):
        self.lag += 1
        self.lag %= 100

    def eval(self):
        if(self.lag != self.val):
            self.state = not self.state

        self.lag = self.val
        return self.state
        

    