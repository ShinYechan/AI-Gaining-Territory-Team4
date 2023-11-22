import random
from itertools import combinations
from shapely.geometry import LineString, Point

class MACHINE():
    """
        [ MACHINE ]
        MinMax Algorithm을 통해 수를 선택하는 객체.
        - 모든 Machine Turn마다 변수들이 업데이트 됨

        ** To Do **
        MinMax Algorithm을 이용하여 최적의 수를 찾는 알고리즘 생성
           - class 내에 함수를 추가할 수 있음
           - 최종 결과는 find_best_selection을 통해 Line 형태로 도출
               * Line: [(x1, y1), (x2, y2)] -> MACHINE class에서는 x값이 작은 점이 항상 왼쪽에 위치할 필요는 없음 (System이 organize 함)
    """
    def __init__(self, score=[0, 0], drawn_lines=[], whole_lines=[], whole_points=[], location=[]):
        self.id = "MACHINE"
        self.score = [0, 0] # USER, MACHINE
        self.drawn_lines = [] # Drawn Lines
        self.board_size = 7 # 7 x 7 Matrix
        self.num_dots = 0
        self.whole_points = []
        self.location = []
        self.triangles = [] # [(a, b), (c, d), (e, f)]

    def find_best_selection(self):
        available = [[point1, point2] for (point1, point2) in list(combinations(self.whole_points, 2)) if self.check_availability([point1, point2])]
        return random.choice(available)

    #5.외부와 연결되지 않은 두 선분 찾는 함수
    def find_unconnected_lines(self):
        for line1 in self.drawn_lines:
            for line2 in self.drawn_lines:
                if line1 != line2 and not self.is_line_connected(line1, line2): #and not self.has_point_inside(line1, line2):
                    return line1, line2
        return None

    def is_line_connected(self, line1, line2):
        x1, y1 = line1[0]
        x2, y2 = line1[1]
        x3, y3 = line2[0]
        x4, y4 = line2[1]

        # Check if the lines share an endpoint
        if (x1, y1) == (x3, y3) or (x1, y1) == (x4, y4) or (x2, y2) == (x3, y3) or (x2, y2) == (x4, y4):
            return True

        # Check if the lines overlap
        line1 = LineString([line1[0], line1[1]])
        line2 = LineString([line2[0], line2[1]])
        return line1.intersects(line2)
    
    def has_point_inside(self, line1, line2):
        # Extract coordinates of the four points
        x1, y1 = line1[0]
        x2, y2 = line1[1]
        x3, y3 = line2[0]
        x4, y4 = line2[1]

        polygon = Polygon([(x1, y1), (x2, y2), (x3, y3), (x4, y4)])

        # Check if any whole_points, excluding the points of line1 and line2, are inside the polygon
        points_to_check = set(self.whole_points) - set([line1[0], line1[1], line2[0], line2[1]])
        inside_polygon = any(polygon.contains(Point(point)) for point in points_to_check)

        # If any whole_points are inside, return True; otherwise, return False
        return not inside_polygon


    #6.외부와 연결되지 않은 두 선분으로 만들 수 있는 선분의 개수 구하는 함수
    def count_possible_lines(self, line1, line2):
        count = 0
        for point1 in line1:
            for point2 in line2:
                if point1 != point2 and self.check_availability([point1, point2]):
                    count += 1
        return count

    def is_diagonal_blocked(self, line1, line2):
        x1, y1 = line1[0]
        x2, y2 = line1[1]
        x3, y3 = line2[0]
        x4, y4 = line2[1]

        # Check if the lines are diagonals and if they block each other
        if (x1 - x2) * (y3 - y4) == (y1 - y2) * (x3 - x4):
            # Check if the lines cross each other
            line1 = LineString([line1[0], line1[1]])
            line2 = LineString([line2[0], line2[1]])
            return line1.crosses(line2)
        else:
            return False
    
    
    def check_availability(self, line):
        line_string = LineString(line)

        # Must be one of the whole points
        condition1 = (line[0] in self.whole_points) and (line[1] in self.whole_points)
        
        # Must not skip a dot
        condition2 = True
        for point in self.whole_points:
            if point==line[0] or point==line[1]:
                continue
            else:
                if bool(line_string.intersection(Point(point))):
                    condition2 = False

        # Must not cross another line
        condition3 = True
        for l in self.drawn_lines:
            if len(list(set([line[0], line[1], l[0], l[1]]))) == 3:
                continue
            elif bool(line_string.intersection(LineString(l))):
                condition3 = False

        # Must be a new line
        condition4 = (line not in self.drawn_lines)

        if condition1 and condition2 and condition3 and condition4:
            return True
        else:
            return False    

    
