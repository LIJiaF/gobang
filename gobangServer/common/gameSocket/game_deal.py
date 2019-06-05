# coding=utf-8

import numpy as np
from functools import cmp_to_key
import copy


class baseGameDeal(object):
    def __init__(self, game, *args, **kwargs):
        self.game = game


class gameDeal(baseGameDeal):
    def __init__(self, game, x_width=15, y_height=15, *args, **kwargs):
        super(gameDeal, self).__init__(game, *args, **kwargs)
        self.x_width = x_width
        self.y_height = y_height
        self.addMaxIndex = 6

        # self.chessBoard = np.random.randint(0, 3, size=(self.x_width, self.y_height))
        self.chessBoard = np.zeros((self.x_width, self.y_height), dtype=int)
        self.zeroBoard = np.zeros((self.x_width, self.y_height))  # self._p()

    def get_chessBoard(self):
        return copy.deepcopy(self.chessBoard)

    def _p(self):
        print(self.chessBoard)

    def get_playPoint(self, play_type=0):
        tmpPoints = np.where(self.chessBoard == play_type)
        points = list(zip(tmpPoints[0], tmpPoints[1]))
        return points

    def play_chess(self, play_point, play_type):
        _x, _y = play_point
        print('[play_chess] 玩家[%s]下点[%s,%s]' % (play_type, _x, _y))
        if self.chessBoard[_x, _y] != 0:
            print('[play_chess] 无效')
            return False
        self.chessBoard[_x, _y] = play_type
        self.zeroBoard[_x, _y] = 1
        return True

    def checkIsWinResult_One(self, _x, _y, play_type):
        isWin = False
        if self.horizontal_Match(_x, _y, play_type):
            isWin = True
        elif self.vertical_Match(_x, _y, play_type):
            isWin = True
        elif self.slantTop_Match(_x, _y, play_type):
            isWin = True
        elif self.slantBottom_Match(_x, _y, play_type):
            isWin = True
        self._p()
        if isWin:
            print('[play_chess] 玩家[%s]胜利' % (play_type))
        return isWin

    def checkIsWinResult_All(self, _x, _y, play_type):
        resultPointsList = []

        horizontal_result = self.horizontal_Match(_x, _y, play_type)
        if horizontal_result:
            resultPointsList.append(horizontal_result)

        vertical_result = self.vertical_Match(_x, _y, play_type)
        if vertical_result:
            resultPointsList.append(vertical_result)

        slantTop_Match_result = self.slantTop_Match(_x, _y, play_type)
        if slantTop_Match_result:
            resultPointsList.append(slantTop_Match_result)

        slantBottom_Match_result = self.slantBottom_Match(_x, _y, play_type)
        if slantBottom_Match_result:
            resultPointsList.append(slantBottom_Match_result)

        if resultPointsList:
            print('[check_is_win_all] 坐标(%s,%s) 类型[%s] 结果集 => %s' % (_x, _y, play_type, resultPointsList))

        return resultPointsList

    def horizontal_Match(self, play_x, play_y, play_type):
        '''横行判断(即y轴不变,与x轴平行)'''
        maxCount = 1  # 所下的点在横行方向(正反)连续个数
        points = []  # 符合条件的坐标集
        for _x in range(1, self.addMaxIndex):  # 反方向(-)(左边)
            curXpoint = play_x - _x
            curYpoint = play_y
            if curXpoint < 0:  # 超出边界
                break
            if self.chessBoard[curXpoint, curYpoint] != play_type:
                break
            maxCount += 1
            points.append((curXpoint, curYpoint))

        points.append((play_x, play_y))

        for x_ in range(1, self.addMaxIndex):  # 正方向(+)(右边)
            curXpoint = play_x + x_
            curYpoint = play_y
            if curXpoint >= self.x_width:  # 超出边界
                break
            if self.chessBoard[curXpoint, curYpoint] != play_type:
                break
            maxCount += 1
            points.append((curXpoint, curYpoint))

        points = self.sort_point(points)
        print('[horizontal_Match] maxCount', maxCount)
        print('[horizontal_Match] points', points)
        if maxCount >= 5:
            return points
        return []

    def vertical_Match(self, play_x, play_y, play_type):
        '''竖行判断(即x轴不变,与y轴平行)'''
        maxCount = 1  # 所下的点在竖直方向(正反)连续个数
        points = []  # 符合条件的坐标集
        for _y in range(1, self.addMaxIndex):  # 反方向(-)(上边)
            curXpoint = play_x
            curYpoint = play_y - _y
            if curYpoint < 0:  # 超出边界
                break
            if self.chessBoard[curXpoint, curYpoint] != play_type:
                break
            maxCount += 1
            points.append((curXpoint, curYpoint))

        points.append((play_x, play_y))

        for y_ in range(1, self.addMaxIndex):  # 正方向(+)(下边)
            curXpoint = play_x
            curYpoint = play_y + y_
            if curYpoint >= self.y_height:  # 超出边界
                break
            if self.chessBoard[curXpoint, curYpoint] != play_type:
                break
            points.append((curXpoint, curYpoint))
            maxCount += 1

        points = self.sort_point(points)
        print('[vertical_Match] maxCount', maxCount)
        print('[vertical_Match] points', points)
        if maxCount >= 5:
            return points
        return []

    def slantTop_Match(self, play_x, play_y, play_type):
        '''上斜判断/,XY轴同加减(即x轴+,y轴+和x轴-,y轴-)'''
        maxCount = 1  # 所下的点在上斜方向(正反)连续个数
        points = []  # 符合条件的坐标集
        for _x, _y in zip(range(1, self.addMaxIndex), range(1, self.addMaxIndex)):  # 反方向(-)(左下)
            curXpoint = play_x - _x
            curYpoint = play_y - _y
            if curXpoint < 0 or curYpoint < 0:  # 超出边界
                break
            if self.chessBoard[curXpoint, curYpoint] != play_type:
                break
            maxCount += 1
            points.append((curXpoint, curYpoint))

        points.append((play_x, play_y))

        for _x, _y in zip(range(1, self.addMaxIndex), range(1, self.addMaxIndex)):  # 正方向(+)(右下)
            curXpoint = play_x + _x
            curYpoint = play_y + _y
            if curXpoint >= self.x_width or curYpoint >= self.y_height:  # 超出边界
                break
            if self.chessBoard[curXpoint, curYpoint] != play_type:
                break
            maxCount += 1
            points.append((curXpoint, curYpoint))

        points = self.sort_point(points)
        print('[slantTop_Match] maxCount', maxCount)
        print('[slantTop_Match] points', points)
        if maxCount >= 5:
            return points
        return []

    def slantBottom_Match(self, play_x, play_y, play_type):
        '''下斜判断/,XY轴反加减(即x轴-,y轴+和x轴+,y轴-)'''
        maxCount = 1  # 所下的点在下斜方向(正反)连续个数
        points = []  # 符合条件的坐标集
        for _x, _y in zip(range(1, self.addMaxIndex), range(1, self.addMaxIndex)):  # 反方向(-)(左上)
            curXpoint = play_x - _x
            curYpoint = play_y + _y
            if curXpoint < 0 or curYpoint >= self.y_height:  # 超出边界
                break
            if self.chessBoard[curXpoint, curYpoint] != play_type:
                break
            maxCount += 1
            points.append((curXpoint, curYpoint))

        points.append((play_x, play_y))

        for _x, _y in zip(range(1, self.addMaxIndex), range(1, self.addMaxIndex)):  # 正方向(+)(右上)
            curXpoint = play_x + _x
            curYpoint = play_y - _y
            if curXpoint >= self.x_width or curYpoint < 0:  # 超出边界
                break
            if self.chessBoard[curXpoint, curYpoint] != play_type:
                break
            maxCount += 1
            points.append((curXpoint, curYpoint))

        points = self.sort_point(points)

        print('[slantBottom_Match] maxCount', maxCount)
        print('[slantBottom_Match] points', points)
        if maxCount >= 5:
            return points
        return []

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

    def check(self, play_type):
        for _zeroPoint in self.get_playPoint(play_type=0):
            # print(_zeroPoint)
            _x, _y = _zeroPoint
            if self.checkIsWinResult_All(_x, _y, play_type):
                print('[check] %s,%s 符合' % (_zeroPoint))
