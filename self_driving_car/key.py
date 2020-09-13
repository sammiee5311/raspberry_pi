import pygame

def init():
    pygame.init()
    win = pygame.display.set_mode((100,100))

def get_key(key_name):
    flag = False
    for eve in pygame.event.get():
        pass
    keyInput = pygame.key.get_pressed()
    key = getattr(pygame, 'K_%s' %key_name)
    if keyInput [key]:
        flag = True
    pygame.display.update()
    return flag

def main():
    continue

if __name__ == '__main__':
    init()
    while True:
        main()