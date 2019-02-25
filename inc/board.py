import wiringpi

relays = [15, 2, 16, 3, 4, 7, 5, 0, 6, 13, 10, 21, 31, 22, 26, 27]
statuses = []

OUTPUT = 1
LOW = 0
HIGH = 1


def updateRelay(index: int, status: int):
    wiringpi.digitalWrite(relays[index], status)
    statuses[index] = status


def initialize():
    wiringpi.wiringPiSetup()
    for r in relays:
        wiringpi.pinMode(r, OUTPUT)
        statuses.append(LOW)
        wiringpi.digitalWrite(r, LOW)
