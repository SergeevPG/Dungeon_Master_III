from ctypes import string_at


class cars(object):
    def __init__(self, name, price):
        self.name2 = name
        self.price2 = price

    def printt(self):
        print(self.name2, self.price2)


rang = cars("range Rover", 10000)
rang2 = cars("range Rover2", 101232100)
rang3 = cars("range Rover3", 1012400)
rang4 = cars("range Rover4", 1041200)

rang3.printt()
str="dfda"
print(str.capitalize())