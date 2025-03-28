import chess
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from stockfish import Stockfish
import time

# Inicjalizacja Selenium i przeglądarki
#service = Service("chromedriver.exe")  # Ścieżka do chromedriver.exe
#driver = webdriver.ChromiumEdge(service=service)
#driver.get("https://lichess.org/editor/")

# Inicjalizacja szachownicy i Stockfisha
board = chess.Board()
stockfish = Stockfish("/usr/games/stockfish")
stockfish.set_depth(20)
stockfish.set_skill_level(20)

global roszadaWhite, roszadaBlack
roszadaWhite = True
roszadaBlack = True

# Funkcja do aktualizacji szachownicy na Lichess
def update_board_in_browser(board):
    fen = board.fen().replace(" ", "_")
    fen_url = f"https://lichess.org/editor/{fen}"
    #driver.get(fen_url)


def calculateMove(previousPosition):
    global roszadaWhite, roszadaBlack
    actualPosition = previousPosition
    while(previousPosition == actualPosition):
        with open("move.txt", "r") as file:
            actualPosition = file.readline().split(',')

            for element in previousPosition:
                if element not in actualPosition:
                    difference = element
                    print(difference)

            time.sleep(0.1)
            
    pionekRuszajacy = difference
    print(pionekRuszajacy)

    previousPosition = actualPosition
    lenPrevious = len(previousPosition)
    bicie = False

    while(previousPosition == actualPosition):
        with open("move.txt", "r") as file:
            actualPosition = file.readline().split(',')

            if lenPrevious - len(actualPosition) == 1:
                bicie = True
                for element in previousPosition:
                    if element not in actualPosition:
                        difference = element                        
                break
            elif lenPrevious - len(actualPosition) == -1:
                for element in actualPosition:
                    if element not in previousPosition:
                        difference = element
                break
            else:
                time.sleep(0.1)

    print(difference)
    previousPosition = actualPosition

    if bicie == True:
        pionekZbity = difference
        
        while(previousPosition == actualPosition):
            with open("move.txt", "r") as file:
                actualPosition = file.readline().split(',')

                for element in actualPosition:
                    if element not in previousPosition:
                        difference = element
                time.sleep(0.1)

        string = pionekRuszajacy + pionekZbity
        return string.lower(), actualPosition
    
    previousPosition = actualPosition
    if roszadaWhite == True:
        if pionekRuszajacy == 'E1':
            if difference == 'G1':
                print(1)
                _ruch = difference
                # Roszada krótka biała
                while(previousPosition == actualPosition):
                    with open("move.txt", "r") as file:
                        actualPosition = file.readline().strip().split(',')

                        for element in previousPosition:
                            if element not in actualPosition:
                                print(f"coś tam{element}")
                                _difference = element         
                        time.sleep(0.1)               

                previousPosition = actualPosition
                # print(_difference)

                while(previousPosition == actualPosition):
                    with open("move.txt", "r") as file:
                        actualPosition = file.readline().strip().split(',')

                        for element in actualPosition:
                            if element not in previousPosition:
                                print(f"coś tam2{element}")
                                __difference = element
                        time.sleep(0.1)               

                print(f"asdasdadas{actualPosition}")

                string = pionekRuszajacy + _ruch
                print(string.lower())

                return string.lower(), actualPosition
            elif difference == 'C1':
                _ruch = difference
                # Roszada długa biała
                while(previousPosition == actualPosition):
                    with open("move.txt", "r") as file:
                        actualPosition = file.readline().strip().split(',')

                        for element in previousPosition:
                            if element not in actualPosition:
                                _difference = element
                        time.sleep(0.1)

                previousPosition = actualPosition

                while(previousPosition == actualPosition):
                    with open("move.txt", "r") as file:
                        actualPosition = file.readline().strip().split(',')
                        
                        for element in actualPosition:
                            if element not in previousPosition:
                                _difference = element

                string = pionekRuszajacy + _ruch
                print(string.lower())

                return string.lower(), actualPosition
            else:
                roszadaWhite = False
    
    if roszadaBlack == True:
        if pionekRuszajacy == 'E8':
            if difference == 'G8':
                # Roszada krótka czarna
                _ruch = difference
                while(previousPosition == actualPosition):
                    with open("move.txt", "r") as file:
                        actualPosition = file.readline().strip().split(',')

                        for element in previousPosition:
                            if element not in actualPosition:
                                difference = element
                        time.sleep(0.1)               

                previousPosition = actualPosition

                while(previousPosition == actualPosition):
                    with open("move.txt", "r") as file:
                        actualPosition = file.readline().strip().split(',')

                        for element in actualPosition:
                            if element not in previousPosition:
                                difference = element
                
                string = pionekRuszajacy + _ruch
                print(string.lower())

                return string.lower(), actualPosition
            elif difference == 'C8':
                _ruch = difference
                # Roszada długa biaczarnała
                while(previousPosition == actualPosition):
                    with open("move.txt", "r") as file:
                        actualPosition = file.readline().strip().split(',')

                        for element in previousPosition:
                            if element not in actualPosition:
                                difference = element
                        time.sleep(0.1)              

                previousPosition = actualPosition

                while(previousPosition == actualPosition):
                    with open("move.txt", "r") as file:
                        actualPosition = file.readline().strip().split(',')

                        for element in actualPosition:
                            if element not in previousPosition:
                                difference = element
                
                string = pionekRuszajacy + _ruch
                print(string.lower())

                return string.lower(), actualPosition
            else:
                roszadaBlack = False

        
    string = pionekRuszajacy + difference

    return string.lower(), actualPosition
            


# Aktualizujemy szachownicę przed rozpoczęciem gry
update_board_in_browser(board)
print(board)
print("--------------------")

previousPosition = [
    "E1", "F1", "F8", "G8"
]

newPosition = [
    "E1", "F1", "F8", "G8"
]



# Pętla gry
while not board.is_game_over():
    try:
        # Ustawienie pozycji Stockfisha
        stockfish.set_fen_position(board.fen())

        # Ocena pozycji i propozycja ruchu Stockfisha
        stockfish_move = stockfish.get_top_moves(1)
        if not stockfish_move:
            print("Stockfish nie zwrócił żadnego ruchu. Gra zakończona.")
            break

        best_move = stockfish_move[0]["Move"]
        print(f"Ruch Stockfisha: {best_move}")



        # Wprowadzenie ruchu użytkownika
        move, newPosition = calculateMove(previousPosition)
        print(move)
        print(newPosition)
        previousPosition = newPosition

        # time.sleep(5)
        print(board.legal_moves)
        if chess.Move.from_uci(move) in board.legal_moves:
            board.push(chess.Move.from_uci(move))
            # Aktualizacja szachownicy w przeglądarce po ruchu gracza
            update_board_in_browser(board)
        else:
            print("Nielegalny ruch. Spróbuj ponownie.")
            continue

        # Wykonanie ruchu przez Stockfisha
        if not board.is_game_over() and best_move in [m.uci() for m in board.legal_moves]:
            board.push(chess.Move.from_uci(best_move))
            print(f"Stockfish wykonuje ruch: {best_move}")
            # Aktualizacja szachownicy w przeglądarce po ruchu Stockfisha
            update_board_in_browser(board)
        else:
            print("Stockfish nie może wykonać ruchu.")

        print(board)
        print("--------------------")
    except Exception as e:
        print(f"Błąd: {e}")
        break

# Koniec gry
print("Koniec gry.")
print("Wynik:", board.result())

# Zamknięcie przeglądarki
#driver.quit()
