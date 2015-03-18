# taken from http://blog.jameskyle.org/2010/10/nose-unit-testing-quick-start/

class A(object):
    def __init__(self):
        self.value = "Some Value"
    def return_true(self):
        return True
    def raise_exc(self, val):
        raise KeyError(val)
