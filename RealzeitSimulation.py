import threading
import time
import logging

from collections import deque
import heapq

f = open("supermarkt.txt", "w")
fc = open("supermarkt_customer.txt", "w")
fs = open("supermarkt_station.txt", "w")
SCALING = 30

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
    t = EvQueue.time
    # print(str(round(t,4))+':'+s+' '+msg)
    fs.write(str(round(t, 4)) + ':' + s + ' ' + msg + ' ' + name + '\n')


# class consists of instance variables:
# t: time stamp
# work: job to be done
# args: list of arguments for job to be done
# prio: used to give leaving, being served, and arrival different priorities
class Ev:
    counter = 0

    def __init__(self, t, work, args=(), prio=255):
        self.t = t
        self.n = Ev.counter
        self.work = work
        self.args = args
        self.prio = prio
        Ev.counter += 1


# class consists of
# name: station name
# buffer: customer queue
# delay_per_item: service time
# CustomerWaiting, busy: possible states of this station
class Station:
    # stationsname = "default"

    def __init__(self, delay_per_item, name):
        super().__init__()
        print("2. Initialize the new instance of Point.")
        self.delay_per_Item = delay_per_item
        self.stationsname = name
        self.buffer = deque([])
        self.busy = False
        self.condition = threading.Condition()
        self.condition.acquire()
        self.condition.wait()
        self.condition.release()


    def anstellen(self, customer):
        if customer.shoppinglist[0][3] >= len(self.buffer):
            if len(self.buffer) == 0 and self.busy == False:
                self.buffer.append(customer)
                self.busy = True
                customer.condition.acquire()
                customer.condition.wait(self.delay_per_Item * customer.shoppinglist[0][2] * SCALING)
            else:
                customer.condition.acquire()
                customer.condition.wait()
                self.buffer.append(customer)
        else:
            customer.skipped = True

    def fertig(self):
        self.busy = False
        customerDone = self.buffer.popleft()
        customerDone.condition.notify()
        customerDone.condition.release()
        if len(self.buffer) > 0:
            kunde = self.buffer[0]
            self.busy = True
            kunde.condition.wait(self.delay_per_Item * kunde.shoppinglist[0][2] * SCALING)
        else:
            self.condition.acquire()
            self.condition.wait()
            self.condition.release()


# please implement here


# class consists of
# statistics variables
# and methods as described in the problem description
class Customer:
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
        super().__init__()
        self.shoppinglist = list(shoppinglist)
        self.id = id
        self.time = time
        self.skipped = False
        self.condition = threading.Condition()
        self.tasks()

    def tasks(self):
        while self.shoppinglist:
            time.sleep(self.shoppinglist[0][0] * SCALING)
            self.skipped = False
            self.ankunft_station()
            if self.skipped == False:
                self.verlassen_station()

    def ankunft_station(self):
        if self.shoppinglist[0][1].stationsname == baecker.stationsname:
            baecker.condition.acquire()
            baecker.condition.notify()
            baecker.condition.release()
            Station.anstellen(baecker, self)
        elif self.shoppinglist[0][1].stationsname == metzger.stationsname:
            metzger.condition.acquire()
            metzger.condition.notify()
            metzger.condtion.release()
            Station.anstellen(metzger, self)
        elif self.shoppinglist[0][1].stationsname == kaese.stationsname:
            kaese.condition.acquire()
            kaese.condition.notify()
            kaese.condition.release()
            Station.anstellen(kaese, self)
        elif self.shoppinglist[0][1].stationsname == kasse.stationsname:
            kasse.condition.acquire()
            kasse.condition.notify()
            kasse.condition.release()
            Station.anstellen(kasse, self)

    def verlassen_station(self):
        if self.shoppinglist[0][1].stationsname == baecker.stationsname:
            Customer.served[baecker.stationsname] += 1
            Station.fertig(baecker)
        elif self.shoppinglist[0][1].stationsname == metzger.stationsname:
            Customer.served[metzger.stationsname] += 1
            Station.fertig(metzger)
        elif self.shoppinglist[0][1].stationsname == kaese.stationsname:
            Customer.served[kaese.stationsname] += 1
            Station.fertig(kaese)
        elif self.shoppinglist[0][1].stationsname == kasse.stationsname:
            Customer.served[kasse.stationsname] += 1
            Station.fertig(kasse)

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


def startCustomers(einkaufsliste, name, sT, dT, mT):
    i = 1
    t = sT
    while t < mT:
        kunde = threading.Thread(target=Customer, args=(list(einkaufsliste), name + str(i), t))
        kunde.start()
        i += 1
        t += dT


baecker = threading.Thread(target=Station, args=(10,'Bäcker'))
metzger = threading.Thread(target=Station, args=(30,'Metzger'))
kaese = threading.Thread(target=Station, args=(60,'Käse'))
kasse = threading.Thread(target=Station, args=(5,'Kasse'))
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
startCustomers(einkaufsliste1, 'A', 0, 200, 30 * 60 + 1)
startCustomers(einkaufsliste2, 'B', 1, 60, 30 * 60 + 1)
my_print('Simulationsende: %is' % evQ.time)
my_print('Anzahl Kunden: %i' % (Customer.count
                                ))
my_print('Anzahl vollständige Einkäufe %i' % Customer.complete)
x = Customer.duration / Customer.count
my_print(str('Mittlere Einkaufsdauer %.2fs' % x))
x = Customer.duration_cond_complete / Customer.complete
my_print('Mittlere Einkaufsdauer (vollständig): %.2fs' % x)
S = ('Bäcker', 'Metzger', 'Käse', 'Kasse')
for s in S:
    x = Customer.dropped[s] / (Customer.served[s] + Customer.dropped[s]) * 100
    my_print('Drop percentage at %s: %.2f' % (s, x))

f.close()
fc.close()
fs.close()
