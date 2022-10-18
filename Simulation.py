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
    q = []
    evCount = 0
    time = 0
    heapq.heapify(q)

    def start(self):
        while len(self.q) != 0:
            self.pop()

    def push(self, event):
        heapq.heappush(self.q, event)

    def pop(self):
        event = heapq.heappop(self.q)


# class consists of
# name: station name
# buffer: customer queue
# delay_per_item: service time
# CustomerWaiting, busy: possible states of this station
class Station():
    delay_per_item = 1
    #stationsname = "default"
    busy = False
    buffer = deque

    def __init__(self, delay_per_item, name):
        print("2. Initialize the new instance of Point.")
        self.delay_per_Item = delay_per_item
        self.stationsname = name

    def anstellen(self, customer):
        if (customer.shoppinglist[0][2] <= len(self.buffer)):
            if (len(self.buffer) == 0 and self.busy == False):
                self.buffer.append(customer)
                self.busy = True
                fertig = Ev(EvQueue.time + (self.delay_per_Item * customer.shoppinglist[0][3]), self.stationsname,
                            (customer, "Fertig"), 1)  # 1 eventuell weg
                EvQueue.push(fertig)
            else:
                self.buffer.append(customer)
        else:
            customer.shoppinglist.remove(0)

    def fertig(self):
        self.busy = False
        customer = self.buffer.popleft()  # hier sollten wir uns noch den Customer speichern, da wir diesen noch benötigen um ihn zur nächsten Station zu schicken
        if (len(self.buffer) > 0):
            self.busy = True
            fertig = Ev(EvQueue.time + (self.delay_per_Item * self.buffer[0].shoppinglist[0][3]), self.stationsname,
                        (self.buffer[0], "Fertig"), 1)  # 1 eventuell weg
            EvQueue.push(fertig)
            ankunft = Ev(EvQueue.time + customer.shoppinglist[0][0], customer.shoppinglist[0][1], (customer, "Ankunft"),
                         1)  # 1 eventuell weg ?


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

    # please implement here

    def __init__(self, shoppinglist, id, time):
        self.shoppinglist = shoppinglist
        self.id = id
        self.time = time

    def beginn_einkauf(self):
        ankunft = Ev(EvQueue.time + self.shoppinglist[0][0], self.shoppinglist[0][1], (self, "Ankunft"), 1) # laufe zur ersten Station

    def ankunft_station(self):
        if self.shoppinglist[0][1] == baecker.stationsname:
            Station.anstellen(baecker, self)
        elif self.shoppinglist[0][1] == metzger.stationsname:
            Station.anstellen(metzger,self)
        elif self.shoppinglist[0][1] == kaese.stationsname:
            Station.anstellen(kaese, self)
        elif self.shoppinglist[0][1] == kasse.stationsname:
            Station.anstellen(kasse, self)

    def verlassen_station(self):



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
einkaufsliste1 = [(10, baecker, 10, 10), (30, metzger, 5, 10), (45, kaese, 3, 5), (60, kasse, 30, 20)]  # 3 überspringen
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

