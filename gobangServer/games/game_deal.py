# coding=utf-8

import numpy as np
import random
from functools import cmp_to_key


class gameDeal:
    def __init__(self, x_width=15, y_height=15):
        self.x_width = x_width
        self.y_height = y_height

        # self.chessboard = np.random.randint(0, 3, size=(self.x_width, self.y_height))
        self.chessboard = np.zeros((self.x_width, self.y_height), dtype=int)
        self.zeroBoard = np.zeros((self.x_width, self.y_height))
        # self._p()

    def _p(self):
        print(self.chessboard)

    def get_notPlayPoint(self):
        tmpPoints = np.where(self.chessboard == 0)
        points = list(zip(tmpPoints[0], tmpPoints[1]))
        return points

    def play_chess(self, play_point, play_type):
        _x, _y = play_point
        print('[play_chess] 玩家[%s]下点[%s,%s]' % (play_type, _x, _y))
        if self.chessboard[_x, _y] != 0:
            print('[play_chess] 无效')
            return
        self.chessboard[_x, _y] = play_type
        self.zeroBoard[_x, _y] = 1
        isWin = False
        if self.horizontal_Match(_x, _y, play_type):
            isWin = True
        elif self.vertical_Match(_x, _y, play_type):
            isWin = True
        elif self.slant_top(_x, _y, play_type):
            isWin = True
        elif self.slant_bottom(_x, _y, play_type):
            isWin = True
        self._p()
        if isWin:
            print('[play_chess] 玩家[%s]胜利' % (play_type))
        return isWin

    def horizontal_Match(self, play_x, play_y, play_type):
        '''横行判断(即y轴不变,与x轴平行)'''
        maxCount = 1  # 所下的点在横行方向(正反)连续个数
        points = []  # 符合条件的坐标集
        for _x in range(1, 6):  # 反方向(-)(左边)
            curXpoint = play_x - _x
            curYpoint = play_y
            if curXpoint < 0:  # 超出边界
                break
            if self.chessboard[curXpoint, curYpoint] != play_type:
                break
            maxCount += 1
            points.append((curXpoint, curYpoint))

        points.append((play_x, play_y))

        for x_ in range(1, 6):  # 正方向(+)(右边)
            curXpoint = play_x + x_
            curYpoint = play_y
            if curXpoint >= self.x_width:  # 超出边界
                break
            if self.chessboard[curXpoint, curYpoint] != play_type:
                break
            maxCount += 1
            points.append((curXpoint, curYpoint))

        print('[horizontal_Match] maxCount', maxCount)
        print('[horizontal_Match] points', self.sort_point(points))
        return maxCount >= 5

    def vertical_Match(self, play_x, play_y, play_type):
        '''竖行判断(即x轴不变,与y轴平行)'''
        maxCount = 1  # 所下的点在竖直方向(正反)连续个数
        points = []  # 符合条件的坐标集
        for _y in range(1, 6):  # 反方向(-)(上边)
            curXpoint = play_x
            curYpoint = play_y - _y
            if curYpoint < 0:  # 超出边界
                break
            if self.chessboard[curXpoint, curYpoint] != play_type:
                break
            maxCount += 1
            points.append((curXpoint, curYpoint))

        points.append((play_x, play_y))

        for y_ in range(1, 6):  # 正方向(+)(下边)
            curXpoint = play_x
            curYpoint = play_y + y_
            if curYpoint >= self.y_height:  # 超出边界
                break
            if self.chessboard[curXpoint, curYpoint] != play_type:
                break
            points.append((curXpoint, curYpoint))
            maxCount += 1

        print('[vertical_Match] maxCount', maxCount)
        print('[vertical_Match] points', self.sort_point(points))
        return maxCount >= 5

    def slant_top(self, play_x, play_y, play_type):
        '''上斜判断/,XY轴同加减(即x轴+,y轴+和x轴-,y轴-)'''
        maxCount = 1  # 所下的点在上斜方向(正反)连续个数
        points = []  # 符合条件的坐标集
        for _x, _y in zip(range(1, 6), range(1, 6)):  # 反方向(-)(左下)
            curXpoint = play_x - _x
            curYpoint = play_y - _y
            if curXpoint < 0 or curYpoint < 0:  # 超出边界
                break
            if self.chessboard[curXpoint, curYpoint] != play_type:
                break
            maxCount += 1
            points.append((curXpoint, curYpoint))

        points.append((play_x, play_y))

        for _x, _y in zip(range(1, 6), range(1, 6)):  # 正方向(+)(右下)
            curXpoint = play_x + _x
            curYpoint = play_y + _y
            if curXpoint >= self.x_width or curYpoint >= self.y_height:  # 超出边界
                break
            if self.chessboard[curXpoint, curYpoint] != play_type:
                break
            maxCount += 1
            points.append((curXpoint, curYpoint))

        print('[slant_top] maxCount', maxCount)
        print('[slant_top] points', self.sort_point(points))
        return maxCount >= 5

    def slant_bottom(self, play_x, play_y, play_type):
        '''下斜判断/,XY轴反加减(即x轴-,y轴+和x轴+,y轴-)'''
        maxCount = 1  # 所下的点在下斜方向(正反)连续个数
        points = []  # 符合条件的坐标集
        for _x, _y in zip(range(1, 6), range(1, 6)):  # 反方向(-)(左上)
            curXpoint = play_x - _x
            curYpoint = play_y + _y
            if curXpoint < 0 or curYpoint >= self.y_height:  # 超出边界
                break
            if self.chessboard[curXpoint, curYpoint] != play_type:
                break
            maxCount += 1
            points.append((curXpoint, curYpoint))

        points.append((play_x, play_y))

        for _x, _y in zip(range(1, 6), range(1, 6)):  # 正方向(+)(右上)
            curXpoint = play_x + _x
            curYpoint = play_y - _y
            if curXpoint >= self.x_width or curYpoint < 0:  # 超出边界
                break
            if self.chessboard[curXpoint, curYpoint] != play_type:
                break
            maxCount += 1
            points.append((curXpoint, curYpoint))

        print('[slant_bottom] maxCount', maxCount)
        print('[slant_bottom] points', self.sort_point(points))
        return maxCount >= 5

    def sort_point(self, points, first='X', reverse=False):
        '''
        坐标索引排序
        :param points: 坐标集,如 [(1,2),(2,3),(4,4)]
        :param first:优先排序X,还是Y,(1,2)与(2,1) 哪个牌前面
        :param reverse:是否反向排序,从大到小
        :return:
        '''

        def sort_point(nextPoint, curPoint):
            if nextPoint == curPoint:
                return 0
            if first in ['y', 'Y']:
                if nextPoint[1] == curPoint[1]:
                    return 1 if nextPoint[0] > curPoint[0] else -1
                else:
                    return 1 if nextPoint[1] > curPoint[1] else -1
            else:
                if nextPoint[0] == curPoint[0]:
                    return 1 if nextPoint[1] > curPoint[1] else -1
                else:
                    return 1 if nextPoint[0] > curPoint[0] else -1

        return sorted(points, key=cmp_to_key(sort_point), reverse=reverse)


if __name__ == '__main__':
    chess = ChessObj()
    curPlayType = 1
    for x in range(9 * 9):
        print('*' * 70)
        points = chess.get_notPlayPoint()
        if chess.play_chess(random.choice(points), curPlayType):
            break
        if curPlayType == 1:
            curPlayType = 2
        elif curPlayType == 2:
            curPlayType = 1
        else:
            assert False
