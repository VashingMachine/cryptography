import argparse

KEY_SIZE = 64


def prepare(line_size=KEY_SIZE):
    with open("orig.txt") as src:
        orig = src.read()

    orig = orig.replace(',', '')
    orig = orig.replace('.', '')
    orig = orig.replace('\n', '')
    orig = orig.lower()

    split = []
    lines_count = len(orig) // line_size
    for l in range(lines_count):
        split.append(orig[l * line_size:(l + 1) * line_size])

    with open("plain.txt", 'w') as output:
        for line in split:
            output.write(line + '\n')


def encrypt():
    with open("key.txt") as src:
        key = src.read().strip()

    with open("plain.txt") as src:
        plain = src.readlines()

    encoded_lines = []
    for line in plain:
        line = line.replace('\n', '')
        encoded = [str(ord(key[idx]) ^ ord(letter)) for idx, letter in enumerate(line)]
        encoded_lines.append(encoded)

    with open("crypto.txt", 'w') as output:
        for line in encoded_lines:
            text = " ".join(line)
            output.write(text + '\n')


def analysis():
    with open("crypto.txt") as src:
        lines = src.readlines()

    lines = list(map(lambda line: list(map(lambda l: int(l), line.split())), lines))
    keys = []

    for i in range(KEY_SIZE):
        first = lines[0][i]
        space_intersection = -1
        not_space_intersection = -1
        key_found = False
        for n, line in enumerate(lines):
            if (first ^ line[i]) >> 5 == 2:
                space_intersection = n
            elif first ^ line[i] != 0:
                not_space_intersection = n

            if not_space_intersection >= 0 and space_intersection >= 0:
                space_encoded = lines[space_intersection][i]
                key = chr(space_encoded ^ ord(' '))
                keys.append(key)
                key_found = True
                break

        if not_space_intersection < 0 and space_intersection >= 0:
            space_encoded = first
            key = chr(space_encoded ^ ord(' '))
            keys.append(key)
            key_found = True

        if not key_found:
            keys.append('?')

    with open("decrypt.txt", 'w') as output:
        for line in lines:
            text = "".join(
                [chr(ord(keys[idx]) ^ letter) if keys[idx] != '?' else '?' for idx, letter in enumerate(line)])
            output.write(text + '\n')

    print("key: " + "".join(keys))


def parse_args():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-p', action='store_true')
    group.add_argument('-e', action='store_true')
    group.add_argument('-k', action='store_true')
    return parser.parse_args()


def main():
    args = parse_args()
    if args.p:
        prepare()
    elif args.e:
        encrypt()
    elif args.k:
        analysis()


if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
