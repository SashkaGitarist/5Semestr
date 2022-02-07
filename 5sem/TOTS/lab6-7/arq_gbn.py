import random
from queue import Queue
from threading import Thread
from time import sleep, time
from colorama import init, Fore

init(autoreset=True)

stop = False
LOOP_DELAY = 0.002

SUCCESS_PACKS = set()


class Pack:
    id: int
    destination: str

    def __init__(self, id: int, destination: str):
        self.id = id
        self.destination = destination

    def __repr__(self) -> str:
        return f"{self.id} [{self.destination}]"


class Receiver(Thread):
    q: Queue[Pack]
    delay: float
    expected_pack_id: int

    def __init__(self, name: str, max_q_size: int, delay: float, channel):
        super().__init__(name=name)
        self.q = Queue(max_q_size)
        self.delay = delay
        self.channel = channel
        self.expected_pack_id = 1

    def run(self):
        while not stop:
            if self.q.empty():
                sleep(LOOP_DELAY)
                continue
            self.process_q()

    def process_q(self):
        sleep(self.delay)
        pack = self.q.get()

    def put(self, pack: Pack):
        if pack.id != self.expected_pack_id:
            print(
                f'***DEBUG: Receiver putted: {pack} WAITING {self.expected_pack_id}')
            last_success_pack = Pack(
                self.expected_pack_id-1, destination='sender')
            self.channel.put(last_success_pack)
            return
        self.q.put(pack)
        self.expected_pack_id = pack.id + 1
        print(
            f'***DEBUG: Receiver putted: {pack} WAITING {self.expected_pack_id}')


class Sender(Thread):
    packs_amount: int
    generator_delay: float
    current_pack_id: int
    timer: float
    sent_sequence_time: float
    last_success_pack_id: int
    sender_limit: int

    def __init__(self, name: str, packs_amount: int,
                 generator_delay: float, timer: float, limit: int, channel):
        super().__init__(name=name)
        self.packs_amount = packs_amount
        self.generator_delay = generator_delay
        self.channel = channel
        self.timer = timer
        self.sender_limit = limit
        self.current_pack_id = 1
        self.last_success_pack_id = 0
        self.sent_sequence_time = 0

    def run(self):
        while not stop:
            sleep(LOOP_DELAY)
            self.generate()
            if self.sent_sequence_time != 0 and time() - self.sent_sequence_time > self.timer:
                self.current_pack_id = self.last_success_pack_id + 1
                self.sent_sequence_time = 0
                print(f'***DEBUG: Sender sending {self.current_pack_id} pack')

    def put(self, pack: Pack):
        print(f'***DEBUG: Sender received pack: {pack}')
        self.last_success_pack_id = pack.id
        SUCCESS_PACKS.add(pack.id)
        self.current_pack_id = pack.id + 1
        self.sent_sequence_time = 0

    def generate(self):
        if self.current_pack_id > self.packs_amount:
            return

        if self.current_pack_id - self.last_success_pack_id > self.sender_limit:
            return
        sleep(self.generator_delay)
        pack_id = self.current_pack_id
        pack = Pack(pack_id, destination='receiver')
        print(f'***DEBUG: Sender generated pack: {pack}')
        self.current_pack_id = pack.id + 1

        if self.current_pack_id - self.last_success_pack_id > self.sender_limit:
            self.sent_sequence_time = time()
        self.channel.put(pack)


class Channel(Thread):
    error_factor: float
    q: Queue[Pack]
    delay: float

    def __init__(self, name: str, max_q_size: int, delay: float, error_factor: float):
        super().__init__(name=name)
        self.delay = delay
        self.q = Queue(max_q_size)
        self.error_factor = error_factor
        self.sender = None
        self.receiver = None

    def run(self):
        while not stop:
            if self.q.empty():
                sleep(LOOP_DELAY)
                continue
            sleep(self.delay)
            pack = self.q.get()
            if pack.destination == "receiver":
                if random.random() > self.error_factor:
                    self.receiver.put(pack)
                else:
                    print(f'***DEBUG: Chanel Lost : {pack}')
            elif pack.destination == "sender":
                self.sender.put(pack)

    def put(self, pack: Pack):
        self.q.put(pack)


def start(packs_amount=20):
    global stop

    print('\nARQ со возвратом на N кадров - (Go-back-n)')
    start_time = time()
    channel = Channel("channel", max_q_size=100, delay=0.05,
                      error_factor=0.8)
    sender = Sender("sender", packs_amount=packs_amount,
                    generator_delay=0.05, timer=0.5, limit=3,
                    channel=channel)
    receiver = Receiver("receiver", max_q_size=100,
                        delay=0.05, channel=channel)

    channel.receiver = receiver
    channel.sender = sender

    channel.start()
    receiver.start()
    sender.start()

    while not stop:
        sleep(0.3)
        if SUCCESS_PACKS:
            stop = max(SUCCESS_PACKS) == packs_amount

    channel.join()
    receiver.join()
    sender.join()

    print(Fore.RED + f'Обработалось за {time() - start_time}')
    return time() - start_time


if __name__ == '__main__':
    start()
