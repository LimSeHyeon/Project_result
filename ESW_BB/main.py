from PIL import Image, ImageDraw, ImageFont
import time
import random
from colorsys import hsv_to_rgb
from boss import Boss
from bullet import Bullet
from character import Character
from enemy import Enemy
from joystick import Joystick
from meat import Meat
from popup import Popup




def main():
    #클래스들을 통해 객체 생성(조이스틱, 캐릭터, draw)
    joystick = Joystick()
    user = Character(joystick.width, joystick.height)
    canvas = Image.new("RGB", (joystick.width, joystick.height))
    draw = ImageDraw.Draw(canvas, 'RGBA')

    font = ImageFont.truetype('/home/kau-esw/ESW_BB/font/DalseoHealingMedium.ttf', 15) #큰글자
    bigFont = ImageFont.truetype('/home/kau-esw/ESW_BB/font/DalseoHealingMedium.ttf', 20) #중간글자
    smallFont = ImageFont.truetype('/home/kau-esw/ESW_BB/font/DalseoHealingMedium.ttf', 8) #작은글자

    game_state = 'start' #게임시작
    howToPlay = False
    #txt 읽어오기
    with open("howToPlay.txt", "r") as f:
        directions = f.read()
    while game_state == 'start':
        draw.rectangle((0, 0, joystick.width, joystick.height), fill = (0,0,0)) #검은 배경
        if howToPlay == False: #게임 시작화면(로고 + PRESS A/B)
            logo = Image.open('/home/kau-esw/ESW_BB/image/logo.png')
            logo = logo.resize((120, 120))
            canvas.paste(logo, (70, 50))
            draw.text((95, 10), '빵야빵야', (255, 255, 255, 255), font = font)
            draw.text((20, 180), 'PRESS A -> GAME START...!!', (255, 255, 255, 255), font = font)
            draw.text((20, 200), 'PRESS B -> HOW TO PLAY', (255, 255, 255, 255), font = font)
            joystick.disp.image(canvas)
        else: #게임방법 띄우기
            draw.text((10, 10), directions, (255, 255, 255, 255), font = font)
            draw.text((20, 225), 'PRESS A -> GAME START...!!', (255, 255, 255, 255), font = font)
            joystick.disp.image(canvas)
    
        if not joystick.button_A.value:
            game_state = 'run' #A버튼 누르면 게임시작
        if not joystick.button_B.value:
            howToPlay = True #B버튼 누르면 게임방법
            

    #enemy, boss, bullet, meat, 팝업점수 객체를 담는 리스트 생성
    enemy_list = []
    bullet_list = []
    boss_list = []
    meat_list = []
    popup_list = []
    
    count = 0 #클락과 비슷한 개념으로 쓰일 예정
    a_gauge = 0 #스킬B 게이지
    kill_count = 0 #보스몬스터 죽인 횟수(점수)
    skillA_effect = 0 #몇 클락동안 효과를 보일지를 저장할 변수

    skill_command = {'A_used': False, 'B_used': False} #스킬은 한 번씩만 사용
    toward = 'right' #오른쪽 바라보며 시작하기 때문

    while game_state == 'run': #본게임 시작
        count += 1
        present_time = time.time() #랜덤값 생성
        rand4 = (random.randint(0, int(present_time))) % 4
        rand240 = (random.randint(0, int(present_time))) % 240
        
        #방향, 스폰위치 설정
        command = {'move': False, 'up_pressed': False , 'down_pressed': False, 'left_pressed': False, 'right_pressed': False, 'center_pressed': False}
        spawn_position = {'0': tuple([rand240, 0]), '1': tuple([0, rand240]), '2': tuple([243, rand240]), '3': tuple([rand240, 243])}
        
        if not joystick.button_U.value: #up pressed
            command['up_pressed'] = True
            command['move'] = True
            toward = 'up'

        if not joystick.button_D.value: #down pressed
            command['down_pressed'] = True
            command['move'] = True
            toward = 'down'

        if not joystick.button_L.value: #left pressed
            command['left_pressed'] = True
            command['move'] = True
            toward = 'left'

        if not joystick.button_R.value: #right pressed
            command['right_pressed'] = True
            command['move'] = True
            toward = 'right'

        #스킬A
        if not joystick.button_A.value: #A pressed
            if a_gauge == 100 and skill_command['A_used'] == False: #False일 때 한 번 사용
                enemy_list.clear()
                skill_command['A_used'] = True
                skillA_effect = 25
        
        #스킬B
        if not joystick.button_B.value: #B pressed
            if user.moving_gauge == 100 and skill_command['B_used'] == False: #False일 때 한 번 사용
                object_count = count + 30 #앞으로 30클락동안 효과 발생할 것
                skill_command['B_used'] = True

        #스킬B 효과발동
        if skill_command['B_used'] == True:
            if count < object_count:
                user.state = 'strong'
            else: #효과 끝
                user.state = 'alive'
        
        #enemy 생성
        if count % 10 == 0:
            enemy = Enemy(spawn_position['%d' % rand4])
            enemy_list.append(enemy)

        #bullet 생성
        if count % 5 == 0:
            bullet = Bullet(user.center, command, toward)
            bullet_list.append(bullet)
        
        #boss 생성
        if count > 0 and count % 100 == 0:
            boss = Boss(spawn_position['%d' % rand4])
            boss_list.append(boss)

        #meat 생성
        if count > 0 and count % 300 == 0:
            meat = Meat(rand240, rand240)
            meat_list.append(meat)

        #총알 맞았는지 or 맵 밖으로 나갔는지 확인
        for bullet in bullet_list:
            bullet.out_check()
            bullet.collision_check(boss_list)
            bullet.collision_check(enemy_list)
            if bullet.state != 'shot':
                bullet_list.remove(bullet)
            bullet.move()
            
        #각각의 몬스터마다 확인
        for enemy in enemy_list:
            enemy.kiss(user) #user와 부딪히는지 확인
            enemy.move(user.center) #이동
            enemy.check() #state 확인
            if enemy.state == 'dead': #팝업추가, 죽은 적 리스트에서 제거, 스킬A 게이지 추가
                popup3 = Popup(enemy.center, 'A', 3) #A+3 popup 생성
                popup_list.append(popup3)
                enemy_list.remove(enemy)
                if a_gauge < 98:
                    a_gauge += 3
                elif a_gauge >= 98:
                    a_gauge = 100
    
        for boss in boss_list:
            boss.kiss(user) #user와 부딪히는지 확인
            boss.move(user.center) #이동
            boss.check() #state 확인
            boss.set_image() #체력 상태에 따라 이미지 변경
            if boss.state == 'dead': #팝업추가, 죽은 보스 리스트에서 제거, 스킬A 게이지 추가
                popup5 = Popup(boss.center, 'A', 5) #A+5 popup 생성
                popupk = Popup([boss.center[0], boss.center[1]+20], 'kill', 1) #kill+1 popup 생성
                popup_list.append(popup5)
                popup_list.append(popupk)
                boss_list.remove(boss)
                kill_count += 1
                if kill_count == 10: #보스 10킬 달성하면 win
                    game_state = 'win'
                    continue
                if a_gauge < 96:
                    a_gauge += 5
                elif a_gauge >= 96:
                    a_gauge = 100

        for meat in meat_list:
            meat.eat(user)
            if meat.state == 'eaten': #고기 먹었는지 확인
                popupm = Popup(meat.center, 'health', 1) #먹은 고기 제거
                popup_list.append(popupm)
                meat_list.remove(meat)

        user.move(command) #캐릭터 이동, 벽 밖으로 못나감
        user.hitcheck() #몬스터와 부딪힌 상태인지 확인
        user.live_check() #죽었는지 확인
        user.set_image() #state에 따라 이미지 변경
            
        for popup in popup_list:
            if popup.state == 'erase': #다 쓴 팝업 지우기
                popup_list.remove(popup)

        if user.state == 'dead': #게임오버
            game_state = 'lose'
            continue
        else:

        #그림 그리기
            draw.rectangle((0, 0, joystick.width, joystick.height), fill = (0,0,0)) #흰 도화지 깔아주기
            back_img = Image.open('/home/kau-esw/ESW_BB/image/background.png') # 배경이미지 가져오기
            canvas.paste(back_img) #배경 그리기

            if toward == 'left': #user가 바라보는 방향에 따라 그림 좌우반전 시켜주기
                canvas.paste(user.appearance.transpose(Image.FLIP_LEFT_RIGHT), (int(user.position[0]), int(user.position[1])))
            else:
                canvas.paste(user.appearance, (int(user.position[0]), int(user.position[1])))
            
            for enemy in enemy_list: #enemy 그리기
                if enemy.state == 'alive':
                    canvas.paste(enemy.appearance, (int(enemy.position[0]), int(enemy.position[1])))

            for boss in boss_list: #boss 그리기
                if boss.state == 'alive':
                    canvas.paste(boss.appearance, (int(boss.position[0]), int(boss.position[1])))
        
            for bullet in bullet_list: #bullet 그리기
                if bullet.state == 'shot':
                    canvas.paste(bullet.appearance, (int(bullet.position[0]), int(bullet.position[1])))

            for meat in meat_list: #meat 그리기
                if meat.state != 'eaten':
                    draw.rectangle((tuple(meat.position)), outline = (0,0,0), fill = (113,1,24))

            for popup in popup_list: #popup 띄우기
                popup.show(draw, font)

            #스킬A 게이지 바            
            if a_gauge == 100 and skill_command['A_used'] == False: #스킬 사용 가능한 상태 : 위아래로 흔들림
                if count%2 == 0: #위
                    draw.rectangle((5, 216, 107, 224), outline = (0,0,0), fill = (255, 0, 0, 150))
                    draw.text((6, 215), 'A : 사용가능', (255, 255, 255, 255), font = smallFont)
                elif count%2 == 1: #아래
                    draw.rectangle((5, 218, 107, 226), outline = (0,0,0), fill = (255, 0, 0, 150))
                    draw.text((6, 217), 'A : 사용가능', (255, 255, 255, 255), font = smallFont)
            elif a_gauge == 100: #스킬 사용 후
                draw.rectangle((5, 217, 107, 225), outline = (0,0,0), fill = (0, 0, 0, 0))
                draw.rectangle((6, 218, 6 + a_gauge, 224), fill = (0, 255, 0, 150 ))
            else: #스킬 사용 전 : 점점 차오름
                draw.rectangle((5, 217, 107, 225), outline = (0,0,0), fill = (0, 0, 0, 0))
                draw.rectangle((6, 218, 6 + a_gauge, 224), fill = (150 + a_gauge, 0, 0, 150 ))
                draw.text((6, 216), 'A : %s%%' %a_gauge, (255, 255, 255, 255)) #얼마나 찼는지 적어줌

            # 스킬B 게이지 바
            if user.moving_gauge == 100 and skill_command['B_used'] == False: # 스킬 사용 가능한 상태 : 위아래로 흔들림
                if count%2 == 0: #위
                    draw.rectangle((5, 227, 107, 235), outline = (0,0,0), fill = (0, 0, 255, 150))
                    draw.text((6, 226), 'B : 사용가능!!', (255, 255, 255, 255), font = smallFont)
                elif count%2 == 1: #아래
                    draw.rectangle((5, 229, 107, 237), outline = (0,0,0), fill = (0, 0, 255, 150))
                    draw.text((6, 228), 'B : 사용가능!!', (255, 255, 255, 255), font = smallFont)
            elif user.moving_gauge == 100 and user.state == 'strong': #스킬 사용 중
                draw.rectangle((5, 228, 107, 236), outline = (0,0,0), fill = (0, 0, 0, 0))
                draw.rectangle((6, 229, 6 + int(user.moving_gauge), 235), fill = (255, 255, 0, 150))
            elif user.moving_gauge == 100 and user.state == 'alive': #스킬 끝난 후
                draw.rectangle((5, 228, 107, 236), outline = (0,0,0), fill = (0, 0, 0, 0))
                draw.rectangle((6, 229, 6 + int(user.moving_gauge), 235), fill = (0, 255, 0, 150))
            else: #스킬 사용 전 : 점점 차오름
                draw.rectangle((5, 228, 107, 236), outline = (0,0,0), fill = (0, 0, 0, 0))
                draw.rectangle((6, 229, 6 + int(user.moving_gauge), 235), fill = (0, 0, 155 + int(user.moving_gauge), 150))
                draw.text((6, 227), 'B : %s%%' %user.moving_gauge, (255, 255, 255, 150)) #얼마나 찼는지 적어줌
                
            draw.text((5, 5), 'HEALTH:%s' %user.health, (255, 255, 255)) #화면 좌측 상단
            draw.text((5, 15), 'KILL: %s' %kill_count, (255, 255, 255))  #체력, 점수 표시
    
            if skillA_effect > 0: # 스킬A 발동 -> 화면 하얘졌다 점차 보이기(폭탄 터지는 느낌)
                draw.rectangle((0, 0, 240, 240), fill = (255, 255, 255, skillA_effect*10))
                skillA_effect -= 1

            joystick.disp.image(canvas) # 화면에 찍기

    if game_state == 'lose' or game_state == 'win': #게임 승리 혹은 패배 시
        boss_list.clear()                           #모든 리스트 제거
        enemy_list.clear()
        bullet_list.clear()
        meat_list.clear()
        popup_list.clear()
        back_img = Image.open('/home/kau-esw/ESW_BB/image/background2.png')
        canvas.paste(back_img) #새 배경 그려주기
        if game_state == 'lose':
            draw.text((65, 80), 'GAME OVER !!', (255, 255, 255), font = bigFont) #게임 패배 시 GAME OVER !! 출력
        else:
            draw.text((75, 80), 'YOU WIN !!', (255, 255, 255), font = bigFont)   #게임 승리 시 YOU WIN !! 출력
        draw.text((85, 115), 'HEALTH : %s'%user.health, (255, 255, 255), font = font)
        draw.text((95, 130), 'KILL : %s'%kill_count, (255, 255, 255), font = font)
        draw.text((40, 180), 'PLAY AGAIN??  PRESS A', (255, 255, 255), font = font) #다시 플레이하려면 A버튼 누르기

        joystick.disp.image(canvas) #화면에 찍기
        
        while joystick.button_A.value: #A버튼 눌릴 때까지
            continue
        game_state = 'start' #게임 재시작
            

if __name__ == '__main__':
    while 1: #게임 반복을 위해 while문 안에서 진행
        main()