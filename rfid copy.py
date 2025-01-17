from rfidpy import SimpleMFRC522

reader = SimpleMFRC522()

while True:
    id, text = reader.read()
    print(id, text)