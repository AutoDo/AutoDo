from AutoDoApp.parser.temp.test_app.Circle import Circle
from AutoDoApp.parser.temp.test_app.Square import Square
from AutoDoApp.parser.temp.test_app.Triangle import Triangle


class Math(object):

    def __init__(self):
        self.answer = 0
        self.problems = 5

    def get_mean(self):
        self.answer = 5

    def calculate_square(self, x, y):
        sq = Square(width=x, height=y)
        sq.get_area()
        sq.get_height()
        sq.get_width()

    def calculate_triangle(self, angle1, angle2, angle3):
        tr = Triangle(angle1=angle1, angle2=angle2, angle3=angle3)
        tr.check_angle()

    def calculate_circle(self, radius):
        cir = Circle(radius=radius)
        cir.get_area()
        cir.get_circumference()
