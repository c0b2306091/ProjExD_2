import os
import random
import sys
import time
import pygame as pg
import pygame


WIDTH, HEIGHT = 1600, 900
DELTA = {
    pg.K_UP:(0,-5),
    pg.K_DOWN:(0,+5),
    pg.K_LEFT:(-5,0),
    pg.K_RIGHT:(+5,0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))
#BGM再生（独自昨日）
def alarm():
    pygame.mixer.init(frequency = 44100)    # 初期設定
    pygame.mixer.music.load("なんでしょう？.mp3")     # 音楽ファイルの読み込み
    pygame.mixer.music.play(1)              # 音楽の再生回数(1回)
    while(1):
        a = input("Finish? --->")
        if(a is 'y'): break
    pygame.mixer.music.stop()               # 再生の終了
    return 0

def check_bound(obj_rct):
    """
    こうかとんRect，または，爆弾Rectの画面内外判定用の関数
    引数：こうかとんRect，または，爆弾Rect
    戻り値：横方向判定結果，縦方向判定結果（True：画面内／False：画面外）
    """
    yoko, tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right: 
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        tate = False
    return yoko, tate

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400
    bd_img = pg.Surface((20,20))
    bd_img.set_colorkey((0,0,0))
    pg.draw.circle(bd_img,(255,0,0),(10,10),10)
    bd_rct=bd_img.get_rect()
    bd_rct.center = random.randint(0,WIDTH),random.randint(0,HEIGHT)
    #ゲームオーバー画面
    black_img = pg.surface((WIDTH,HEIGHT)) #黒画面
    pg.draw.rect(black_img,(0),(0,0,WIDTH,HEIGHT))
    black_img.set_alpha(163)
    black_rct=black_img.get_rect()
    black_rct.center = WIDTH/2, HEIGHT/2
    go_kkR_img = pg.transform.rotozoom(pg.image.load("fig/2.png"), 0, 2.0)
    go_kkL_img = pg.transform.flip(go_kkR_img,True,False) #画像反転

    fonto = pg.font.Font(None,100) 
    txt = fonto.render("Game Over",True,(0))

    vx,vy = +5,+5
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bd_rct): #工科豚と爆弾の衝突
            #ゲームオーバー画面
            screen.blit(black_img,black_rct)
            screen.blit(txt,[WIDTH/2 - 170, HEIGHT/2 - 40])
            screen.blit(go_kkR_img, (500,370))
            screen.blit(go_kkL_img, (1050,370))
            pg.display.update()
            time.sleep(5)
            return
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv=[0,0]
        for k,v in DELTA.items():
            if key_lst[k]:
                sum_mv[0] += v[0]
                sum_mv[1] += v[1]
        if check_bound(kk_rct) != (True,True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        
        """ if key_lst[pg.K_UP]:
            sum_mv[1] -= 5
        if key_lst[pg.K_DOWN]:
            sum_mv[1] += 5
        if key_lst[pg.K_LEFT]:
            sum_mv[0] -= 5
        if key_lst[pg.K_RIGHT]:
            sum_mv[0] += 5 """
        kk_rct.move_ip(sum_mv)
        screen.blit(kk_img, kk_rct)
        if check_bound(kk_rct) != (True,True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        bd_rct.move_ip(vx, vy)       
        screen.blit(bd_img, bd_rct)
        yoko,tate=check_bound(bd_rct)
        if not yoko: #横方向のはみ出し
            vx *= -1
        if not tate: #縦方向のはみ出し
            vy *= -1
        pg.display.update()
        tmr += 1
        clock.tick(50)
        alarm()


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
