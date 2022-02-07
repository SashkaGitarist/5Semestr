import random
from enum import Enum
from queue import Queue
from threading import Thread
from time import sleep, time

from colorama import init, Fore

init(autoreset=True)

stop = False
LOOP_DELAY = 0.002

SUCCESS_PACKS = []


class PackType(Enum):
    SUCCESS = "success"
    ERROR = "error"


class Pack:
    id: int
    destination: str
    type: PackType
    error_pack_id: int

    def __init__(self, id: int, destination: str, type: PackType):
        self.id = id
        self.destination = destination
        self.type = type

    def __repr__(self) -> str:
        return f"{self.id} [{self.destination}]"


class Receiver(Thread):
    q: Queue[Pack]
    delay: float

    def __init__(self, name: str, max_q_size: int, delay: float, channel):
        super().__init__(name=name)
        self.q = Queue(max_q_size)
        self.delay = delay
        self.channel = channel

    def run(self):
        while not stop:
            if self.q.empty():
                sleep(LOOP_DELAY)
                continue
            self.process_q()

    def process_q(self):
        sleep(self.delay)
        pack = self.q.get()
        if pack.type == PackType.SUCCESS:
            print(f'***DEBUG: Receiver proccessed: {pack}')
        else:
            print(f'Receiver lost {pack}')
        pack.destination = 'sender'
        self.channel.put(pack)

    def put(self, pack: Pack):
        self.q.put(pack)
        print(f'***DEBUG: Receiver putteed: {pack}')


class Sender(Thread):
    packs_amount: int
    q: Queue[Pack]
    delay: float
    generator_delay: float
    current_pack_id: int

    def __init__(self, name: str, packs_amount: int,
                 delay: float, generator_delay: float, channel):
        super().__init__(name=name)
        self.packs_amount = packs_amount
        self.q = Queue(self.packs_amount)
        self.delay = delay
        self.generator_delay = generator_delay
        self.channel = channel
        self.current_pack_id = 1

    def run(self):
        while not stop:
            self.generate()
            if self.q.empty():
                sleep(LOOP_DELAY)
                continue
            self.process_q()

    def process_q(self):
        sleep(self.delay)
        pack = self.q.get()
        if pack.type == PackType.ERROR:
            self.resend_pack(pack)
        else:
            SUCCESS_PACKS.append(pack.id)
            print(f'***DEBUG: Sender proccessed: {pack}')

    def put(self, pack: Pack):
        self.q.put(pack)

    def generate(self):
        if self.current_pack_id > self.packs_amount:
            return
        sleep(self.generator_delay)

        pack_id = self.current_pack_id
        self.current_pack_id += 1
        pack = Pack(pack_id, destination='receiver', type=PackType.SUCCESS)
        print(f'***DEBUG: Sender generated ask: {pack}')
        self.channel.put(pack)

    def resend_pack(self, pack: Pack):
        pack.destination = 'receiver'
        pack.type = PackType.SUCCESS
        print(f'***DEBUG: Sender resending: {pack}')
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
                if random.random() < self.error_factor:
                    pack.type = PackType.ERROR
                self.receiver.put(pack)
            elif pack.destination == "sender":
                self.sender.put(pack)

    def put(self, pack: Pack):
        self.q.put(pack)


def start(packs_amount=50):
    global stop

    print('\nARQ с избирательной повторной передачей (Selective repeat)')

    start_time = time()
    channel = Channel("channel", max_q_size=100, delay=0.05,
                      error_factor=0.3)
    sender = Sender("sender", packs_amount=packs_amount,
                    delay=0.05, generator_delay=0.05,
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
        stop = len(SUCCESS_PACKS) == packs_amount

    channel.join()
    receiver.join()
    sender.join()

    print(Fore.RED + f'Обработалось за {time() - start_time}')
    return time() - start_time


if __name__ == '__main__':
    start()
