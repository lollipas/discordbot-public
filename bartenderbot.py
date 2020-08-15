from discord import *
import json
import random
from datetime import datetime, timedelta 
import pydealer
import asyncio

with open('the_bank.json') as f:
    data = json.load(f)

with open('work.txt', 'r') as f, open('output.txt', 'w') as fo:
    for line in f:
        fo.write(line.replace('"', '').replace("'", ""))

client = Client()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await client.change_presence(activity=Game(name='Comeback 😳'))

@client.event
async def on_message(message):
    
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        
        await message.channel.send('Hello!')
        if message.author.id == 224521739579686912:
            await message.channel.send('<@!224521739579686912>, hecc off fungun!')    
    if message.content.startswith('!membercount'):
                await message.channel.send("5")
    username = message.author.name
    if message.content.startswith('!moneh'):
        #fungun
        moneh_amount = data['users'][username]['moneh']
        await message.channel.send('{} has {} moneh'.format(username, moneh_amount))

    if message.content.startswith('!stonks'):
        embed = Embed(title='Click here to recieve the BIG STONKS!',
                       url='https://www.youtube.com/watch?v=matctZItfJg',
                       description='1000% WORKS')
        await message.channel.send(embed=embed)

    if message.content.startswith('!work'): 
        
        salary = random.randint(1,1000)
        random_work = random.choice(open("output.txt").readlines())
        await message.channel.send('{} {} {} moneh '.format(username,random_work,salary))
  
        data['users'][username]['moneh'] = int(data['users'][username]['moneh']) + salary
        with open('the_bank.json', "w")  as f:
            json.dump(data,f)
       
    
    
    if message.content.startswith('!blackjack'):
        player_list = [username]
        print(player_list)
        gameover = False
        deck = pydealer.Deck()
        deck.shuffle()
        dealer_hand = deck.deal(1)
        player_hand = deck.deal(2)
        vals = message.content.split(" ")
        bet_int = int(vals[1])
        bet = abs(bet_int)
        max_bet = int(data['users'][username]['moneh'])
        bonus = bet * 1.5
        print(bet)
        
        def calculate_value(hand):
            num_aces = 0
            total_value = 0
            

            for card in hand:
                    
                    
                if pydealer.const.DEFAULT_RANKS['values'][card.value] == 13:
                    num_aces += 1
                    total_value += 11
                elif pydealer.const.DEFAULT_RANKS['values'][card.value] >= 10:
                    total_value += 10
                else:
                    total_value += int(card.value)

            while num_aces > 0 and total_value > 21:
                    total_value -= 10
                    num_aces -= 1
            return total_value

        #PLAYER HANDS - IF PLAYER GETS A BLACKJACK
        if calculate_value(player_hand) == 21:
           if calculate_value(dealer_hand) != 21:
                await message.channel.send('{} hit a blackjack and won {} moneh '.format(username,bonus))
                gameover = True
                data['users'][username]['moneh'] = int(data['users'][username]['moneh']) + bonus
                with open('the_bank.json', "w")  as f:
                    json.dump(data,f)
        elif calculate_value(player_hand) and calculate_value(dealer_hand) == 21:
                await message.channel.send('{} hit a blackjack, Bot hit a blackjack. Its a draw '.format(username))
                gameover = True
                
        #PLAYER HANDS - IF PLAYER HAS UNDER 21
        if gameover == False:
            if bet < max_bet:
                await message.channel.send('Your current hand is : \n{}\n and its value is {}'.format(player_hand,calculate_value(player_hand)))
                await message.channel.send('Dealers first card is : \n{}\nand its value is {}'.format(dealer_hand,calculate_value(dealer_hand)))
                await message.channel.send('------------------------------------------------------------------') 
                await message.channel.send('{} do you want to hit or stand? '.format(username))
                while gameover == False:
                    msg = (await client.wait_for("message")).content
                
                    

                    
                    if msg == "hit":
                        if player_list[0] == username:    
                            await message.channel.send('{} hit! '.format(username))
                            player_hand += deck.deal(1)
                            await message.channel.send('You drew \n{}\n and your deck value value is {}'.format(player_hand[-1],calculate_value(player_hand)))
                            
                            print(calculate_value(player_hand))
                            if calculate_value(player_hand) == 21:
                                if calculate_value(dealer_hand) != 21:
                                    await message.channel.send('{} hit a blackjack and won {} moneh '.format(username,bonus))
                                    data['users'][username]['moneh'] = int(data['users'][username]['moneh']) + bonus
                                    with open('the_bank.json', "w")  as f:
                                            json.dump(data,f)
                                            gameover = True
                                    break
                            elif calculate_value(player_hand) and calculate_value(dealer_hand) == 21:
                                    await message.channel.send('{} hit a blackjack, Bot hit a blackjack. Its a draw '.format(username))
                                    gameover = True
                                    break
                            elif calculate_value(player_hand) > 21:
                                    await message.channel.send('{} Bust! and lost {} moneh'.format(username, bet))
                                    data['users'][username]['moneh'] = int(data['users'][username]['moneh']) - bet
                                    with open('the_bank.json', "w")  as f:
                                        json.dump(data,f)
                                    gameover = True
                                    break
                    if msg == "stand":
                            await message.channel.send('{} stands! '.format(username))
                            #CALCULATE DEALER'S HAND VALUE
                            while calculate_value(dealer_hand) <= 17:
                                dealer_hand += deck.deal(1)
                                await message.channel.send('Dealer drew\n{}\nand its deck value is now {}'.format(dealer_hand[-1],calculate_value(dealer_hand)))
                                print(calculate_value(dealer_hand))
                                asyncio.sleep(2)
                                if calculate_value(dealer_hand) > 21:
                                    await message.channel.send('Dealer bust!')
                                    await message.channel.send('{} won {} moneh!'.format(username, bet))
                                    data['users'][username]['moneh'] = int(data['users'][username]['moneh']) + bet
                                    with open('the_bank.json', "w")  as f:
                                        json.dump(data,f)
                                    gameover = True
                                if calculate_value(dealer_hand) == 21:
                                        await message.channel.send('Dealer hit a blackjack!')
                                        await message.channel.send('{} lost {} moneh!'.format(username, bet))
                                        data['users'][username]['moneh'] = int(data['users'][username]['moneh']) - bet
                                        with open('the_bank.json', "w")  as f:
                                            json.dump(data,f)
                                        gameover = True
                                if calculate_value(dealer_hand) > calculate_value(player_hand) and calculate_value(dealer_hand) < 21:
                                    await message.channel.send('Dealer won! It scored {} while {} scored {}'.format(calculate_value(dealer_hand), username, calculate_value(player_hand)))
                                    data['users'][username]['moneh'] = int(data['users'][username]['moneh']) - bet
                                    with open('the_bank.json', "w")  as f:
                                        json.dump(data,f)
                                    gameover = True
                                if calculate_value(dealer_hand) >= 17 and calculate_value(dealer_hand) < calculate_value(player_hand) and calculate_value(dealer_hand) < 21 and calculate_value(player_hand) < 21:
                                        await message.channel.send('{} won! It scored {} while dealer scored {}'.format(username,calculate_value(player_hand),  calculate_value(dealer_hand)))
                                        await message.channel.send('{} won! {} moneh!'.format(username,bet))
                                        data['users'][username]['moneh'] = int(data['users'][username]['moneh']) + bet
                                        with open('the_bank.json', "w")  as f:
                                                json.dump(data,f)
                                        gameover = True
                                if calculate_value(dealer_hand) == calculate_value(player_hand):
                                    await message.channel.send('{} got {}, dealer got {} Its a draw! '.format(username, calculate_value(player_hand), calculate_value(dealer_hand)))
                                    gameover = True
                            
                else: await message.channel.send('{} is playing right now!'.format(username))

    if message.content.startswith('!dice'):
            player_chose_dice = random.randint(0,1)
            dice = random.randint(0,1)
            print(player_chose_dice)
            print(dice)
            vals = message.content.split(" ")
            bet = int(vals[1])
            max_bet = int(data['users'][username]['moneh']) + 1
           
            victory = bet * 2
            if player_chose_dice == dice:
                if bet >= 0:
                    if bet < max_bet:
                        await message.channel.send('{} WON {} moneh!'.format(username, victory))
                        data['users'][username]['moneh'] = int(data['users'][username]['moneh']) + victory
                        with open('the_bank.json', "w")  as f:
                                json.dump(data,f)
                    else: await message.channel.send('{} you dont have enough moneh for that, your max bet is {}!'.format(username, max_bet))
                else: await message.channel.send('{} play nice and enter a valid number!'.format(username))
            elif bet >= 0:
                if bet < max_bet:
                    data['users'][username]['moneh'] = int(data['users'][username]['moneh']) - bet
                    await message.channel.send('{} LOST {} moneh!'.format(username, bet))
                    with open('the_bank.json', "w")  as f:
                            json.dump(data,f)
                else: await message.channel.send('{} you dont have enough moneh for that, your max bet is {}!'.format(username, max_bet))
            else: await message.channel.send('{} you dont have enough moneh for that, your max bet is {}!'.format(username, max_bet))

client.run('your token')
