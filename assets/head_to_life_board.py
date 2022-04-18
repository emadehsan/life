
'''
this script converts the head represented as ascii art in head.ascii.txt
to a board configuration in Game of Life.

Every ' ' (space) character is considered live.
Dead otherwise
'''
import pprint
from typing import List

class AsciiToBoard:

    @staticmethod
    def read_board_state() -> List[List[int]]:

        '''
        either ignore the '\n' new line character at the end of each line.
        or add a new line in the end of the of head.ascii.txt
        to equalize the number of chars in each line. because each other line has a \n
        at the end
        '''
        filepath = './assets/head.ascii.txt'
        # filepath = './head.ascii.txt'

        board = []
        with open(filepath, 'r') as f:
            line = f.readline()
            while len(line) > 0:
                row = []
                for c in line:
                    if c != '\n':
                        # insert a 1 for every space. 0 otherwise
                        row.append(
                            1 if c == ' ' else 0
                        )
                board.append(row)
                line = f.readline()

        print(len(board), ' x ', len(board[0]))
        return board



if __name__ == '__main__':
    AsciiToBoard.read_board_state()