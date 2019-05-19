# coding=utf-8

class game(object):
    roomId = None

    def __init__(self, *args, **kwargs):
        self.players = [] * self.getPlayerCount()

    def getPlayerCount(self):
        return 2
