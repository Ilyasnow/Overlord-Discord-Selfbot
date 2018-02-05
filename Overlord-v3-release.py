import discord
import os 
from datetime import datetime
from threading import Timer
from threading import Thread
import time
import winsound
import asyncio

TOKEN = "" #insert your discord token here
client = discord.Client()
timers = [] #list of Timers for raid detection
timers_q = [] #list of short Timers for raid detection
joined_users = [] #debug

authorized_servers = ['280418753236172811', 
                      '87583189161226240'] #servers to alert about banned words and user joins
authorized_channels = ['87583189161226240', 
                       '187665178303660032',
                       '280418753236172811'] #channels to alert about oversized images (ponyville, manehattan)
mention_servers = ['280418753236172811', 
                   '87583189161226240'] #servers to alert about mentions of your pseudonyms
friends = ['140166787953197056'] #friends to keep track of when they come online
friends_fix = [] #list of friends that are already online (fix)
banned_words = ['fag', 'nigg', 'milf', 
                'cunt', 'retard', 'autis', 'aryanne']#banned words
pseudonyms = ['snow', 'ilya', 'bulka'] #your pseudonyms that mention you

dir_path = os.path.dirname(os.path.realpath(__file__))
notification_sound = os.path.join(dir_path,'typewriter_click_quiet.wav') #alert sound. File with this name should be present in the same directory as this script (.wav only)

print('Starting...')

@client.event
async def on_ready(): #when bot logs in
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    await client.change_presence(status=discord.Status.invisible)
    print('Set status as invisible')
    global loop_timer
    if not loop_timer.is_alive():
        loop_f()

def empty_f(): #function to time the 10 minutes cooldown for joined people
    global timers
    if len(timers_q) > 1 or len(timers) > 2:
        print('User {0} can now talk.'.format(joined_users.pop(0)))
    else:
        joined_users.pop(0)
    timers.pop(0)
    #print('User {0} can now talk.'.format(joined_users.pop(0))) #debug
    return;

def empty_f_q(): #function to time 30 seconds cooldown between joined people
    global timers_q
    timers_q.pop(0)
    return;

loop_timer = Timer(0,empty_f)

@client.event
async def on_member_join(member): #when someone joins the authorized server
    if member.server.id in authorized_servers:
        print('({1.hour:02d}:{1.minute:02d}){0.name} joined server {0.server.name}.'.format(member, datetime.now()))
        #if (len(timers) > 0) and not timers[0].is_alive():
        #    timers.pop(0)
        timers.append(Timer(600,empty_f))
        timers_q.append(Timer(30,empty_f_q))
        #global joined_users #debug
        joined_users.append(member.name) #debug
        timers[-1].start()
        timers_q[-1].start()
        if len(timers_q) > 1:
            winsound.PlaySound(notification_sound, winsound.SND_FILENAME | winsound.SND_ASYNC)
            print()
            print('          HIGH PROBABILITY OF RAID!!')
            print()
        else:
            if len(timers) > 2:
                winsound.PlaySound(notification_sound, winsound.SND_FILENAME | winsound.SND_ASYNC)
                print()
                print('          HIGH PROBABILITY OF RAID!!')
                print()
            #cheeky unicorn ^:)
            #print('                  ^^   ')
            #print('     ^^    ^^^     ^^  ')
            #print('     ^^    ^^^      ^^ ')
            #print('   ^^  ^^           ^^ ')
            #print('   ^^  ^^           ^^ ')
            #print('                    ^^ ')
            #print('           ^^^      ^^ ')
            #print('           ^^^     ^^  ')
            #print('                  ^^   ')
            
@client.event
async def on_member_remove(member): #when someone leaves the authorized server
    if member.server.id in authorized_servers:
        print('({1.hour:02d}:{1.minute:02d}){0.name} left server {0.server.name}.'.format(member, datetime.now()))
        if member.server.name in joined_users:
            joined_users.pop(0)

@client.event
async def on_message(message): #when you recieve a message.
    if message.server is not None: #not DM
        if message.server.id in authorized_servers:
            for i in banned_words: #banned words
                if i in message.content.lower():
                    winsound.PlaySound(notification_sound, winsound.SND_FILENAME | winsound.SND_ASYNC)
                    if message.author.nick is None:
                        print('({1.hour:02d}:{1.minute:02d}){0.author.name} said banned word in #{0.channel.name} at {0.server.name}.'.format(message, datetime.now()))
                        print('\"{0.author.name}:{0.content}\"'.format(message))
                    else:
                        print('({1.hour:02d}:{1.minute:02d}){0.author.nick}({0.author.name}) said banned word in #{0.channel.name} at {0.server.name}.'.format(message, datetime.now()))
                        print('\"{0.author.nick}:{0.content}\"'.format(message))
                    break
            #if not message.author.bot:
            if message.channel.id in authorized_channels: #oversized images
                if message.attachments is not None:
                    for i in message.attachments:
                        if i is not None:
                            if(i.get('width') is not None) and (i.get('height') > 128):
                                winsound.PlaySound(notification_sound, winsound.SND_FILENAME | winsound.SND_ASYNC)
                                if message.author.nick is None:
                                    print('({3.hour:02d}:{3.minute:02d}){0.author.name} posted a picture({1}x{2}) in #{0.channel.name} at {0.server.name}.'.format(message, i.get('width'),i.get('height'),datetime.now()))
                                else:
                                    print('({3.hour:02d}:{3.minute:02d}){0.author.nick}({0.author.name}) posted a picture({1}x{2}) in #{0.channel.name} at {0.server.name}.'.format(message, i.get('width'),i.get('height'),datetime.now()))
                                break
                if message.embeds is not None:
                    for i in message.embeds:
                        if i is not None:
                            if(i.get('thumbnail').get('width') is not None) and (i.get('thumbnail').get('height') > 128):
                                winsound.PlaySound(notification_sound, winsound.SND_FILENAME | winsound.SND_ASYNC)
                                if message.author.nick is None:
                                    print('({3.hour:02d}:{3.minute:02d}){0.author.name} posted a picture({1}x{2}) in #{0.channel.name} at {0.server.name}.'.format(message, i.get('thumbnail').get('width'),i.get('thumbnail').get('height'),datetime.now()))
                                else:
                                    print('({3.hour:02d}:{3.minute:02d}){0.author.nick}({0.author.name}) posted a picture({1}x{2}) in #{0.channel.name} at {0.server.name}.'.format(message, i.get('thumbnail').get('width'),i.get('thumbnail').get('height'),datetime.now()))
                                break
                if message.author.bot:
                    winsound.PlaySound(notification_sound, winsound.SND_FILENAME | winsound.SND_ASYNC)
                    print('({1.hour:02d}:{1.minute:02d})(Bot){0.author.name} is rampaging in #{0.channel.name} at {0.server.name}.'.format(message, datetime.now()))
            if 'https://discord.gg/' in message.content.lower(): #invite links
                winsound.PlaySound(notification_sound, winsound.SND_FILENAME | winsound.SND_ASYNC)
                if message.author.nick is None:
                    print('({1.hour:02d}:{1.minute:02d}){0.author.name} posted invite link in #{0.channel.name} at {0.server.name}.'.format(message, datetime.now()))
                    print('\"{0.author.name}:{0.content}\"'.format(message))
                else:
                    print('({1.hour:02d}:{1.minute:02d}){0.author.nick}({0.author.name}) posted invite link in #{0.channel.name} at {0.server.name}.'.format(message, datetime.now()))
                    print('\"{0.author.nick}:{0.content}\"'.format(message))
        if message.server.id in mention_servers: #mentions
            for i in pseudonyms:
                if i in message.content.lower():
                    if not message.author.bot:
                        print('Someone mentioned you in #{0.channel.name} at {0.server.name}.'.format(message))
                        winsound.PlaySound(notification_sound, winsound.SND_FILENAME | winsound.SND_ASYNC)
                        try:
                            if message.author.nick is None:
                                print('({1.hour:02d}:{1.minute:02d}){0.author.name}:{0.content}'.format(message, datetime.now()))
                            else:
                                print('({1.hour:02d}:{1.minute:02d}){0.author.nick}:{0.content}'.format(message, datetime.now()))
                            break
                        except AttributeError:
                            print('({1.hour:02d}:{1.minute:02d}){0.author.name}:{0.content}'.format(message, datetime.now()))
                            break
						
@client.event
async def on_member_update(member_before, member_after): #when friend goes online
    if member_before.id in friends:
        if member_before.status is discord.Status.offline:
            if member_after.status is discord.Status.online:
                if member_after.id not in friends_fix:
                    print('({1.hour:02d}:{1.minute:02d}) Friend {0.name} is now online.'.format(member_after, datetime.now()))
                    friends_fix.append(member_after.id)
        if member_before.status is discord.Status.online:
            if member_after.status is discord.Status.offline:
                if member_after.id in friends_fix:
                    friends_fix.remove(member_after.id)

def loop_f(): #one hour markdown
    print('{0.hour:02d}:{0.minute:02d}\t-----------------------------------------------------------------------'.format(datetime.now()))
    global loop_timer
    loop_timer = Timer(3600,loop_f)
    loop_timer.start()

print('Run() begins...')
client.run(TOKEN, bot=False) #this blocks the script until abort is called (Ctrl+C)

print('Exit.')
loop_timer.cancel()
client.close()
