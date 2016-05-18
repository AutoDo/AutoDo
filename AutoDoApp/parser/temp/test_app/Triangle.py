class Triangle(object):

    def __init__(self, angle1, angle2, angle3):
        self._angle1 = angle1
        self._angle2 = angle2
        self._angle3 = angle3

    def check_angle(self):
        return self._angle1 + self._angle2 + self._angle3 == 180
