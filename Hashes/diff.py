import os
import sys


def main():
    functions = ['md5sum', 'sha1sum', 'sha224sum', 'sha256sum', 'sha384sum', 'sha512sum', 'b2sum']
    if os.path.isfile('hash.txt'):
        os.remove('hash.txt')
    for func in functions:
        os.system(f"cat hash.pdf personal.txt | {func} >> hash.txt")
        os.system(f"cat hash.pdf personal_.txt | {func} >> hash.txt")
    with open('hash.txt') as src:
        lines = src.readlines()
        hash_packs = zip(functions, [lines[2*n:2*n+2] for n in range(0, len(lines) // 2)])
    with open('diff.txt', 'w') as out:
        for function, hashes in hash_packs:
            hash1, hash2 = [bytes.fromhex(hash.split()[0]) for hash in hashes]
            xor = bytes(a ^ b for (a, b) in zip(hash1, hash2))
            diff = bin(int.from_bytes(xor, 'little')).count('1')
            total = len(hash1) * 8
            out.write(f"cat hash.pdf personal.txt | {function} >> hash.txt\n"
                      f"cat hash.pdf personal_.txt | {function} >> hash.txt\n"
                      f"{hashes[0].split()[0]}\n"
                      f"{hashes[1].split()[0]}\n"
                      f"Liczba bitów różniąca wyniki: {diff} tj. {diff/total * 100:.0f}% z {total}\n\n")


if __name__ == '__main__':
    main()