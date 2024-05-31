EXP = 6         # Hệ số mũ dùng để đánh giá window
INF = 1 << 30
WIN_PTS = INF - 1


class Cell:
    EMPTY: int = 0
    X: int = 1
    O: int = 2


def toCell(s: str):
    match s:
        case "x" | "X":
            return Cell.X
        case "o" | 'O':
            return Cell.O
        case _:
            return Cell.EMPTY


def getOp(role: Cell):
    match role:
        case Cell.X:
            return Cell.O
        case Cell.O:
            return Cell.X
        case _:
            return Cell.EMPTY
