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
# q: event queue
# time: current time
# evCount: counter of all popped events
# methods push, pop, and start as described in the problem description

class EvQueue:
    q = []
    evCount = 0
    time = 0

    def heapsort(self, iterable):

        h = []

        for value in iterable:
            heapq.heappush(h, value)

        return [heapq.heappop(h)for i in range(len(h))]

    def start(self):
        while len(self.q) != 0:
            self.pop()

    def checkNextFreeSpot(self, event, firstEvent):
        startIndex = self.q.index(firstEvent)
        event.t = event.t + 1
        for x2 in range(startIndex + 1, len(self.q)):
            tmp = self.q[x2][0]
            if tmp == event.t:
                event.t = event.t + 1
            else:
                break


    def push(self, event: Ev):
        for element in self.q:
            if event.t == element[0]:
                self.checkNextFreeSpot(event, element)
        heapq.heappush(self.q, (event.t, event))
        self.q = self.heapsort(self.q)
    #def push(self, event: Ev):
    #    doubleTimes = False
    #    for element in self.q:
    #        if element[0] == event.t:
    #            doubleTimes = True
    #    if doubleTimes:
    #         heapq.heappush(self.q, (event.t + 1, event))
    #       self.q = self.heapsort(self.q)
    #    else:
    #        heapq.heappush(self.q, (event.t, event))
    #        self.q = self.heapsort(self.q)

    def pop(self):
        event = self.q.pop(0)
        self.time = event[0]
        if (event[1].args[1] == "Beginn"):
            my_print(
                f'{event[0]}: Begin {event[1].args[0].id}')  # event[1].args[0].id, event[1].args[0].nextStation().stationsname, "Beginn"
            event[1].args[0].beginn_einkauf()
        elif (event[1].args[1] == "Ankunft"):
            my_print1(event[1].args[0].id, event[1].args[0].nextStation().stationsname, "Ankunft", event[0])
            event[1].args[0].ankunft_station()
        elif (event[1].args[1] == "Fertig"):
            my_print1(event[1].args[0].id, event[1].args[0].nextStation().stationsname, "Fertig", event[0])
            event[1].args[0].verlassen_station()


# class consists of
# name: station name
# buffer: customer queue
# delay_per_item: service time
# CustomerWaiting, busy: possible states of this station
class Station():
    # stationsname = "default"

    def __init__(self, delay_per_item, name):
        print("2. Initialize the new instance of Point.")
        self.delay_per_Item = delay_per_item
        self.stationsname = name
        self.buffer = deque([])
        self.busy = False

    def anstellen(self, customer):
        if (customer.shoppinglist[0][3] >= len(self.buffer)):
            if (len(self.buffer) == 0 and self.busy == False):
                self.buffer.append(customer)
                self.busy = True
                fertig = Ev(evQ.time + (self.delay_per_Item * customer.shoppinglist[0][2]),
                            customer.verlassen_station,
                            (customer, "Fertig"),
                            1)  # 1 eventuell weg
                evQ.push(fertig)
            else:
                self.buffer.append(customer)
        else:
            self.skippedStation(customer)

    def skippedStation(self, customer):
        my_print1(customer.id, self.stationsname, "skipped, because Stations q was this long: " + str(len(self.buffer)) + " | customer waiting time was: " + str(customer.nextStationMaxQueue()), evQ.time)
        customer.allDone = False
        Customer.dropped[self.stationsname] += 1
        customer.shoppinglist.pop(0)
        if not customer.shoppinglist:
            customer.duration = evQ.time - customer.startingTime
            my_print(f'{evQ.time}: Verlassen {customer.id}')
        else:
            anstellen = Ev(evQ.time + customer.shoppinglist[0][0] + 1, customer.ankunft_station,
                           (customer, "Ankunft"), 1)  # 1 eventuell weg
            evQ.push(anstellen)

    def fertig(self):
        self.busy = False
        customerDone = self.buffer.popleft()
        if (len(self.buffer) > 0):
            kunde = self.buffer[0]
            self.busy = True
            fertig = Ev(evQ.time + (self.delay_per_Item * kunde.shoppinglist[0][2]),
                        kunde.verlassen_station,
                        (self.buffer[0], "Fertig"),
                        1)
            evQ.push(fertig)
        self.createAnstellenEvent(customerDone)

    def createAnstellenEvent(self, customer):
        customer.shoppinglist.pop(0)
        if not customer.shoppinglist:
            Customer.duration = Customer.duration + (evQ.time - customer.startingTime)
            if customer.allDone:
                Customer.complete = Customer.complete + 1
                Customer.duration_cond_complete = Customer.duration_cond_complete + (evQ.time - customer.startingTime)
            my_print(f'{evQ.time}: Verlassen {customer.id}')
        else:
            anstellen = Ev(evQ.time + customer.shoppinglist[0][0] + 1, customer.ankunft_station,
                           (customer, "Ankunft"), 1)  # 1 eventuell weg
            evQ.push(anstellen)


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
    startingTime = 0
    allDone = True

    # please implement here

    def __init__(self, shoppinglist, id, time):
        self.shoppinglist = list(shoppinglist)
        self.id = id
        self.time = time

    def beginn_einkauf(self):
        Customer.count = Customer.count + 1
        self.startingTime = evQ.time
        ankunft = Ev(evQ.time + self.nextStationWalkTime(), self.ankunft_station, (self, "Ankunft"),
                     1)  # laufe zur ersten Station
        evQ.push(ankunft)

    def ankunft_station(self):
        if self.shoppinglist[0][1].stationsname == baecker.stationsname:
            Station.anstellen(baecker, self)
        elif self.shoppinglist[0][1].stationsname == metzger.stationsname:
            Station.anstellen(metzger, self)
        elif self.shoppinglist[0][1].stationsname == kaese.stationsname:
            Station.anstellen(kaese, self)
        elif self.shoppinglist[0][1].stationsname == kasse.stationsname:
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
        kunde = Customer(list(einkaufsliste), name + str(i), t)
        ev = Ev(t, kunde.beginn_einkauf, (kunde, "Beginn"), prio=1)
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
