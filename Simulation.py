from collections import deque
import heapq

f = open("supermarkt.txt", "w")
fc = open("supermarkt_customer.txt", "w")
fs = open("supermarkt_station.txt", "w")


# print on console and into supermarket log
def my_print(msg):
    print(msg)
    f.write(msg + '\n')


# print on console and into customer log
# k: customer name
# s: station name
def my_print1(k, s, msg):
    t = EvQueue.time
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
# q: event queue
# time: current time
# evCount: counter of all popped events
# methods push, pop, and start as described in the problem description

class EvQueue:
    liste = heapq
    evCount = 0
    time = 0
    def push(event):
        heapq.heappush(liste, event)


# class consists of
# name: station name
# buffer: customer queue
# delay_per_item: service time
# CustomerWaiting, busy: possible states of this station
class Station():
    delay_per_item = 1
    stationsname = "default"
    busy = False
    buffer = deque

    def __init__(self,delay_per_item, name):
        print("2. Initialize the new instance of Point.")
        self.delay_per_Item = delay_per_item
        self.stationsnamename = name

    def anstellen(self, customer):
        if (Customer.nextStationMaxQueue(customer) <= len(self.buffer)):
            if (len(self.buffer) == 0 and self.busy == False):
                self.buffer.append(customer)
                self.busy = True
                fertig = Ev(EvQueue.time + (self.delay_per_Item * Customer.nextStationItemCount(customer)),
                            self.stationsname,
                            (customer, "Fertig"),
                            1) # 1 eventuell weg
                EvQueue.push(fertig)
            else:
                self.buffer.append(customer)
        else:
            Customer.removeCurrentListItem(customer)

    def fertig(self):
        self.busy = False
        customerDone = self.buffer.popleft()
        if (len(self.buffer) > 0):
            self.busy = True
            fertig = Ev(EvQueue.time + (self.delay_per_Item * Customer.nextStationItemCount(self.buffer[0])),
                        self.stationsname,
                        (self.buffer[0], "Fertig"),
                        1)  # 1 eventuell weg
            EvQueue.push(fertig)
        anstellen = Ev(EvQueue.time + (customerDone.shoppinglist[0][0]), customerDone.shoppinglist[2],
                    (customerDone, "Ankunft"), 1)  # 1 eventuell weg
        EvQueue.push(anstellen)




# please implement here


# class consists of
# statistics variables
# and methods as described in the problem description
class Customer():
    served = dict()
    dropped = dict()
    complete = 0
    duration = 0
    duration_cond_complete = 0
    count = 0

    def __init__(self, shoppinglist, id, time):
        self.shoppinglist = shoppinglist
        self.id = id
        self.time = time

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
        kunde = Customer(list(einkaufsliste), name + str(i), t)
        ev = Ev(t, kunde.run, prio=1)
        evQ.push(ev)
        i += 1
        t += dT


evQ = EvQueue()
baecker = Station(10, 'Bäcker')
metzger = Station(30, 'Metzger')
kaese = Station(60, 'Käse')
kasse = Station(5, 'Kasse')
Customer.served['Bäcker'] = 0
Customer.served['Metzger'] = 0
Customer.served['Käse'] = 0
Customer.served['Kasse'] = 0
Customer.dropped['Bäcker'] = 0
Customer.dropped['Metzger'] = 0
Customer.dropped['Käse'] = 0
Customer.dropped['Kasse'] = 0
# WalkTime - Name - ItemCount - MaxQueue
einkaufsliste1 = [(10, baecker, 10, 10), (30, metzger, 5, 10), (45, kaese, 3, 5), (60, kasse, 30, 20)] # 3 überspringen
einkaufsliste2 = [(30, metzger, 2, 5), (30, kasse, 3, 20), (20, baecker, 3, 20)]
startCustomers(einkaufsliste1, 'A', 0, 200, 30 * 60 + 1)
startCustomers(einkaufsliste2, 'B', 1, 60, 30 * 60 + 1)
evQ.start()
my_print('Simulationsende: %is' % EvQueue.time)
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
