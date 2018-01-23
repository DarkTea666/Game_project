class Observer:
    def __init__(self, subject1 = None, subject2 = None):
        if subject1:
            subject1.push_handlers(self)
        if subject2:
            subject2.push_handlers(self)