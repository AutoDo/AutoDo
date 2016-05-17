class Square(object):

    def __init__(self, width, height):
        self._width = width
        self._height = height

    def get_width(self):
        return self._width

    def get_height(self):
        return self._height

    def get_area(self):
        return self._height * self._width
