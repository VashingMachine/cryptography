import argparse

plain_file = 'plain.txt'
crypto_file = 'crypto.txt'
decrypt_file = 'decrypt.txt'
key_file = 'key.txt'
extra_file = 'extra.txt'
key_found_file = 'key-found.txt'


def euc_ext(a, b):
    if b > a:
        a, b = b, a
    if b == 0:
        return 1, 0
    p_a, p_b = euc_ext(b, a - (a // b) * b)
    return p_b, p_a - (a // b) * p_b


def code(letter: str):
    return ord(letter) - (65 if letter.isupper() else 97)


def inverse(num: int):
    assert num % 2 != 0 and num % 13 != 0, "Wybrany element nie ma elementu odwrotnego"
    return euc_ext(26, num)[1] % 26


class AffinicCypher:
    def __init__(self, a: int, b: int):
        self.a = a
        self.b = b

    def encode(self, text: str):
        output = []
        for letter in text:
            if letter.isupper():
                code = ord(letter) - 65
                output_code = (code * self.a + self.b) % 26
                output.append(chr(65 + output_code))
            elif letter.islower():
                code = ord(letter) - 97
                output_code = (code * self.a + self.b) % 26
                output.append(chr(97 + output_code))
            else:
                output.append(letter)
        return "".join(output)

    def decode(self, text: str):
        output = []
        a_inv = inverse(self.a)
        for letter in text:
            if letter.isupper():
                code = ord(letter) - 65
                output_code = a_inv * (code - self.b) % 26
                output.append(chr(65 + output_code))
            elif letter.islower():
                code = ord(letter) - 97
                output_code = a_inv * (code - self.b) % 26
                output.append(chr(97 + output_code))
            else:
                output.append(letter)
        return "".join(output)


class CesarCypher(AffinicCypher):
    def __init__(self, b):
        super().__init__(1, b)


class TaskProcessor:
    def __init__(self, args):
        self.mode = 'linear' if args.linear else 'cesar'
        if args.e:
            self.task = self.encode
        elif args.d:
            self.task = self.decode
        elif args.j:
            self.task = self.analysis_with_text
        else:
            self.task = self.analysis

    def encode(self):
        keys = self._read_key()

        with open(plain_file) as src:
            text = src.read()

        engine = AffinicCypher(*keys)
        cryptogram = engine.encode(text)

        with open(decrypt_file, 'w') as out:
            out.write(cryptogram)

    def decode(self):
        keys = self._read_key()

        with open(decrypt_file) as src:
            text = src.read()

        engine = AffinicCypher(*keys)
        plain = engine.decode(text)

        with open(plain_file, 'w') as out:
            out.write(plain)

    def analysis_with_text(self):
        with open(extra_file) as src:
            extra = src.read().rstrip()

        with open(decrypt_file) as src:
            encrypted = src.read().rstrip()

        if self.mode == 'cesar':
            key = str((ord(encrypted[0]) - ord(extra[0])) % 26)
        else:
            if all(ord(letter) % 2 == 0 for letter in extra) \
                    or all(ord(letter) % 2 == 1 for letter in extra) \
                    or len(extra) < 2 \
                    or len(extra) == 2 and (ord(extra[0]) - ord(extra[1])) % 13 == 0:
                print("Cannot extract key from such data")
                exit(-1)
            else:
                def matched_combination(a, b):
                    return (code(a) - code(b)) % 2 != 0 and (code(a) - code(b)) % 13 != 0

                found = False
                for idx_1, letter_1 in enumerate(extra):
                    for idx_2, letter_2 in enumerate(extra):
                        if matched_combination(letter_1, letter_2):
                            plain_1 = code(extra[idx_1])
                            enc_1 = code(encrypted[idx_1])
                            key_a = ((code(encrypted[idx_1]) - code(encrypted[idx_2])) * inverse(
                                (code(letter_1) - code(letter_2)) % 26)) % 26
                            key_b = (enc_1 - plain_1 * key_a) % 26
                            found = True
                            break
                    if found:
                        break
                key = f"{key_a} {key_b}"

        with open(key_found_file, 'w') as out:
            out.write(key)

    def analysis(self):
        with open(decrypt_file) as src:
            text = src.read().rstrip()
        counter = 0
        if self.mode == 'cesar':
            with open(plain_file, 'w') as out:
                for i in range(26):
                    engine = CesarCypher(i)
                    out.write(engine.decode(text) + '\n')
        else:
            with open(plain_file, 'w') as out:
                for a in range(26):
                    if a % 2 != 0 and a % 13 != 0:
                        for b in range(26):
                            counter += 1
                            engine = AffinicCypher(a, b)
                            to_write = engine.decode(text) + '\n'
                            print(to_write)
                            out.write(to_write)

        print(counter)

    def execute_task(self):
        self.task()

    def _read_key(self):
        with open(key_file) as src:
            keys = [int(key) for key in src.read().split()]
        if len(keys) == 1 and self.mode == 'cesar':
            keys = [1, *keys]
            print("Missing one key in file. Cesar mode only available")
        return keys


def parse_args():
    parser = argparse.ArgumentParser()
    c_group = parser.add_mutually_exclusive_group()
    c_group.add_argument('-c', '--cesar', action='store_true')
    c_group.add_argument('-a', '--linear', action='store_true')
    o_group = parser.add_mutually_exclusive_group()
    o_group.add_argument('-e', action='store_true')
    o_group.add_argument('-d', action='store_true')
    o_group.add_argument('-j', action='store_true')
    o_group.add_argument('-k', action='store_true')
    return parser.parse_args()


def main():
    args = parse_args()
    task_processor = TaskProcessor(args)
    task_processor.execute_task()


if __name__ == '__main__':
    main()
