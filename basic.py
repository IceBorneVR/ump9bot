#-*- coding: utf-8 -*-

import discord
import requests
import json
from bs4 import BeautifulSoup
from discord.ext import commands

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print('bot on')

@bot.command()
async def 전적(arg1, arg2, arg3): # arg1 = Nickname, arg2 = krjp/as/kakao... , arg3 = solo/duo/squad
        pubg_stats = {
            'rating':0, 'matches_cnt':0, 'win_matches_cnt':0,
            'topten_matches_cnt':0, 'kills_sum':0, 'kills_max':0,
            'assists_sum':0, 'headshot_kills_sum':0, 'deaths_sum':0,
            'longest_kill_max':0, 'rank_avg':0, 'damage_dealt_avg':0,
            'time_survived_avg':0
        }
        pubg_rank = {
            'your_rank':0,
            'all_player':0
        }
        pubg_text = {
            'rank':'', 'rating':'', 'win_rating':'',
            'top_ten':'', 'kd':'', 'avgdmg':'',
            'head_rate':''
        }
        pubg_to_text = {
            'solo':'1', 'duo':'2', 'squad':'4'
        }
        # argument process
        pubg_id = arg1
        pubg_server = arg2.lower()
        pubg_queue = pubg_to_text[arg3.lower()]
        pubg_link = "https://pubg.op.gg/user/{}?server={}".format(pubg_id,pubg_server)
        
        soup = BeautifulSoup(requests.get(pubg_link).text,"html.parser")
        pubg_hash = soup.find("div", attrs={"data-user_id": True}) # check attribute

        if pubg_hash:
            pubg_hash = pubg_hash.attrs['data-user_id'] # Get user hash
            pubg_web_data = BeautifulSoup(requests.get("https://pubg.op.gg/api/users/{}/ranked-stats?season=2018-02&server={}&queue_size={}&mode=tpp".format(
                pubg_hash,pubg_server,pubg_queue)).text,"html.parser")
            json_data = json.loads(pubg_web_data.text)

            if not('message' in json_data):
                json_stats = json_data["stats"]
                pubg_rank['your_rank'] = json_data["ranks"]["rating"]
                pubg_rank['all_player'] = json_data["max_ranks"]["rating"]
                
                for i in pubg_stats.keys():
                    pubg_stats[i] = int(json_stats[i])

                pubg_text['rank'] = '#' + str(pubg_rank['your_rank']) + ' (Top ' + str(round(pubg_rank['your_rank']/pubg_rank['all_player']*100, 2)) + '%)'
                pubg_text['rating'] = str(pubg_stats['rating'])
                pubg_text['win_rating'] = str(round(pubg_stats['win_matches_cnt']/pubg_stats['matches_cnt']*100,2)) + '%'
                pubg_text['top_ten'] = str(round(pubg_stats['topten_matches_cnt']/pubg_stats['matches_cnt']*100,2)) + '%'
                pubg_text['kd'] = str(round(pubg_stats['kills_sum']/pubg_stats['deaths_sum'],2))
                pubg_text['avgdmg'] = str(pubg_stats['damage_dealt_avg'])
                pubg_text['head_rate'] = str(round(pubg_stats['headshot_kills_sum']/pubg_stats['kills_sum']*100,2)) + '%'
                
                embed=discord.Embed(title='Go to pubg.op.gg', url=pubg_link, color=0xff7578)
                embed.set_author(name=(pubg_id + '#' + arg3), icon_url="https://cdn.discordapp.com/avatars/255309888702382080/c5496c61c8cfb225de2476f91655a968.webp?size=1024")
                embed.add_field(name=u'랭킹', value=pubg_text['rank'], inline=False)
                embed.add_field(name=u'점수', value=pubg_text['rating'], inline=True)
                embed.add_field(name=u'승리 비율', value=pubg_text['win_rating'], inline=True)
                embed.add_field(name=u'탑10 비율', value=pubg_text['top_ten'], inline=True)
                embed.add_field(name=u'Kill/Death', value=pubg_text['kd'], inline=True)
                embed.add_field(name=u'데미지 평균', value=pubg_text['avgdmg'], inline=True)
                embed.add_field(name=u'헤드샷 비율', value=pubg_text['head_rate'], inline=True)
                embed.set_footer(text='By Mojito :)', icon_url="https://cdn.discordapp.com/avatars/255309888702382080/c5496c61c8cfb225de2476f91655a968.webp?size=1024")
                await bot.say(embed=embed)
            else:
                await bot.say(u'전적이 아직 기록되지 않았어!.')
        else:
            await bot.say(u'없는 유저라는데? 다시 확인해봐!')
        
bot.run('NDA5NTQ3ODIwNzY1NDEzMzk2.DVgMug.xs68LVCyMhAHFwPMtMZFhrecMnc')
