from . import *


WIDTH, HEIGHT = SCREEN_RESOLUTION = 600,401

pygame.init()
pygame.font.init()
display = pygame.display.set_mode(SCREEN_RESOLUTION)
clock = pygame.time.Clock()
_break = False
pause_menu = menus.PauseMenu(SCREEN_RESOLUTION)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            _break = True
            break
    if _break:
        break
    mouse_clicked = pygame.mouse.get_pressed()[0]
    pause_menu.update(mouse_clicked)
    pause_menu.draw(display)
    pygame.display.update()
pygame.quit()
sys.exit()