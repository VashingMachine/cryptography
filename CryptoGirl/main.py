from PIL import Image as PilImage
import numpy as np
import hashlib

FRAME_SIZE = 4

def ecb(image: PilImage.Image):
    width, height = image.size
    w_iters = width // FRAME_SIZE
    h_iters = height // FRAME_SIZE
    for w in range(w_iters):
        for h in range(h_iters):
            crop = (w * FRAME_SIZE, h * FRAME_SIZE, (w + 1) * FRAME_SIZE, (h + 1) * FRAME_SIZE)
            np_frame = np.array(image.crop(crop)).flatten()
            message = np.packbits(np_frame).tobytes()
            hash = hashlib.md5(message).digest()[:2]
            output_frame = np.array(np.unpackbits(np.frombuffer(hash, dtype=np.uint8)).reshape(FRAME_SIZE, FRAME_SIZE), dtype=bool)
            image.paste(PilImage.fromarray(output_frame), crop)
    image.save("ecb.png")

def cbc(image):
    width, height = image.size
    w_iters = width // FRAME_SIZE
    h_iters = height // FRAME_SIZE
    previous_bytes = np.array([0, 0], dtype=np.uint8)
    for w in range(w_iters):
        for h in range(h_iters):
            crop = (w * FRAME_SIZE, h * FRAME_SIZE, (w + 1) * FRAME_SIZE, (h + 1) * FRAME_SIZE)
            np_frame = np.array(image.crop(crop)).flatten()
            message = np.bitwise_xor(np.packbits(np_frame), previous_bytes, dtype=np.uint8).tobytes()
            hash = hashlib.md5(message).digest()[:2]
            previous_bytes = np.frombuffer(hash, dtype=np.uint8)
            output_frame = np.array(np.unpackbits(previous_bytes).reshape(FRAME_SIZE, FRAME_SIZE), dtype=bool)
            image.paste(PilImage.fromarray(output_frame), crop)
    image.save("cbc.png")


def main():
    source_image: PilImage.Image = PilImage.open("girl.jpg")
    bin_image = source_image.convert('L').point(lambda p: 255 if p > 200 else 0, mode='1')
    # cbc(bin_image)
    ecb(bin_image)
    # test_frame = source_image.crop((0, 0, 4, 4))
    # np_frame = np.array(test_frame).flatten()
    #
    # np_frame_p = np.packbits(np_frame).tobytes()
    # hash = hashlib.shake_128(np_frame_p).digest(2)
    #
    # output_frame = np.unpackbits(np.frombuffer(hash, dtype=np.uint8)).reshape(4, 4)
    # print(output_frame)
    # print(np.array(test_frame))


if __name__ == '__main__':
    main()
