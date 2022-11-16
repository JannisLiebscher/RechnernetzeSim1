from threading import Thread
import time
from threading import Condition
import logging

from collections import deque
import heapq

# f = open("supermarkt.txt", "w")
# fc = open("supermarkt_customer.txt", "w")
# fs = open("supermarkt_station.txt", "w")
SCALING = 0.1

# print on console and into supermarket log
def my_print(msg):
    print(msg)
    f.write(msg + '\n')


# print on console and into customer log
# k: customer name
# s: station name
def my_print1(k, s, msg, time):
    t = time
    print(str(round(t, 4)) + ':' + k + ' ' + msg + ' at ' + s)
    fc.write(str(round(t, 4)) + ':' + k + ' ' + msg + ' at ' + s + '\n')


# print on console and into station log
# s: station name
# name: customer name
def my_print2(s, msg, name):
    #t = EvQueue.time
    # print(str(round(t,4))+':'+s+' '+msg)
    fs.write(str(round(t, 4)) + ':' + s + ' ' + msg + ' ' + name + '\n')

# class consists of
# name: station name
# buffer: customer queue
# delay_per_item: service time
# CustomerWaiting, busy: possible states of this station
class Station(Thread):
    # stationsname = "default"

    def __init__(self, delay_per_item, name):
        Thread.__init__(self)
        print("2. Initialize the new instance of Point.")
        self.delay_per_Item = delay_per_item
        self.stationsname = name
        self.buffer = deque([])
        self.busy = False
        self.condition = Condition()

    def run(self):
        self.condition.acquire()
        self.condition.wait()
        self.condition.release()
        while not self.killEv.is_set():
            self.condition.acquire()
            if len(self.buffer) != 0:
                customer = self.buffer.popleft()
                self.condition.release()
                time.sleep(self.delay_per_Item * customer.shoppinglist[0][2] * SCALING)
                self.condition.acquire()
                cutomer.condition.acquire()
                cutomer.condition.notify()
                cutomer.condition.release()
            else:
                self.condition.wait()
            self.condition.release()

# class consists of
# statistics variables
# and methods as described in the problem description
class Customer(Thread):
    served = dict()
    dropped = dict()
    complete = 0
    duration = 0
    duration_cond_complete = 0
    count = 0
    startingTime = 0
    allDone = True

    # please implement here

    def __init__(self, shoppinglist, id, time):
        Thread.__init__(self)
        self.shoppinglist = list(shoppinglist)
        self.id = id
        self.time = time
        self.skipped = False
        self.condition = Condition()


    def run(self):
        time.sleep(time * SCALING)
        while not self.shoppinglist.isEmpyt():
            # Läuft zur Station
            time.sleep(nextSTationWalkTime() * SCALING)
            # An Station anstellen
            nextStation().buffer.append(self)
            # Station benachrichtigen
            nextStation().acquire()
            nextStation().notify()
            nextStation().release()
            # Warten auf abshcluss an der Station
            self.condition.acquire()
            self.condition.wait()
            self.condition.release()
            removeCurrentListItem()

    def nextStationWalkTime(self):
        return self.shoppinglist[0][0]

    def nextStation(self):
        return self.shoppinglist[0][1]

    def nextStationItemCount(self):
        return self.shoppinglist[0][2]

    def nextStationMaxQueue(self):
        return self.shoppinglist[0][3]

    def removeCurrentListItem(self):
        self.shoppinglist.remove(0)


def startCustomers(einkaufslisteA, nameA, einkaufslisteB, nameB):
    i = 0
    delayA = 200
    delayB = 60
    startA = 0
    startB = 1
    while i < 30:
        if i < 9:
            kundeA = Customer(list(einkaufslisteA), nameA + str(i), startA + delayA * i)
            kundeA.start()
        kundeB = Customer(list(einkaufslisteB), nameB + str(i), startB + delayB * i)
        kundeB.start()
        i += 1

if __name__ == "__main__":
    baecker = Station(10,'Bäcker')
    metzger = Station(30,'Metzger')
    kaese = Station(60,'Käse')
    kasse = Station(5,'Kasse')
    baecker.start()
    metzger.start()
    kaese.start()
    kasse.start()
    Customer.served['Bäcker'] = 0
    Customer.served['Metzger'] = 0
    Customer.served['Käse'] = 0
    Customer.served['Kasse'] = 0
    Customer.dropped['Bäcker'] = 0
    Customer.dropped['Metzger'] = 0
    Customer.dropped['Käse'] = 0
    Customer.dropped['Kasse'] = 0
    einkaufsliste1 = [(10, baecker, 10, 10), (30, metzger, 5, 10), (45, kaese, 3, 5), (60, kasse, 30, 20)]
    einkaufsliste2 = [(30, metzger, 2, 5), (30, kasse, 3, 20), (20, baecker, 3, 20)]
    startCustomers(einkaufsliste1, 'A', einkaufsliste2, 'B')
    #my_print('Simulationsende: %is' % evQ.time)
    # my_print('Anzahl Kunden: %i' % (Customer.count
    #                                 ))
    # my_print('Anzahl vollständige Einkäufe %i' % Customer.complete)
    # x = Customer.duration / Customer.count
    # my_print(str('Mittlere Einkaufsdauer %.2fs' % x))
    # x = Customer.duration_cond_complete / Customer.complete
    # my_print('Mittlere Einkaufsdauer (vollständig): %.2fs' % x)
    # S = ('Bäcker', 'Metzger', 'Käse', 'Kasse')
    # for s in S:
    #     x = Customer.dropped[s] / (Customer.served[s] + Customer.dropped[s]) * 100
    #     my_print('Drop percentage at %s: %.2f' % (s, x))
    #
    # f.close()
    # fc.close()
    # fs.close()
