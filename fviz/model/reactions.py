#!/usr/bin/python3

from __future__ import annotations
from typing import List, Tuple, Dict
from datetime import datetime
from os.path import exists
from json import load
from functools import reduce
from .reactedContent import ReactedContent


class Reactions:
    '''
        Holds all reacted content realated information made by an actor
        in form of an ordered listed ( chronologically decreasing )
    '''

    def __init__(self, reactions: List[ReactedContent]):
        self._reactions = reactions

    @property
    def reactions(self) -> List[ReactedContent]:
        '''
            All reactions present under this object
        '''
        return self._reactions

    @property
    def groupByPeers(self) -> Dict[str, List[int]]:
        '''
            Groups all rections by peer name i.e. whose content is
            reacted to, on which ReactedContent instance

            Returns a mapping from peer name to list of ReactedContent indices
        '''
        buffer = {}

        for i, j in enumerate(self.reactions):
            _peer = j.peer

            if _peer not in buffer:
                buffer[_peer] = [i]
                continue

            buffer[_peer].append(i)

        return buffer

    def getReactionByIndex(self, index: int) -> ReactedContent:
        '''
            Returns ReactedContent object, looked up by
            index of that content in reaction set  
        '''
        if not (index >= 0 and index < self.count):
            return None

        return self._reactions[index]

    @property
    def count(self) -> int:
        '''
            Number of all reactions by actor
        '''
        return len(self._reactions)

    @property
    def getTimeFrame(self) -> Tuple[datetime, datetime]:
        '''
            Timeframe of all reactions present in data set, i.e.
            returns a 2-element tuple of datetimes, where first one
            is starting point & another one is ending point
        '''
        return self._reactions[self.count - 1].time, self._reactions[0].time

    @staticmethod
    def fromJSON(src: str) -> Reactions:
        '''
            Given path to data file, returns instance of this class
            holding all reacted contents, by actor
        '''
        if not exists(src):
            return None
        try:
            data = None
            with open(src, 'r') as fd:
                data = load(fd)

            if not data:
                return None

            return Reactions(
                list(map(lambda e: ReactedContent(e.get('title'),
                                                  e.get('data')[0].get(
                    'reaction').get('reaction'),
                    e.get('data')[0].get(
                    'reaction').get('actor'),
                    e.get('timestamp')), data['reactions']))
            )
        except Exception:
            return None


if __name__ == '__main__':
    print('It is not supposed to be used this way !')
