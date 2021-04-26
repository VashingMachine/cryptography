from PIL import Image as PilImage
import numpy as np
import hashlib
import os

FRAME_SIZE = 4

def block_processing(image, dest, key, use_previous=False):
    image = image.copy()
    width, height = image.size
    w_iters = width // FRAME_SIZE
    h_iters = height // FRAME_SIZE
    previous = key
    for w in range(w_iters):
        for h in range(h_iters):
            crop = (w * FRAME_SIZE, h * FRAME_SIZE, (w + 1) * FRAME_SIZE, (h + 1) * FRAME_SIZE)
            np_frame = np.array(image.crop(crop)).flatten()
            message = np.bitwise_xor(np.packbits(np_frame), previous, dtype=np.uint8).tobytes()
            hash = hashlib.shake_256(message).digest(2)
            hash_array = np.frombuffer(hash, dtype=np.uint8)
            if use_previous:
                previous = hash_array
            output_frame = np.array(np.unpackbits(hash_array).reshape(FRAME_SIZE, FRAME_SIZE), dtype=bool)
            image.paste(PilImage.fromarray(output_frame), crop)
    image.save(dest)

def ecb(image, key):
    block_processing(image, 'ecb_crypto.bmp', key, use_previous=False)

def cbc(image, key):
    block_processing(image, 'cbc_crypto.bmp', key, use_previous=True)

def read_key():
    if os.path.isfile('key.txt'):
        with open('key.txt') as file:
            key = np.array([int(k) for k in file.read().split()], dtype=np.uint8)
    else:
        key = np.array([0, 0], dtype=np.uint8)
    return key

def main():
    source_image = PilImage.open("plain.bmp")
    bin_image = source_image.convert('L').point(lambda p: 255 if p > 200 else 0, mode='1')
    key = read_key()
    cbc(bin_image, key)
    ecb(bin_image, key)


if __name__ == '__main__':
    main()
