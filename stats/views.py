import re
from string import printable
from tracemalloc import start
import requests
from .cheack_api import API_KEY
from riotwatcher import LolWatcher
from riotwatcher._apis import BaseApi

#django import
from django.http import  HttpResponseNotFound
from django.shortcuts import redirect, render
from .forms import UsernameForm
from pprint import pp, pprint


watcher = LolWatcher(API_KEY)

        
def basic_page(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = UsernameForm(request.POST)
        
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return redirect('detail_page',request.POST['username'],request.POST['region'])

    # if a GET (or any other method) we'll create a blank form
    else:
        form = UsernameForm(initial={'username':'Type your username'})
    return render(request,'stats/start_page.html',{'form':form})


def detail_page(request,user,region):
   
    #summoner
    user_defoult_information =  watcher.summoner.by_name(region,user)
    NAME = user_defoult_information['name']
    SUMMONERLEVEL = user_defoult_information['summonerLevel']
    PROFILEICONID = f"http://ddragon.leagueoflegends.com/cdn/12.3.1/img/profileicon/{user_defoult_information['profileIconId']}.png"
    #bad username
    if user_defoult_information.get('status'):
            return HttpResponseNotFound('<h1>User not found</h1>')
    else:
        #ranked
        user_ranked_information = watcher.league.by_summoner(region, user_defoult_information['id'])[0]
        RANKED_ICON = f"/static/img/rank/Emblem_{user_ranked_information['tier'].title()}.png"
        RANK = user_ranked_information['tier'].title()+' '+user_ranked_information['rank']
        LP = str(user_ranked_information['leaguePoints'])+'LP'
        WINS,LOSSES = user_ranked_information['wins'],user_ranked_information['losses']


        #champion mastery
        champion_mastery_top_10_end_point = watcher.champion_mastery.by_summoner(region,user_defoult_information['id'])[:10]
        champion_mastery_top_10_key_id_value = {champion_mastery_top_10_end_point[i]['championId']:[champion_mastery_top_10_end_point[i]['championLevel'],champion_mastery_top_10_end_point[i]['championPoints']] for i in range(len(champion_mastery_top_10_end_point))}

        versions = watcher.data_dragon.versions_for_region(region.lower())
        champions_version = versions['n']['champion']
        current_champ_list = watcher.data_dragon.champions(champions_version)
        all_champions = {current_champ_list['data'][k]['key']:k  for k in current_champ_list['data'].keys()}#{'id':nameHero}
        FINISH_MASTERY_CHAMPIONS_FOR_USER = {all_champions[str(key)]:value for key,value in champion_mastery_top_10_key_id_value.items()}
        CHAMPION_ICON = [f"http://ddragon.leagueoflegends.com/cdn/12.3.1/img/champion/{k}.png" for k in FINISH_MASTERY_CHAMPIONS_FOR_USER.keys()]
        FINISH_MASTERY_CHAMPIONS_FOR_USER_LVL = [FINISH_MASTERY_CHAMPIONS_FOR_USER[key][0] for key in FINISH_MASTERY_CHAMPIONS_FOR_USER.keys()]
        FINISH_MASTERY_CHAMPIONS_FOR_USER_POINTS = [FINISH_MASTERY_CHAMPIONS_FOR_USER[key][1] for key in FINISH_MASTERY_CHAMPIONS_FOR_USER.keys()]

       


        #info about matches
        data_region_for_matches = {'EUROPE':['EUW1','EUNE','TR','RU'],'AMERICAS ':['NA','BR', 'LAN', 'LAS','OCE'],'ASIA':['KR','JP']}
        new_region = ''.join([key for key,value in data_region_for_matches.items() if region in value])
        ids_matches = watcher.match.matchlist_by_puuid(new_region,user_defoult_information['puuid'])

        global_info_stats_about_all_user_in_match = []
        GLOBAL_INFO_SORTED_1_USER = []   
        for i in range(len(ids_matches)):
            global_info_stats_about_all_user_in_match.extend(watcher.match.by_id(new_region,ids_matches[i])['info']['participants'])
        for i in global_info_stats_about_all_user_in_match:
            if i['puuid'] == user_defoult_information['puuid']:
                GLOBAL_INFO_SORTED_1_USER.append({
                    f"http://ddragon.leagueoflegends.com/cdn/12.3.1/img/champion/{i['championName']}.png":{'kills':i['kills'],'assists':i['assists'],'deaths':i['deaths'],'status':'Victory' if i['win'] else 'Defeat'}
                    })
        print(GLOBAL_INFO_SORTED_1_USER)
    return render(request,'stats/detail_page.html',{'profileIconId':PROFILEICONID,'name':NAME,'summonerLevel':SUMMONERLEVEL,'ranked_icon':RANKED_ICON,'rank':RANK,
                                                    'lp':LP,'wins':WINS,'losses':LOSSES,'finish_mastery_champions_for_user_hero_name':FINISH_MASTERY_CHAMPIONS_FOR_USER.items(),
                                                    'champion_icon':CHAMPION_ICON,'finish_mastery_champions_for_user_lvl':FINISH_MASTERY_CHAMPIONS_FOR_USER_LVL,
                                                    'finish_mastery_champions_for_user_points':FINISH_MASTERY_CHAMPIONS_FOR_USER_POINTS,'global_info_sorted_1_user':GLOBAL_INFO_SORTED_1_USER})