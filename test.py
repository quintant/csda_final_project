

from AuWav.auwav import AuWav

au = AuWav('wizz.wav')

g = au.write_sine()

g.play()