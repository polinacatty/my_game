import pygame
import time

import src.consts as cst

from src.wtf import Run, Icons


def game():
    """The function launches the game from the menu state and maintains its correct state.

    The function also starts a round of the game.
    Args:
        None.
    Returns:
        None.
    """
    in_game = True
    pygame.init()
    myfont_120 = pygame.font.Font('src/fonts/18VAG Rounded M Bold.ttf', 120)
    myfont_60 = pygame.font.Font('src/fonts/18VAG Rounded M Bold.ttf', 60)
    screen = pygame.display.set_mode(cst.background_size, flags=pygame.SCALED | pygame.RESIZABLE, vsync=True)
    tx = myfont_120.render('START', True, cst.font_color)
    rct = tx.get_rect(topleft=cst.tx_menu)
    tx_res = myfont_60.render('RESULTS', True, cst.font_color)
    rct_res = tx_res.get_rect(topleft=cst.tx_results)
    tx_pt = myfont_60.render('PET', True, cst.font_color)
    rect_pt = tx_pt.get_rect(topleft=cst.tx_pet)
    tx_back = myfont_60.render('BACK', True, cst.font_color)
    rect_back = tx_back.get_rect(topleft=cst.tx_back)
    fps = 30

    shiba = 'shiba_white'

    r = Run(screen, shiba)

    state = 'menu'

    fon = pygame.Surface(cst.background_size)
    fon.fill(cst.background_color)

    records = []
    with open('src/numbers.txt', 'r') as f:
        for line in f:
            records.append(myfont_60.render('{0:.1f}'.format(float(line.strip())), True, cst.font_color))

    icn = Icons(screen)

    cnt = 0

    while in_game:
        if (state == 'game'):
            if not r.run():
                screen.blit(tx, cst.tx_menu)
                state = 'menu'
                records = []
                with open('src/numbers.txt', 'r') as f:
                    for line in f:
                        records.append(myfont_60.render('{0:.1f}'.format(float(line.strip())), True, cst.font_color))
        if (state == 'menu'):
            screen.blit(fon, cst.background_cords)
            screen.blit(tx, cst.tx_menu)
            screen.blit(tx_pt, cst.tx_pet)
            screen.blit(tx_res, cst.tx_results)
        if (state == 'res'):
            screen.blit(fon, cst.background_cords)
            screen.blit(tx_back, cst.tx_back)
            for i in range(len(records)):
                screen.blit(records[i], (553, 50 + i * 70))
        if (state == 'pet'):
            screen.blit(fon, cst.background_cords)
            screen.blit(tx_back, cst.tx_back)
            icn.draw(cnt // 12)
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                pygame.quit()
                in_game = False
            elif state == 'menu':
                mouse = pygame.mouse.get_pos()
                if (rct.collidepoint(mouse) and event.type == pygame.MOUSEBUTTONUP):
                    r = Run(screen, shiba)
                    state = 'game'
                elif (rct_res.collidepoint(mouse) and event.type == pygame.MOUSEBUTTONUP):
                    state = 'res'
                elif (rect_pt.collidepoint(mouse) and event.type == pygame.MOUSEBUTTONUP):
                    state = 'pet'
            elif state == 'res':
                mouse = pygame.mouse.get_pos()
                if (rect_back.collidepoint(mouse) and event.type == pygame.MOUSEBUTTONUP):
                    state = 'menu'
            elif state == 'pet':
                mouse = pygame.mouse.get_pos()
                if (rect_back.collidepoint(mouse) and event.type == pygame.MOUSEBUTTONUP):
                    state = 'menu'
                elif (icn.r1.collidepoint(mouse) and event.type == pygame.MOUSEBUTTONUP):
                    shiba = 'shiba_white'
                elif (icn.r2.collidepoint(mouse) and event.type == pygame.MOUSEBUTTONUP):
                    shiba = 'shiba_classic'
                elif (icn.r4.collidepoint(mouse) and event.type == pygame.MOUSEBUTTONUP):
                    shiba = 'cat_black'
                elif (icn.r5.collidepoint(mouse) and event.type == pygame.MOUSEBUTTONUP):
                    shiba = 'cat_red'
                elif (icn.r6.collidepoint(mouse) and event.type == pygame.MOUSEBUTTONUP):
                    shiba = 'cat_gray'
        pygame.display.update()
        cnt = ((cnt + 1) % 24)
        time.sleep(max(1 / fps - time.time() + r.time_, 0))
