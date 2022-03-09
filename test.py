

from random import randint
from AuWav.auwav import AuWav

au = AuWav('mudic.wav')
# au.play()
with open('data.txt') as f:
    DATA = f.read()

DATA = DATA.encode('ascii')
print(f"Encoding the following data {DATA}")
print(f"{len(DATA)} bytes")
g, bits = au.encode(DATA, key=1337)
# g.play()
DECODED = g.decode(bits, key=1337)
print(f"Should be: {DATA.decode('ascii')}")
print(f"It's decoded to: {DECODED}")

try:
    DECODED_W = g.decode(bits, key=randint(0,1000000))
    print(f"Decoded with wron key: {DECODED_W}")
except Exception:
    print(f"Decoding with the wrong key failed, which is very likely to happen.")