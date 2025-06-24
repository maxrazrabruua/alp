import myLib as ml

with open('Java.zip', 'rb') as file:
    ml.stream(file.read(), True)

while True: pass