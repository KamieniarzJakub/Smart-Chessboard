import chess
import webbrowser
from stockfish import Stockfish

board = chess.Board()
#PATH to local stockfish (ale można też dodać do ENV VARIABLES)
stockfish = Stockfish("stockfish/stockfish-windows-x86-64-avx2.exe")
stockfish.set_depth(20)
stockfish.set_skill_level(20)
stockfish.get_parameters()

while not board.is_game_over():
    stockfish.set_fen_position(board.fen())
    stockfish.get_evaluation() #100cp ~ 1 pawn advantage

    stockfish_move = stockfish.get_top_moves(1)[0]
    board.push_san(stockfish_move["Move"])
    print(stockfish_move)
    print(board)
    #webbrowser.open("https://lichess.org/editor/"+board.fen().replace(' ','_') )


    while not board.is_game_over():
        try:
            black_move = input("Ruch przeciwnika (SAN): ")
            board.push_san(black_move)
            break
        except:
            print("ILLEGAL MOVE - try again")
    print("--------------------")

print("CHECKMATE")