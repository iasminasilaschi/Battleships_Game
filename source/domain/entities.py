from dataclasses import dataclass


@dataclass
class Ship:
    __symbol: str
    __length: int
    __coordinate_x: int
    __coordinate_y: int
    __orientation: str

    @property
    def symbol(self):
        return self.__symbol

    @property
    def length(self):
        return self.__length

    @property
    def coordinate_x(self):
        return self.__coordinate_x

    @property
    def coordinate_y(self):
        return self.__coordinate_y

    @symbol.setter
    def symbol(self, new_symbol):
        self.__symbol = new_symbol

    @coordinate_x.setter
    def coordinate_x(self, new_coordinate_x):
        self.__coordinate_x = new_coordinate_x

    @coordinate_y.setter
    def coordinate_y(self, new_coordinate_y):
        self.__coordinate_y = new_coordinate_y

    @property
    def orientation(self):
        return self.__orientation


@dataclass
class Move:
    __coordinate_x: int
    __coordinate_y: int
    __symbol: str

    @property
    def symbol(self):
        return self.__symbol

    @property
    def coordinate_x(self):
        return self.__coordinate_x

    @property
    def coordinate_y(self):
        return self.__coordinate_y

    @coordinate_x.setter
    def coordinate_x(self, new_coordinate_x):
        self.__coordinate_x = new_coordinate_x

    @coordinate_y.setter
    def coordinate_y(self, new_coordinate_y):
        self.__coordinate_y = new_coordinate_y

    def __str__(self) -> str:
        return "Move: ({}, {})".format(self.__coordinate_x, self.__coordinate_y)
