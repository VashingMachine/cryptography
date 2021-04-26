import argparse
import random


class InverseException(Exception):
    pass


def euc_ext(a, b):
    if b > a:
        a, b = b, a
    if b == 0:
        if a != 1:
            raise InverseException()
        return 1, 0
    p_a, p_b = euc_ext(b, a - (a // b) * b)
    return p_b, p_a - (a // b) * p_b


def inverse(num: int, base: int):
    try:
        a, b = euc_ext(base, num)
        return b % base
    except InverseException:
        return -1


class TaskExecutor:
    def __init__(self, args):
        self.args = args

    def generate_keys(self):
        with open('elgamal.txt') as src:
            prime, gen = [int(number) for number in src.readlines()]
        b = random.getrandbits(256)
        beta = pow(gen, b, prime)
        with open('private.txt', 'w') as out:
            out.writelines(str(line) + '\n' for line in [prime, gen, b])
        with open('public.txt', 'w') as out:
            out.writelines(str(line) + '\n' for line in [prime, gen, beta])

    def encrypt(self):
        with open('public.txt') as src:
            prime, gen, beta = [int(number) for number in src.readlines()]
        with open('plain.txt') as src:
            m = int(src.read())
        if m >= prime:
            print("Message is longer than prime! Aborting")
            return
        k = random.getrandbits(256)
        e1 = pow(gen, k, prime)
        e2 = m * pow(beta, k, prime) % prime
        with open('crypto.txt', 'w') as out:
            out.writelines(str(line) + '\n' for line in [e1, e2])

    def decrypt(self):
        with open('private.txt') as src:
            prime, gen, b = [int(number) for number in src.readlines()]
        with open('crypto.txt') as src:
            e1, e2 = [int(number) for number in src.readlines()]
        sub = pow(e1, b, prime)
        m = e2 * inverse(sub, prime) % prime
        with open('decrypt.txt', 'w') as out:
            out.write(str(m))

    def signature(self):
        with open('private.txt') as src:
            prime, gen, b = [int(number) for number in src.readlines()]
        with open('message.txt') as src:
            m = int(src.read())
        k = random.getrandbits(256)
        while inverse(k, prime - 1) < 0:
            k = random.getrandbits(256)
        r = pow(gen, k, prime)
        x = ((m - b * r) * inverse(k, prime - 1)) % (prime - 1)
        with open('signature.txt', 'w') as out:
            out.writelines(str(line) + '\n' for line in [r, x])

    def verify(self):
        with open('public.txt') as src:
            prime, gen, beta = [int(number) for number in src.readlines()]
        with open('message.txt') as src:
            m = int(src.read())
        with open('signature.txt') as src:
            r, x = [int(number) for number in src.readlines()]
        v1 = pow(gen, m, prime)
        v2 = (pow(r, x, prime) * pow(beta, r, prime)) % prime
        with open('verify.txt', 'w') as out:
            if v1 == v2:
                print("T\nSignature verified!")
                out.write("T\nSignature verified!")
            else:
                print("F\nSignature dissmised")
                out.write("F\nSignature dissmised")

    def execute(self):
        if self.args.k:
            self.generate_keys()
        elif self.args.e:
            self.encrypt()
        elif self.args.d:
            self.decrypt()
        elif self.args.s:
            self.signature()
        else:
            self.verify()


def parse_args():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-k', action='store_true')
    group.add_argument('-e', action='store_true')
    group.add_argument('-d', action='store_true')
    group.add_argument('-s', action='store_true')
    group.add_argument('-v', action='store_true')
    return parser.parse_args()


def main():
    args = parse_args()
    task = TaskExecutor(args)
    task.execute()


if __name__ == '__main__':
    main()
