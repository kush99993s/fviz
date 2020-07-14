#!/usr/bin/python3

from __future__ import annotations
from argparse import ArgumentParser
from typing import Tuple, List
from os.path import exists, abspath, join
from .extract import (
    makeDir,
    extractAll
)
from .model.reactions import Reactions
from .plot.reactions import (
    plotReactionCount,
    plotPeerToReactionCount
)
from time import time


def _calculateSuccess(arr: List[bool]) -> float:
    '''
        Calculates percentage of success
    '''
    return (arr.count(True) / len(arr)) * 100


def _getCMD() -> Tuple[str, str, str]:
    '''
        Parses command line args, passed while invoking script
    '''
    parser = ArgumentParser()
    parser.add_argument('src',
                        type=str,
                        help='Exported compressed Facebook data as zip file')
    parser.add_argument('extractAt',
                        type=str,
                        help='Extraction location of zip')
    parser.add_argument('sink',
                        type=str,
                        help='Sink directory path, where plots to be placed')
    args = parser.parse_args()

    if not (args.src and args.extractAt and args.sink):
        return None, None, None
    if not (args.src.endswith('.zip') and exists(args.src) and makeDir(abspath(args.sink))):
        return None, None, None

    return tuple(map(lambda e: abspath(e), [args.src, args.extractAt, args.sink]))


def main():
    try:
        src, extractAt, sink = _getCMD()
        if not (src and extractAt and sink):
            raise Exception('Bad CMD args')

        if not extractAll(src, extractAt):
            raise Exception('Failed to extract zip')

        _starTm = time()
        reactions = Reactions.fromJSON(
            join(extractAt,
                 'likes_and_reactions/posts_and_comments.json'))

        if not reactions:
            raise Exception('Failed to parse reactions')

        _success = [
            plotReactionCount(
                reactions.reactionTypeToCount,
                'Reactions by {} [ {} - {} ]'.format(
                    reactions.reactions[0].actor,
                    *[i.strftime('%d %b, %Y') for i in reactions.getTimeFrame]
                ),
                join(
                    sink,
                    'reactionTypeToCountBy{}.png'.format(
                        reactions.reactions[0].actor
                    ))),
            plotPeerToReactionCount(
                reactions.getTopXPeerToReactionCount(10),
                'Top 10 profiles, with mostly reacted post(s) by {} [ {} - {} ]'.format(
                    reactions.reactions[0].actor,
                    *[i.strftime('%d %b, %Y') for i in reactions.getTimeFrame]
                ),
                join(
                    sink,
                    'top10ProfilesWithMostlyReactedPostsBy{}.png'.format(
                        reactions.reactions[0].actor
                    )))
        ]
        print('[+]Completed in {} s with {}% success'.format(
            time() - _starTm,
            _calculateSuccess(_success)))
    except KeyboardInterrupt:
        print('\n[!] Terminated')
    except Exception as e:
        print('[!] {}'.format(e))


if __name__ == '__main__':
    main()
N
