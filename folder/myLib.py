import pygame
import numpy as np
import time
from tqdm import tqdm

pygame.mixer.init(frequency=44100, size=-16, channels=1)
sample_rate = 44100
duration_ms = 7
freq = 440

def generate_tone(amplitude):
    t = np.linspace(0, duration_ms / 1000, int(sample_rate * duration_ms / 1000), False)
    wave = amplitude * np.sin(2 * np.pi * freq * t)
    return wave.astype(np.int16)

# Создаём звуки для амплитуд 0, 30, 60, ..., 7650
step = 120
max_amplitude = 255 * step
sounds = []
for amp in range(0, max_amplitude + step, step):
    samples = generate_tone(amp)
    sound = pygame.mixer.Sound(buffer=samples)
    sounds.append(sound)

def play(x: int):
    """Минимум - 0 Максимум - 255"""
    amplitude_to_play = x * 120
    index = amplitude_to_play // step
    sounds[index].play()

def stream(x: bytes, bps: int | bool, view: bool = False, mode: str = 'progressbar'):
    b = list(x)
    start = time.time()
    if mode == 'progressbar':
        for amply in tqdm(b, 'Воспроизведение', unit='bytes', colour='blue'):
            a = time.time()
            while (a + (1 / bps) >= time.time()) if not bps is True else False:
                pass
            if view: print(amply)
            play(amply)
    elif mode == 'standart':
        for amply in b:
            a = time.time()
            while (a + (1 / bps) >= time.time()) if not bps is True else False:
                pass
            if view: print(amply)
            play(amply)
    elif mode == 'standart+':
        for amply in b:
            a = time.time()
            while (a + (1 / bps) >= time.time()) if not bps is True else False:
                pass
            if view: print(chr(amply), end='')
            play(amply)
    i = time.time() - start
    print('\nВремя на воспроизведение ушло:', i, 'секунд', end='\n')
    print('Байт было:', len(b))
    print('Секунд на один байт:', i / len(b))
    print('Байтов на одну секунду:', 1 / (i / len(b)))