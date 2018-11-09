import random
import sys
import time
Current_money = 0
betting_stack = 0
def show_top5(users):
	print("------------------------------------------------")
	i=0
	sorted_users=sorted(users.items(),key=lambda x: x[1][3],reverse=True) #승률순으로 정렬
	print("Top5! (승률기준)")
	for name in sorted_users[:5]:
		if(sorted_users[i][1][3]==0):
			continue
		print(str(i+1)+"."+str(sorted_users[i][0])+" : "+str(sorted_users[i][1][3]))
		i+=1

def login(users):
	try:
		ID = input("ID를 입력하세요 : ")
		trypasswd = input("비밀번호를 입력하세요 : ")

		if ID in users: #로그인한 사용자 정보 초기화
			password = users[ID][0]
			tries = users[ID][1]
			wins = users[ID][2]
			money = users[ID][3]

			if trypasswd == password:
				print("로그인 되었습니다.")
			else:
				print("비밀번호가 틀립니다.")
				return login(users)
		else:
			users[ID] = (trypasswd, 0, 0, 0)
			password = users[ID][0]
			tries = users[ID][1]
			wins = users[ID][2]
			money = users[ID][3]
		return ID,tries,wins,money
	except KeyboardInterrupt:
		print("종료합니다.")

def store(users):
	print("결과를 저장합니다.")
	file = open('users.txt','w')
	names = users.keys()
	for name in names:
		passwd, tries, wins, money = users[name]
		line = name + "," + passwd + "," + str(tries) + "," + str(wins) + "," + str(money) + "\n"
		file.write(line)
	file.close()

def load_users():
	file=open("users.txt", "r")
	users = {}
	for line in file:
		ID, password, tries, wins, money = line.strip('\n').split(',')
		users[ID] = (password,int(tries), int(wins), float(money))
	file.close()
	return users

def winner(who,wins):
	global player_money , computer1_money , computer2_money , Current_money
	print(str(who['이름']) + "이(가) 승리했습니다")
	if who == You:
		player_money += Current_money
		wins += 1
	elif who == Com1:
		computer1_money += Current_money
	elif who == Com2:
		computer2_money += Current_money
	print("================================================")
	print("                   /  현재 보유금액")
	print(User['이름']+" :",player_money)
	print("\'아 귀\'' :",computer1_money)
	print("\'정마담\'' :",computer2_money)
	return wins

def make_percentage(percent): #0~100숫자입력-> 확률

	skill_percentage = []
	for _ in range(100):
		skill_percentage.append(0)
	for _ in range(percent):
		skill_percentage.remove(skill_percentage[0])
		skill_percentage.append(1)
	random.shuffle(skill_percentage)
	if skill_percentage[0] == 1:
		return True #스킬 성공
	elif skill_percentage[0] == 0:
		return False #스킬 실패

def change_handcard(wins): #스킬1 밑장빼기
	global player , deck, player_money,User
	try:
		if make_percentage(User['Skill_Percentage']) == True:
			print("타짜의 손기술이 성공하였습니다!")

			change_card = input("밑장빼기 후 덱에 돌려줄 패를 선택하세요.. 1.첫번째 패 2.두번째 패  :  ")
			while not (change_card == '1' or change_card == '2'):
				change_card = input("밑장빼기 후 덱에 돌려줄 패를 선택하세요. 1. 첫번째 패 2. 두번째 패  :  ", ' ')
			if change_card == '1':
				card, deck = hit(deck)
				player[0]=card
			elif change_card == '2':
				card, deck = hit(deck)
				player[1]=card
			You['rank'] , You['what_jokbo'] , You['score'] = jokbo(player)
			print("내 패")
			for i in player:
					if i == 1:
						print('1(광)', end = ' ')
					elif i == 3:
						print('3(광)', end = ' ')
					elif i == 4:
						print('4(열끗)', end = ' ')
					elif i == 7:
						print('7(열끗)', end = ' ')
					elif i == 8:
						print('8(광)', end = ' ')
					elif i == 9:
						print('3(열끗)', end = ' ')
					else:
						print(abs(i),"월", end = ' ')
			print('  /  현재 '+User['이름']+'의 족보는 : ' , You['what_jokbo'])
			wins = player_turn(wins)
		else:
			print("으악!!손기술을 사용하다 발각되었습니다!!!!!!")
			if player_money > 100000000:
				print("벌금으로 1억을 몰수합니다ㅠㅠ")
				player_money -= 100000000
			else:
				print("벌금을 낼 돈이 없어요ㅠㅠㅠ")
				print("================================================")
				print("       G    A    M    E    O    V    E    R")
				print("================================================")
				sys.exit(1)
	except KeyboardInterrupt:
		print("G  O  O  D  B  Y  E  !")

def exchange(wins): #스킬 2 바꿔치기
	global player_money,User
	try:
		if make_percentage(User['Skill_Percentage']) == True:
			print("타짜의 손기술이 성공하였습니다!")
			change_card = input("어떤 패를 바꿔치기 하시겠습니까? 1.첫번째 패 2.두번째 패  :  ")
			while not (change_card == '1' or change_card == '2'):
				change_card = input("어떤 패를 교체 하시겠습니까? 1. 첫번째 패 2. 두번째 패 :  ")
			who = input("누구와 패를 바꿔치기 하시겠습니까? 1.아귀 2.정마담 :")
			while not (who == '1' or who == '2'):
				who = input("누구와 패를 바꿔치기 하시겠습니까? 1.아귀 2.정마담  :  ")
			index = int(change_card) - 1
			if who == '1':
				computer1.append(player[index])
				player.remove(player[index])
				player.append(computer1[1])
				computer1.remove(computer1[1])
				You['rank'] , You['what_jokbo'] , You['score'] = jokbo(player)
				Com1['rank'] , Com1['what_jokbo'] , Com1['score'] = jokbo(computer1)
				Com1['check_percentage'] = (round(Com1['rank'] * 5)) + 50
				if Com1['rank'] == -1:
					Com1['check_percentage'] = 0
				for i in player:
						if i == 1:
							print('1(광)', end = ' ')
						elif i == 3:
							print('3(광)', end = ' ')
						elif i == 4:
							print('4(열끗)', end = ' ')
						elif i == 7:
							print('7(열끗)', end = ' ')
						elif i == 8:
							print('8(광)', end = ' ')
						elif i == 9:
							print('3(열끗)', end = ' ')
						else:
							print(abs(i),"월 끗", end = ' ')
				print('  /  현재 '+User['이름']+'의 족보는 : ' , You['what_jokbo'])
				wins = player_turn(wins)
			if who == '2':
				computer2.append(player[index])
				player.remove(player[index])
				player.append(computer2[1])
				computer2.remove(computer2[1])
				You['rank'] , You['what_jokbo'] , You['score'] = jokbo(player)
				Com2['rank'] , Com2['what_jokbo'] , Com2['score'] = jokbo(computer2)
				Com2['check_percentage'] = (round(Com2['rank'] * 5)) + 50
				if Com2['rank'] == -1:
					Com2['check_percentage'] = 0
					print("내 패")
				print("내 패")
				for i in player:
						if i == 1:
							print('1(광)', end = ' ')
						elif i == 3:
							print('3(광)', end = ' ')
						elif i == 4:
							print('4(열끗)', end = ' ')
						elif i == 7:
							print('7(열끗)', end = ' ')
						elif i == 8:
							print('8(광)', end = ' ')
						elif i == 9:
							print('3(열끗)', end = ' ')
						else:
							print(abs(i),"월 끗", end = ' ')
				print('  /  현재 '+User['이름']+'의 족보는 : ' , You['what_jokbo'])
				wins = player_turn(wins)
		else:
			print("으악!!손기술을 사용하다 발각되었습니다!!!!!!")
			if player_money > 100000000:
				print("벌금으로 1억을 몰수합니다ㅠㅠ")
				player_money -= 100000000
			else:
				print("벌금을 낼 돈이 없어요ㅠㅠㅠ")
				print("================================================")
				print("       G    A    M    E    O    V    E    R")
				print("================================================")
				sys.exit(1)
	except KeyboardInterrupt:
		print("G  O  O  D  B  Y  E  !")

def fake(wins): #스킬 3 뻥카
	global player_betting_money , betting_stack , player_money , Current_money

	if make_percentage(User['Skill_Percentage']) == True:
		print("타짜의 손기술이 성공하였습니다!")
		betting_stack *= 2
		player_money -= (betting_stack - You['betting_money'])
		Current_money += (betting_stack - You['betting_money'])
		You['betting_money'] = betting_stack
		Com1['check_percentage'], Com2['check_percentage'] = round(Com1['check_percentage'] // 2) , round(Com2['check_percentage'] // 2)
		print("과감한 베팅으로 상대방의 기가 죽었습니다.")
		wins = player_turn(wins)
	else:
		print("으악!!손기술을 사용하다 발각되었습니다!!!!!!")
		if player_money > 100000000:
			print("벌금으로 1억을 몰수합니다ㅠㅠ")
			player_money -= 100000000

		else:
			print("벌금을 낼 돈이 없어요ㅠㅠㅠ")
			print("================================================")
			print("       G    A    M    E    O    V    E    R")
			print("================================================")
			sys.exit(1)


def peek(wins): #스킬 4 훔쳐보기
	global player_money
	try:
		if make_percentage(User['Skill_Percentage']) == True:
			print(User['이름']+"의 손기술이 성공하였습니다!")
			who = input("누구의 패를 훔쳐보시겠습니까? 1.아귀 2.정마담  :  ")
			while not (who == '1' or who == '2'):
				who = input("누구의 패를 훔쳐보시겠습니까? 1.아귀 2.정마담  :  ")
			if who == '1':
				print("아귀의 손에", abs(computer1[0]), "이(가) 있습니다")
				wins = player_turn(wins)
			if who == '2':
				print("정마담의 손에", abs(computer2[0]), "이(가) 있습니다")
				wins = player_turn(wins)
		else:
			print("으악!!손기술을 사용하다 발각되었습니다!!!!!!")
			if player_money > 100000000:
				print("벌금으로 1억을 몰수합니다ㅠㅠ")
				player_money -= 100000000
			else:
				print("벌금을 낼 돈이 없어요ㅠㅠㅠ")
				print("================================================")
				print("       G    A    M    E    O    V    E    R")
				print("================================================")
				sys.exit(1)
	except KeyboardInterrupt:
		print("G  O  O  D  B  Y  E  !")

def skill_confirm(wins):
    global User , ski1 , ski2 , skill_1 , skill_2, name1, name2
    if ski1 == '1':
        name1='밑장빼기'
        def skill_1():
        	change_handcard(wins)
    elif ski1 == '2':
        name1='바꿔치기'
        def skill_1():
            exchange(wins)
    elif ski1 == '3':
        name1='뻥   카'
        def skill_1():
        	fake(wins)
    elif ski1 == '4':
        name1='훔쳐보기'
        def skill_1():
            peek(wins)
    if ski2 == '1':
        name2='밑장빼기'
        def skill_2():
        	change_handcard(wins)
    elif ski2 == '2':
        name2='바꿔치기'
        def skill_2():
            exchange(wins)
    elif ski2 == '3':
        name2='뻥   카'
        def skill_2():
        	fake(wins)
    elif ski2 == '4':
        name2='훔쳐보기'
        def skill_2():
            peek(wins) #스킬 셋

def choose_character(wins):
	try:
		character = input("캐릭터를 선택해 주세요. 1.평경장(하) 2.고광렬(중) 3.고니(상) ")
		global User,AI1,AI2
		while not (character == '1' or character == '2' or character == '3'):
			character = input("캐릭터를 선택해 주세요. 1.평경장(하) 2.고광렬(중) 3.고니(상) ")
		if character == '1':
			User = {'이름' : '\'평경장\'' , 'Start_money' : 300000000, 'Skill_Percentage' : 70,'standard_pandon' : 10000000}
			AI1 = {'이름' : '\'Computer1\'', 'Start_money' : 200000000, 'Skill_Percentage' : 60}
			AI2 = {'이름' : '\'Computer2\'', 'Start_money' : 200000000, 'Skill_Percentage' : 60}
		elif character == '2':
			User = {'이름' : '\'고광렬\'' , 'Start_money' : 300000000, 'Skill_Percentage' : 55,'standard_pandon' : 20000000}
			AI1 = {'이름' : 'Computer1', 'Start_money' : 500000000, 'Skill_Percentage' : 70}
			AI2 = {'이름' : 'Computer2', 'Start_money' : 500000000, 'Skill_Percentage' : 70}
		elif character == '3':
			User = {'이름' : '\'고 니\'' , 'Start_money' : 300000000, 'Skill_Percentage' : 40,'standard_pandon' : 30000000}
			AI1 = {'이름' : 'Computer1', 'Start_money' : 1000000000, 'Skill_Percentage' : 80}
			AI2 = {'이름' : 'Computer2', 'Start_money' : 1000000000, 'Skill_Percentage' : 80}
		global ski1
		ski1 = input("첫번째 스킬을 선택해주세요. 1.밑장빼기 2.바꿔치기 3.뻥카 4.훔쳐보기 ")
		while not (ski1 == '1' or ski1 == '2' or ski1 == '3' or ski1 == '4'):
			ski1 = input("1~4의 숫자로 선택해주세요. 1.밑장빼기 2.바꿔치기 3.뻥카 4.훔쳐보기 ")
		global ski2
		ski2 = input("두번째 스킬을 선택해주세요. ")
		while not (ski2 == '1' or ski2 == '2' or ski2 == '3' or ski2 == '4') or ski2 == ski1:
			if not (ski2 == '1' or ski2 == '2' or ski2 == '3' or ski2 == '4'):
				ski2 = input("스킬목록에서 선택해주세요. 1.밑장빼기 2.바꿔치기 3.뻥카 4.훔쳐보기 ")
			elif ski2 == ski1:
				ski2 = input("이미 첫번째 스킬로 선택하셨습니다. 다른 스킬을 선택해주세요. ")
		standard_pandon = User['standard_pandon']
		skill_confirm(wins)
	except KeyboardInterrupt:
		print("G  O  O  D  B  Y  E  !")	
def fresh_deck():
	deck = []
	for i in range(10):
		deck.append(i+1)
		deck.append(-(i+1))
	random.shuffle(deck)
	return deck
def hit(deck):
    if deck == []:
        fresh_deck()
    return  (deck[0],deck[1:])

def jokbo(cards):
	gg = 0
	if 3 in cards and -7 in cards:
		rank = -1
		name = '망통'
	elif -3 in cards and (7 in cards or -7 in cards):
		rank = -1
		name = '망통'
	elif (	2 in cards or -2 in cards) and (8 in cards or -8 in cards):
		rank = -1
		name = '망통'
	elif abs(cards[0]) + abs(cards[1]) == 9 or abs(cards[0]) + abs(cards[1]) == 19:
		rank = 1
		name = '갑오'
		if 1 in cards and 8 in cards:
			rank = 9
			name = '18광땡'
	elif (4 in cards or -4 in cards) and (6 in cards or -6 in cards):
		rank = 2
		name = '세륙'
	elif (4 in cards or -4 in cards) and (10 in cards or -10 in cards):
		rank = 3
		name = '장사'
	elif (1 in cards or -1 in cards) and (10 in cards or -10 in cards):
		rank = 4
		name = '장삥'
	elif (1 in cards or -1 in cards) and (9 in cards or -9 in cards):
		rank = 5
		name = '구삥'
	elif (1 in cards or -1 in cards) and (4 in cards or -4 in cards):
		rank = 6
		name = '독사'
	elif (1 in cards or -1 in cards) and (2 in cards or -2 in cards):
		rank = 7
		name = '알리'
	elif abs(cards[0]) == abs(cards[1]):
		rank = 8
		name = str(abs(cards[0])) + '땡'
	elif 1 in cards and 3 in cards:
		rank = 8.5
		name = '13광땡'
	elif 3 in cards and 8 in cards:
		rank = 10
		name = '38광땡'
	elif 3 in cards and 7 in cards:
		rank = 0
		name = '땡잡이'
	elif (4 in cards or -4 in cards) and (9 in cards or -9 in cards):
		if 4 in cards and 9 in cards:
			rank = 0
			name = '멍구사'
		else:
			rank = 0
			name = '구사'
	elif 4 in cards and 7:
		rank = 0
		name = '암행어사'
	else:
		rank = 0
		gg = abs(cards[0]) + abs(cards[1])
		if gg > 10: gg -= 10
		name = str(gg) + '끗'
	return rank , name , gg

def player_menu():
	try:
		global name1, name2
		select='0'
		while True:
			time.sleep(1)
			print("================================================")
			print("1.베    팅        2.체    크           3.다    이")
			print("4."+name1+"                            5."+name2)
			print("================================================")
			print(User['이름']+" 보 유 금 액  :", player_money)
			print("\'아 귀\'' 보 유 금 액  :", computer1_money)
			print("\'정마담\'' 보 유 금 액  :", computer2_money)
			print("================================================")
			select=input("선택 : ")
			if select=='1' or select=='2' or select=='3' or select=='4' or select=='5':
				break
		return select
	except KeyboardInterrupt:
		print("종료합니다.")

def player_betting(player_money):
	try:
		while True:
			player_betting_money=input("얼마를 베팅하시겠습니까? : ")
			if(int(player_betting_money) > player_money):
				print("가진 돈보다 많이 입력할 수 없습니다.")
			elif(int(player_betting_money) < 0):
				print("음수는 입력할 수 없습니다.")
			elif((int(player_betting_money)) < User['standard_pandon']):
				print("기본판돈보다 적게 입력할 수 없습니다. ※기본판돈 :",User['standard_pandon'])
			elif((int(player_betting_money)+You['betting_money']) < betting_stack):
				print((betting_stack-You['betting_money']),"보다 적게 입력할 수 없습니다.")
			else:
				return player_betting_money
	except:
		print("금액을 제대로 입력해주세요")
		player_betting(player_money)

def computer_betting(who):
	if who['rank'] == -1:
		return 0
	elif who['rank'] == 0:
		return User['standard_pandon']
	elif who['rank'] <= 3:
		return User['standard_pandon']+10000000
	elif who['rank'] <= 6:
		return User['standard_pandon']+20000000
	else:
		return User['standard_pandon']+30000000

def WinorLose(wins):
	global player_money, computer1_money, computer2_money
	if You['die'] == True:
		You['rank'] = -2
	if Com1['die'] == True:
		Com1['rank'] = -2
	if Com2['die'] == True:
		Com2['rank'] = -2
	time.sleep(1)
	print(User['이름']+'의 족보는 :',You['what_jokbo'])
	print('\'아 귀\'의 족보는 :',Com1['what_jokbo'])
	print('\'정마담\'의 족보는 :',Com2['what_jokbo'])
	if (You['rank'] > Com1['rank']) and (You['rank'] > Com2['rank']):
		if (8.5 <= You['rank'] <= 10) and (Com1['what_jokbo'] == '암행어사' and Com1['rank'] != -2):
			print("\'아 귀\'의 암행어사!")
			wins = winner(Com1,wins)
		elif (8.5 <= You['rank'] <= 10) and (Com2['what_jokbo'] == '암행어사' and Com2['rank'] != -2):
			print("\'정마담\'의 암행어사!")
			wins = winner(Com2,wins)
		elif You['rank'] == 8 and (Com1['what_jokbo'] == '땡잡이' and Com1['rank'] != -2):
			print("\'아 귀\'의 땡잡이!")
			wins = winner(Com1,wins)
		elif You['rank'] == 8 and (Com2['what_jokbo'] == '땡잡이' and Com2['rank'] != -2):
			print("\'정마담\'의 땡잡이!")
			wins = winner(Com2,wins)
		elif You['rank'] <= 8 and (Com1['what_jokbo'] == '멍구사' and Com1['rank'] != -2):
			print("\'아 귀\'의 멍구사로 게임을 재시작합니다.")
			player_money += You['betting_money']
			computer1_money += Com1['betting_money']
			computer2_money += Com2['betting_money']
		elif You['rank'] <= 8 and (Com2['what_jokbo'] == '멍구사' and Com2['rank'] != -2):
			print("\'정마담\'의 멍구사로 게임을 재시작합니다.")
			player_money += You['betting_money']
			computer1_money += Com1['betting_money']
			computer2_money += Com2['betting_money']
		elif You['rank'] <= 7 and (Com1['what_jokbo'] == '구사' and Com1['rank'] != -2):
			print("\'아 귀\'의 구사로 게임을 재시작합니다.")
			player_money += You['betting_money']
			computer1_money += Com1['betting_money']
			computer2_money += Com2['betting_money']
		elif You['rank'] <= 7 and (Com2['what_jokbo'] == '구사' and Com2['rank'] != -2):
			print("\'정마담\'의 구사로 게임을 재시작합니다.")
			player_money += You['betting_money']
			computer1_money += Com1['betting_money']
			computer2_money += Com2['betting_money']
		else:
			wins = winner(You,wins)
	elif (Com1['rank'] > You['rank']) and (Com1['rank'] > Com2['rank']):
		if (8.5 <= Com1['rank'] <= 10) and (You['what_jokbo'] == '암행어사' and You['rank'] != -2):
			print(User['이름']+"의 암행어사!")
			wins = winner(You,wins)
		elif (8.5 <= Com1['rank'] <= 10) and (Com2['what_jokbo'] == '암행어사' and Com2['rank'] != -2):
			print("\'정마담\'의 암행어사!")
			wins = winner(Com2,wins)
		elif Com1['rank'] == 8 and (You['what_jokbo'] == '땡잡이' and You['rank'] != -2):
			print(User['이름']+"의 땡잡이!")
			wins = winner(You,wins)
		elif Com1['rank'] == 8 and (Com2['what_jokbo'] == '땡잡이' and Com2['rank'] != -2):
			print("\'정마담\'의 땡잡이!")
			wins = winner(Com2,wins)
		elif Com1['rank'] <= 8 and (You['what_jokbo'] == '멍구사'and You['rank'] != -2):
			print(User['이름']+"의 멍구사로 게임을 재시작합니다.")
			player_money += You['betting_money']
			computer1_money += Com1['betting_money']
			computer2_money += Com2['betting_money']
		elif Com1['rank'] <= 8 and (Com2['what_jokbo'] == '멍구사' and Com2['rank'] != -2):
			print("\'정마담\'의 멍구사로 게임을 재시작합니다.")
			player_money += You['betting_money']
			computer1_money += Com1['betting_money']
			computer2_money += Com2['betting_money']
		elif Com1['rank'] <= 7 and (You['what_jokbo'] == '구사' and You['rank'] != -2):
			print(User['이름']+"의 구사로 게임을 재시작합니다.")
			player_money += You['betting_money']
			computer1_money += Com1['betting_money']
			computer2_money += Com2['betting_money']
		elif Com1['rank'] <= 7 and (Com2['what_jokbo'] == '구사' and Com2['rank'] != -2):
			print("\'정마담\'의 구사로 게임을 재시작합니다.")
			player_money += You['betting_money']
			computer1_money += Com1['betting_money']
			computer2_money += Com2['betting_money']
		else:
			wins = winner(Com1,wins)
	elif (Com2['rank'] > Com1['rank']) and (Com2['rank'] > You['rank']):
		if (8.5 <= Com2['rank'] <= 10) and (You['what_jokbo'] == '암행어사' and You['rank'] != -2):
			print(User['이름']+"의 암행어사!")
			wins = winner(You,wins)
		elif (8.5 <= Com2['rank'] <= 10) and (Com1['what_jokbo'] == '암행어사' and Com1['rank'] != -2):
			print("\'아 귀\'의 암행어사!")
			wins = winner(Com1,wins)
		elif Com2['rank'] == 8 and (You['what_jokbo'] == '땡잡이' and You['rank'] != -2):
			print(User['이름']+"의 땡잡이!")
			wins = winner(You,wins)
		elif Com2['rank'] == 8 and (Com1['what_jokbo'] == '땡잡이' and Com1['rank'] != -2):
			print("\'아 귀\'의 땡잡이!")
			wins = winner(Com1,wins)
		elif Com2['rank'] <= 8 and (You['what_jokbo'] == '멍구사' and You['rank'] != -2):
			print(User['이름']+"의 멍구사로 게임을 재시작합니다.")
			player_money += You['betting_money']
			computer1_money += Com1['betting_money']
			computer2_money += Com2['betting_money']
		elif Com2['rank'] <= 8 and (Com1['what_jokbo'] == '멍구사' and Com1['rank'] != -2):
			print("\'아 귀\'의 멍구사로 게임을 재시작합니다.")
			player_money += You['betting_money']
			computer1_money += Com1['betting_money']
			computer2_money += Com2['betting_money']
		elif Com2['rank'] <= 7 and (You['what_jokbo'] == '구사' and You['rank'] != -2):
			print(User['이름']+"의 구사로 게임을 재시작합니다.")
			player_money += You['betting_money']
			computer1_money += Com1['betting_money']
			computer2_money += Com2['betting_money']
		elif Com2['rank'] <= 7 and (Com1['what_jokbo'] == '구사' and Com1['rank'] != -2):
			print("\'아 귀\'의 구사로 게임을 재시작합니다.")
			player_money += You['betting_money']
			computer1_money += Com1['betting_money']
			computer2_money += Com2['betting_money']
		else:
			wins = winner(Com2,wins)
	elif You['rank'] == Com1['rank']:
		if You['score'] > Com1['score']:
			wins = winner(You,wins)
		elif You['score'] == Com1['score']:
			print("무승부입니다. 게임을 재시작합니다.")
		elif You['score'] < Com1['score']:
			wins = winner(Com1,wins)
	elif You['rank'] == Com2['rank']:
		if You['score'] > Com2['score']:
			wins = winner(You,wins)
		elif You['score'] == Com2['score']:
			print("무승부입니다. 게임을 재시작합니다.")
		elif You['score'] < Com2['score']:
			wins = winner(Com2,wins)
	elif Com2['rank'] == Com1['rank']:
		if Com2['score'] > Com1['score']:
			wins = winner(Com2,wins)
		elif Com1['score'] == Com2['score']:
			print("무승부입니다. 게임을 재시작합니다.")
		elif Com2['score'] < Com1['score']:
			wins = winner(Com1,wins)
	return wins

def player_turn(wins):
	global player_money , betting_stack , Current_money , standard_pandon , skill_chance
	if player_money == 0:
		return wins
	if Com1['die'] == True and Com2['die'] == True:
		print("\'아귀\'와 \'정마담\'은 모두 다이를 선언했습니다")
		wins = winner(You,wins)
	elif You['die'] == False and player_money > 0:
		print(User['이름']+"의 차례입니다.")
		select = player_menu()
		if select == '1': #베팅
			if player_money < User['standard_pandon']:
				print("가진 돈보다 기본 판돈이 높으므로 파산합니다.")
				return wins
			else:
				player_betting_money = int(player_betting(player_money))
				if betting_stack < (player_betting_money + You['betting_money']):
					betting_stack = (player_betting_money + You['betting_money'])

				player_money -= player_betting_money
				Current_money += player_betting_money
				You['betting_money'] +=player_betting_money
				print(User['이름']+"은 ",player_betting_money,"원을 베팅했습니다.")
				You['end'] = False
				wins = com1_turn(wins)
		elif select =='2': #플레이어메뉴->체크 선택으로 플레이어가 체크인 경우(3명 모두 체크를 원하면 패 오픈)
			if player_money < (betting_stack - You['betting_money']):
				Current_money += player_money
				You['betting_money'] += player_money
				player_money = 0
				You['end'] = True
				print(User['이름']+"은 올인했습니다.")
			else:
				print(User['이름']+"은",betting_stack - Com1['betting_money'],"원을 베팅하고 체크를 선언했습니다.")				
				if You['betting_money'] < betting_stack:
					player_money -= (betting_stack - You['betting_money'])
					Current_money += (betting_stack - You['betting_money'])
					You['betting_money'] = betting_stack
					You['end'] = True
				print(User['이름']+"은 총",You['betting_money'],'만큼의 돈을 걸었습니다.')
			You['end'] = True
			You['die'] = False
			if (You['end'] == True) and (Com1['end'] == True) and (Com2['end'] == True):
				print("패를 오픈합니다.")
				wins = WinorLose(wins)
			else:
				wins = com1_turn(wins)
		elif select =='3':
			print("다이를 선언하셨습니다.")
			You['end'] = True
			You['die'] = True
			if (You['end'] == True) and (Com1['end'] == True) and (Com2['end'] == True):
				print("패를 오픈합니다.")
				wins = WinorLose(wins)
			else:
				wins = com1_turn(wins)
		elif select =='4':
			skill_1()
		elif select =='5':
			skill_2()
	else:
		You['end'] = True
		wins = com1_turn(wins)
	return wins

def com1_turn(wins):
	global computer1_money , betting_stack , Current_money , standard_pandon
	if player_money < 0:
		return wins
	if You['die'] == True and Com2['die'] == True:
		print(User['이름']+"과 \'정마담\'은 다이를 선언했습니다")
		wins = winner(Com1,wins)
	elif Com1['die'] == False and computer1_money > 0:
		check = make_percentage(Com1['check_percentage'])
		Com1['check_percentage'] = 90
		print("\'아귀\'의 차례입니다.")
		time.sleep(1)
		if check == True:
			if computer_betting(Com1) <= betting_stack: #체크
				Com1['end'] = True
				Com1['die'] = False
				if computer1_money < (betting_stack - Com1['betting_money']):
					Current_money += computer1_money
					Com1['betting_money'] += computer1_money
					computer1_money = 0
					print("\'아귀\'가 올인합니다.")
				else:
					print("\'아귀는\'", betting_stack - Com1['betting_money'], "원을 베팅하고 체크를 선언했습니다.")					
					if Com1['betting_money'] < betting_stack:
						computer1_money -= (betting_stack - Com1['betting_money'])
						Current_money += (betting_stack - Com1['betting_money'])
						Com1['betting_money'] = betting_stack
						Com1['end'] = True
				if (You['end'] == True) and (Com1['end'] == True) and (Com2['end'] == True):
					print("패를 오픈합니다.")
					wins = WinorLose(wins)
				else:
					wins = com2_turn(wins)
			else: #베팅
				if (computer1_money < standard_pandon):
					Current_money += computer1_money
					if betting_stack < (computer1_money + Com1['betting_money']):
						betting_stack = (computer1_money + Com1['betting_money'])
					else:
						betting_stack = betting_stack
					Com1['betting_money'] += computer1_money
					computer1_money = 0
					Com1['end'] = True
					print("\'아귀\'가 올인합니다.")
					wins = com2_turn(wins)
				else:
					computer1_betting_money = com1_lowest
					if computer1_betting_money < (betting_stack - Com1['betting_money']):
						computer1_betting_money = (betting_stack - Com1['betting_money'])
					if betting_stack < (computer1_betting_money + Com1['betting_money']):
						betting_stack = (computer1_betting_money + Com1['betting_money'])

					computer1_money -= computer1_betting_money
					Current_money += computer1_betting_money
					Com1['betting_money'] = betting_stack
					print("\'아귀\'가",computer1_betting_money,"만큼 베팅했습니다.")
					Com1['end'] = False
					wins = com2_turn(wins)
		else:
			print("\'아귀\'가 다이를 선언했습니다")
			Com1['end'] = True
			Com1['die'] = True
			if (You['end'] == True) and (Com1['end'] == True) and (Com2['end'] == True):
				print("패를 오픈합니다.")
				wins = WinorLose(wins)
			else:
				wins = com2_turn(wins)
	else:
		Com1['end'] = True
		wins = com2_turn(wins)
	return wins

def com2_turn(wins):
	global computer2_money , betting_stack , Current_money , standard_pandon
	if player_money < 0:
		return wins
	if You['die'] == True and Com1['die'] == True:
		print(User['이름']+"과 \'아귀\'는 모두 다이를 선언했습니다")
		wins = winner(Com2,wins)
	elif Com2['die'] == False and computer2_money > 0:
		check = make_percentage(Com2['check_percentage'])
		Com2['check_percentage'] = 90
		print("\'정마담\'의 차례입니다.")
		time.sleep(1)
		if check == True:
			if computer_betting(Com2) <= betting_stack: #체크
				Com2['end'] = True
				Com2['die'] = False
				if computer2_money < (betting_stack - Com2['betting_money']):
					Current_money += computer2_money
					Com2['betting_money'] += computer2_money
					computer2_money = 0
					print("\'정마담\'이 올인합니다.")
				else:
					print("\'정마담\'은", betting_stack - Com2['betting_money'], "원을 베팅하고 체크를 선언했습니다.")					
					if Com2['betting_money'] < betting_stack:
						computer2_money -= (betting_stack - Com2['betting_money'])
						Current_money += (betting_stack - Com2['betting_money'])
						Com2['betting_money'] = betting_stack
				if (You['end'] == True) and (Com1['end'] == True) and (Com2['end'] == True):
					print("패를 오픈합니다.")
					wins = WinorLose(wins)
				else:
					wins = player_turn(wins)
			else: #베팅
				if (computer2_money < standard_pandon):
					Current_money += computer2_money
					if betting_stack < (computer2_money + Com2['betting_money']):
						betting_stack = (computer2_money + Com2['betting_money'])
					else:
						betting_stack = betting_stack
					Com2['betting_money'] += computer2_money
					computer2_money = 0
					Com2['end'] = True
					print("\'정마담\'이 올인합니다.")
					wins = player_turn(wins)
				else:
					computer2_betting_money = com2_lowest
					if betting_stack < (computer2_betting_money + Com2['betting_money']):
						betting_stack = (computer2_betting_money + Com2['betting_money'])

					computer2_money -= computer2_betting_money
					Current_money += computer2_betting_money
					Com2['betting_money'] = betting_stack
					print("\'정마담\'이",computer2_betting_money,"만큼 베팅했습니다.")
					Com2['end'] = False
					wins = player_turn(wins)
		else:

			print("\'정마담\'이 다이를 선언했습니다")
			Com2['end'] = True
			Com2['die'] = True
			if (You['end'] == True) and (Com1['end'] == True) and (Com2['end'] == True):
				print("패를 오픈합니다.")
				wins = WinorLose(wins)
			else:
				wins = player_turn(wins)
	else:
		Com2['end'] = True
		wins = player_turn(wins)
	return wins

def one_round(wins):
	global player, computer1, computer2, deck , You , Com1, Com2 , betting_stack , Current_money , com1_lowest , com2_lowest , standard_pandon , player_money , computer1_money , computer2_money , skill_chance,User
	standard_pandon = User['standard_pandon']

	print("================================================")
	print("                 섯다 라운드 시작")
	print("================================================")
	print('기본베팅 금액은 ',standard_pandon,'원 입니다.')
	deck = fresh_deck()
	computer1 = []
	computer2 = []
	player = []
	Current_money = 0
	betting_stack = 0
	You = {'이름' : User['이름'], 'betting_money' : 0 , 'rank' : 0 , 'score' : 0 , 'what_jokbo' : 0 , 'end' : False , 'die' : False}
	Com1 = {'이름' : '아귀' , 'betting_money' : 0 , 'rank' : 0 , 'score' : 0 , 'what_jokbo' : 0 , 'check_percentage' : 0 , 'end' : False , 'die' : False}

	Com2 = {'이름' : '정마담' , 'betting_money' : 0 , 'rank' : 0 , 'score' : 0 , 'what_jokbo' : 0 , 'check_percentage' : 0 , 'end' : False , 'die' : False}
	card, deck = hit(deck)
	player.append(card)
	card, deck = hit(deck)
	computer1.append(card)
	card, deck = hit(deck)
	computer2.append(card)
	card, deck = hit(deck)
	player.append(card)
	card, deck = hit(deck)
	computer1.append(card)
	card, deck = hit(deck)
	computer2.append(card)
	You['rank'] , You['what_jokbo'] , You['score'] = jokbo(player)
	Com1['rank'] , Com1['what_jokbo'] , Com1['score'] = jokbo(computer1)
	Com1['check_percentage'] = (round(Com1['rank'] * 5)) + 50
	if Com1['rank'] == -1:
		Com1['check_percentage'] = 0
	com1_lowest = Com1['rank'] * standard_pandon
	Com2['rank'] , Com2['what_jokbo'] , Com2['score'] = jokbo(computer2)
	Com2['check_percentage'] = (round(Com2['rank'] * 5)) + 50
	if Com2['rank'] == -1:
		Com2['check_percentage'] = 0
	com2_lowest = Com2['rank'] * standard_pandon
	print(User['이름']+"의 패는")
	for i in player:
		if i == 1:
			print('1(광)', end = ' ')
		elif i == 3:
			print('3(광)', end = ' ')
		elif i == 4:
			print('4(열끗)', end = ' ')
		elif i == 7:
			print('7(열끗)', end = ' ')
		elif i == 8:
			print('8(광)', end = ' ')
		elif i == 9:
			print('9(열끗)', end = ' ')
		else:
			print(abs(i),"월 끗", end = ' ')
	print('  /  현재'+User['이름']+'의 족보는 : ' , You['what_jokbo'])
	player_money -= User['standard_pandon']
	You['betting_money'] += standard_pandon
	Current_money+=standard_pandon
	if computer1_money < 0:
		pass
	else:
		computer1_money -= User['standard_pandon']
		Com1['betting_money'] += standard_pandon
		Current_money += standard_pandon
	if computer2_money < 0:
		pass
	else:
		computer2_money -= User['standard_pandon']
		Com2['betting_money'] += standard_pandon
		Current_money += standard_pandon
	betting_stack = standard_pandon
	if player_money <= 0:
		print(User['이름'],"이(가) 파산했습니다ㅠㅠㅠㅠㅠㅠ")
	elif (player_money >= computer1_money) and (player_money >= computer2_money):
		wins = player_turn(wins)
	elif (computer1_money > player_money) and (computer1_money >= computer2_money):
		wins = com1_turn(wins)
	elif (computer2_money > player_money) and (computer2_money > computer1_money):
		wins = com2_turn(wins)
	return wins

def sutda(tries,wins):
	global player_money , computer1_money , computer2_money
	player_money = int(User['Start_money'])
	computer1_money = int(AI1['Start_money'])
	computer2_money = int(AI2['Start_money'])
	while (player_money > 0 and computer1_money > 0) or (player_money > 0 and computer2_money > 0):
		wins = one_round(wins)
		tries += 1
	if player_money <= 0:
		print("G A M E   O V E R")
		print("------------------------------------------------")
	if computer1_money <= 0 and computer2_money <= 0:
		print("상대가 모두 파산했습니다.")
		print("당신의 승리입니다!")
		print("------------------------------------------------")
	return	tries,wins

def main():
	try:
		while(True):
			users = load_users()
			print("---------------------Welcome!-------------------")
			print("---------------------M e n u--------------------")
			print("<<       CTRL+C 를 누르면 바로 종료합니다.          >>")
			print("1. 로그인 및 게임시작")
			print("2. 랭킹 보기")
			print("3. 게임설명(게임방식/스킬/난이도)")
			Select=input("Select : ")
			if Select=='1':
				ID,tries,wins,money = login(users)
				choose_character(wins)
				tries,wins = sutda(tries,wins)
				money = round(float(wins) / float(tries) * 100,1)
				users[ID] = (users[ID][0],tries,wins,money)
				store(users)
				break
			elif Select=='2':
				show_top5(users)
			elif Select=='3':
				manual()
			else:
				print("올바르지 않은 입력입니다.")
	except KeyboardInterrupt:
		print("G  O  O  D  B  Y  E  !")

def manual():
	try:
		while(True):
			print("---------------------게임설명---------------------")
			print("1.게임방식")
			print("2.스킬설명")
			print("3.난이도설명")
			print("4.이전 메뉴로")
			Select = input("Select : ")
			if Select=='1':
				print("------------------------------------------------")
				print('※ 게임방식')
				print('- 각 측에 2장씩 총 6장의 패를 나누어 준다.')
				print('- 각자 가진 2장의 패를 조합해서 패의 서열을 화면에 출력한다.')
				print('- 원하는 금액을 베팅한다.')
				print('- 패의 서열이 높은쪽이 그 판에서 승리한다.')
				print('- 승리한 쪽이 판돈을 가져간다')
				print('- 자신을 제외한 상대의 돈이 0이되면 승리한다.')
			elif Select =='2':
				print("------------------------------------------------")
				print('※ 스킬')
				print()
				print('- 밑장빼기')
				print('교체하고 싶은 패를 선택한뒤, 덱에 있는 무작위 카드 한장과 교체합니다.')
				print()
				print('- 바꿔치기')
				print('교체하고 싶은 패와, 그 카드를 교체할 상대를 선택한뒤, 상대의 무작위 패와 선택한 카드를 교체합니다.')
				print()
				print('- 뻥카')
				print('자신의 베팅금액을 2배로 늘려 상대의 다이확률을 높입니다.')
				print()
				print('- 훔쳐보기')
				print('패를 보고싶은 상대를 선택한 뒤, 그 상대의 무작위 패 한장을 훔쳐봅니다.')
				print()
			elif Select =='3':
				print("------------------------------------------------")
				print('※난이도')
				print('-캐릭터에는 각각의 상, 중, 하 난이도가 설정되어 있습니다.')
				print('난이도가 올라갈수록 스킬 성공확률이 적어지고, 기본판돈이 늘어나며, 상대방의 초기자금이 늘어나게 됩니다.')
			elif Select== '4':
				break
			else:
				print("올바르지 않은 입력입니다.")
	except KeyboardInterrupt:
		print("G  O  O  D  B  Y  E  !")
main()
