# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from sudoku import Sudoku, EMPTY

#game=[[5,8,EMPTY,EMPTY,EMPTY,7,EMPTY,EMPTY,EMPTY],
#      [EMPTY,EMPTY,6,4,5,EMPTY,8,EMPTY,EMPTY],
#      [EMPTY,EMPTY,7,EMPTY,3,EMPTY,EMPTY,EMPTY,1],
#      [1,EMPTY,EMPTY,EMPTY,EMPTY,9,EMPTY,2,EMPTY],
#      [8,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,6],
#      [EMPTY,6,EMPTY,2,EMPTY,EMPTY,EMPTY,EMPTY,4],
#      [7,EMPTY,EMPTY,EMPTY,9,EMPTY,2,EMPTY,EMPTY],
#      [EMPTY,EMPTY,1,EMPTY,2,3,9,EMPTY,EMPTY],
#      [EMPTY,EMPTY,EMPTY,8,EMPTY,EMPTY,EMPTY,1,3]]
#
#sudoku=Sudoku(game)
#sudoku=sudoku.solve()
#print sudoku.game_state()

#lets try the most difficult: http://news.yahoo.com/solve-hardest-ever-sudoku-133055603--abc-news-topstories.html
# It take a while ;)

difficult=[[8,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY],
           [EMPTY,EMPTY,3,6,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY],
           [EMPTY,7,EMPTY,EMPTY,9,EMPTY,2,EMPTY,EMPTY],
           [EMPTY,5,EMPTY,EMPTY,EMPTY,7,EMPTY,EMPTY,EMPTY],
           [EMPTY,EMPTY,EMPTY,EMPTY,4,5,7,EMPTY,EMPTY],
           [EMPTY,EMPTY,EMPTY,1,EMPTY,EMPTY,EMPTY,3,EMPTY],
           [EMPTY,EMPTY,1,EMPTY,EMPTY,EMPTY,EMPTY,6,8],
           [EMPTY,EMPTY,8,5,EMPTY,EMPTY,EMPTY,1,EMPTY],
           [EMPTY,9,EMPTY,EMPTY,EMPTY,EMPTY,4,EMPTY,EMPTY]]


sudoku=Sudoku(difficult)
sudoku=sudoku.solve(True)
print sudoku.game_state()