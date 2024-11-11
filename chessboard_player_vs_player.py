import chess
import webbrowser
from stockfish import Stockfish

board = chess.Board()
#PATH to local stockfish (ale można też dodać do ENV VARIABLES)
stockfish = Stockfish("stockfish/stockfish-windows-x86-64-avx2.exe")
stockfish.set_depth(20)
stockfish.set_skill_level(20)
stockfish.get_parameters()
#webbrowser.open("https://lichess.org/editor/"+board.fen().replace(' ','_') )
print(board)
print("--------------------")
while not board.is_game_over():
    stockfish.set_fen_position(board.fen())
    stockfish.get_evaluation() #100cp ~ 1 pawn advantage

    stockfish_move = stockfish.get_top_moves(1)[0]
    print(stockfish_move)
    move = input("Twój ruch (UCI): ")
    if(chess.Move.from_uci(move) in board.legal_moves):
        board.push(chess.Move.from_uci(move))
    else:
        print("ILLEGAL MOVE - try again")
    #webbrowser.open("https://lichess.org/editor/"+board.fen().replace(' ','_') )
    print(board)
    print("--------------------")

print("END OF GAME")