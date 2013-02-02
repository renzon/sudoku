# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from unittest import TestCase
import math

EMPTY=-1
IMPOSSIBLE=-2
class WrongPlace(Exception):
    pass




Exception()
class WrongPlace(Exception):
    pass


class NumberMatrix(object):
    def __init__(self,number,size):
        self.number=number
        self.matrix=[[EMPTY for i in range(size)] for i in range(size)]
        self.SQUARE_SIZE=int(math.sqrt(size))

    def element(self,line,column):
        return self.matrix[line][column]

    def validate_play(self ,number, line, column):
        if self.element(line,column) != EMPTY and self.number==number:
            raise WrongPlace()


    def play(self,number, line, column):
        if self.number==number:
            self.matrix[line][column]=number
        elif self.number>0:
            self.matrix[line][column]=IMPOSSIBLE
        self.horizontal_restriction(number, line, column)
        self.vertical_restriction(number, line, column)
        self.square_restriction(number, line, column)

    def horizontal_restriction(self,number, line, column):
        if self.number==number:
            size=len(self.matrix)
            for i in xrange(size):
                if column!=i:
                    self.matrix[line][i]=IMPOSSIBLE


    def vertical_restriction(self, number, line, column):
        if self.number==number:
            size=len(self.matrix)
            for i in xrange(size):
                if line!=i:
                    self.matrix[i][column]=IMPOSSIBLE

    def square_restriction(self, number, line, column):
        if self.number==number:
            square_line_coords=self.square_coords(line)
            square_column_coords=self.square_coords(column)
            for sq_line in square_line_coords:
                #horizontal restriction sq_line==line
                if sq_line!=line:
                    for sq_column in square_column_coords:
                         if sq_column!=column:
                             self.matrix[sq_line][sq_column]=IMPOSSIBLE



    def square_coords(self, coord):
        start=(coord//self.SQUARE_SIZE)*self.SQUARE_SIZE
        return xrange(start,start+self.SQUARE_SIZE)


class WrongNumber(Exception):
    pass


class NoSolution(Exception):
    pass


class Sudoku(object):
    def __init__(self,game):
        size=len(game)
        self.game=game
        self.matrix=[NumberMatrix(i,size) for i in xrange(1,size+1)]
        for line in xrange(size):
            for column in xrange(size):
                element=game[line][column]
                if element!=EMPTY:
                    self.play(element,line,column)


    def element(self,line,column):
        for nmatrix in self.matrix:
            element=nmatrix.element(line,column)
            if element>0:
                return element
        return EMPTY

    def play(self, number, line, column):
        if not 0<number<=len(self.game):
            raise WrongNumber()
        self.matrix[number-1].validate_play(number, line, column)
        for nmatrix in self.matrix:
            nmatrix.play(number, line, column)

    def game_state(self):
        size=len(self.game)
        return [[self.element(line,column) for column in xrange(size)] for line in xrange(size)]

    def options(self, line, column):
        return [m.number for m in self.matrix if m.element(line,column)==EMPTY]

    def tip(self):
        size=len(self.game)
        for line in xrange(size):
            for column in xrange(size):
                options=self.options(line,column)
                if len(options)==1:
                    return options[0],line,column

    def solve(self,log_on=False):
        tip=self.tip()
        while tip:
            self.play(*tip)
            tip=self.tip()
        if log_on:
            print "After Tip##################################"
            print self.game_state()
        if not self.is_solved():
            min_possibilities=self._min_possibilities()
            game_state=self.game_state()
            for p in min_possibilities:
                maybe_solution=Sudoku(game_state)

                maybe_solution.play(*p)
                if log_on:
                    print "Maybe Solution#########################################"
                    print maybe_solution.game_state()
                try:
                    return maybe_solution.solve()
                except:
                    if log_on:
                        print "Not a solution ####################################"
        else:
            return self
        raise NoSolution()




    def is_solved(self):
        size=len(self.game)
        for line in xrange(size):
            for column in xrange(size):
                if self.element(line,column)<0:
                    return False
        return True

    def _min_possibilities(self):
        min_possibilities=[]
        size=len(self.game)
        for line in xrange(size):
            for column in xrange(size):
                options=self.options(line,column)
                if len(options)==2:
                    return [(opt,line,column) for opt in options]
                if not min_possibilities and options:
                    min_possibilities=[(opt,line,column) for opt in options]
                elif 0<len(options)<len(min_possibilities):
                    min_possibilities=[(opt,line,column) for opt in options]
        return min_possibilities



class SudokuTests(TestCase):
    def test_solve(self):
        sudoku=Sudoku([[1,EMPTY,EMPTY],
                      [EMPTY,2,EMPTY],
                      [EMPTY,EMPTY,3]])
        sudoku=sudoku.solve()
        self.assertEqual([[1,3,2],
                          [3,2,1],
                          [2,1,3]],
                         sudoku.game_state())
        self.assertTrue(sudoku.is_solved())






    def test_tip(self):
        game_state=[[EMPTY,EMPTY],
                    [EMPTY,EMPTY]]
        sudoku=Sudoku(game_state)
        self.assertFalse(sudoku.tip())
        self.assertEqual(game_state,sudoku.game_state())

        sudoku=Sudoku([[1,EMPTY],
                       [EMPTY,EMPTY]])
        tip=sudoku.tip()
        self.assertEqual((2,0,1),tip)

        sudoku.play(*tip)
        tip=sudoku.tip()
        self.assertEqual((2,1,0),tip)

        sudoku.play(*tip)
        tip=sudoku.tip()
        self.assertEqual((1,1,1),tip)

        sudoku.play(*tip)
        self.assertEqual([[1,2],
                          [2,1]],
                         sudoku.game_state())

        self.assertFalse(sudoku.tip())

    def test_play(self):
        sudoku=Sudoku([[EMPTY]])
        self.assertEqual(EMPTY,sudoku.element(0,0))
        self.assertRaises(WrongNumber,sudoku.play,-1,0,0)
        self.assertRaises(WrongNumber,sudoku.play,2,0,0)
        self.assertEqual(EMPTY,sudoku.element(0,0))
        sudoku.play(1,0,0)
        self.assertEqual(1,sudoku.element(0,0))

        game_state=[[EMPTY,EMPTY],
         [EMPTY,EMPTY]]
        sudoku=Sudoku(game_state)
        self.assertEqual(game_state,sudoku.game_state())
        self.assertEqual([1,2],sudoku.options(0,0))
        self.assertEqual([1,2],sudoku.options(1,0))
        self.assertEqual([1,2],sudoku.options(1,1))
        self.assertEqual([1,2],sudoku.options(0,1))

        game_state[0][0]=1
        sudoku.play(1,0,0)
        self.assertEqual(game_state,sudoku.game_state())
        self.assertEqual([],sudoku.options(0,0))
        self.assertEqual([2],sudoku.options(1,0))
        self.assertEqual([1,2],sudoku.options(1,1))
        self.assertEqual([2],sudoku.options(0,1))

        self.assertRaises(WrongPlace,sudoku.play,2,0,0)
        self.assertEqual(game_state,sudoku.game_state())



class NumberMatrixTests(TestCase):
    def test_number_matrix_creation(self):
        self.assertEqual([[EMPTY]],NumberMatrix(1,1).matrix)
        self.assertEqual([[EMPTY,EMPTY],
                          [EMPTY,EMPTY]],NumberMatrix(1,2).matrix)

    def test_horizontal_restriction(self):
        nmatrix=NumberMatrix(1,2)

        nmatrix.horizontal_restriction(1,0,0)
        self.assertEqual([[EMPTY,IMPOSSIBLE],
                      [EMPTY,EMPTY]],nmatrix.matrix)

        nmatrix.horizontal_restriction(1,1,1)
        self.assertEqual([[EMPTY,IMPOSSIBLE],
                          [IMPOSSIBLE,EMPTY]],nmatrix.matrix)

    def test_vertical_restriction(self):
        nmatrix=NumberMatrix(1,2)
        nmatrix.vertical_restriction(2,0,1)
        self.assertEqual([[EMPTY,EMPTY],
                          [EMPTY,EMPTY]],nmatrix.matrix)

        nmatrix.vertical_restriction(1,0,0)
        self.assertEqual([[EMPTY,EMPTY],
                          [IMPOSSIBLE,EMPTY]],nmatrix.matrix)

        nmatrix.vertical_restriction(1,1,1)
        self.assertEqual([[EMPTY,IMPOSSIBLE],
                          [IMPOSSIBLE,EMPTY]],nmatrix.matrix)


    def test_square_restriction(self):
        nmatrix=NumberMatrix(1,4)
        nmatrix.square_restriction(2,0,0)
        result=[[EMPTY,EMPTY,EMPTY,EMPTY],
                [EMPTY,EMPTY,EMPTY,EMPTY],
                [EMPTY,EMPTY,EMPTY,EMPTY],
                [EMPTY,EMPTY,EMPTY,EMPTY]]
        self.assertEqual(result,nmatrix.matrix)

        nmatrix.square_restriction(1,0,0)
        result[1][1]=IMPOSSIBLE
        self.assertEqual(result,nmatrix.matrix)

        nmatrix.square_restriction(1,0,3)
        result[1][2]=IMPOSSIBLE
        self.assertEqual(result,nmatrix.matrix)

        nmatrix.square_restriction(1,3,1)
        result[2][0]=IMPOSSIBLE
        self.assertEqual(result,nmatrix.matrix)

        nmatrix.square_restriction(1,2,2)
        result[3][3]=IMPOSSIBLE
        self.assertEqual(result,nmatrix.matrix)


