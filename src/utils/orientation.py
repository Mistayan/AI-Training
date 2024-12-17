import enum


class Orientation(enum.Enum):
    EAST: int = 0
    NORTH: int = 1
    WEST: int = 2
    SOUTH: int = 3

    @staticmethod
    def from_angle(angle):
        if 315 <= angle or angle < 45:
            return Orientation.NORTH
        elif 45 <= angle < 135:
            return Orientation.EAST
        elif 135 <= angle < 225:
            return Orientation.SOUTH
        else:  # 225 <= angle < 315
            return Orientation.WEST
