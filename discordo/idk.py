import os
from riotwatcher import LolWatcher
from myapi import api_key
import pandas as pd
class LeagueApi:    
    def __init__(self,name):
        self.api = api_key()
        self.watcher = LolWatcher(self.api)
        self.my_region = 'euw1'
        self.last_version = self.watcher.data_dragon.versions_all()[0]
        self.me = self.watcher.summoner.by_name(self.my_region, name)
    def my_infos(self, user:str):
        with open(os.path.join(os.path.dirname(__file__), f"tmp_{user}.txt"), "w") as f:
            f.write("\n                                                       *My infos* \n\n")
            for key, value in self.me.items():
                f.write(f"**{key}** : {value}\n")
        return self.me

    def current_game(self):
        current_game = self.watcher.spectator.by_summoner(self.my_region, self.me['id'])
        return current_game

    def ranked_stats(self, user:str):
        with open(os.path.join(os.path.dirname(__file__), f"tmp_{user}.txt"), "w") as f:
            f.write("\n\n                                                       Ranked stats\n\n")
            ranked_stats = self.watcher.league.by_summoner(self.my_region, self.me['id'])
            for gamemodes in ranked_stats:
                gamemode = gamemodes['queueType']

                if gamemode == 'RANKED_SOLO_5x5':
                    f.write("\n**STATS EN SOLO-DUO**\n")
                elif gamemode == 'RANKED_FLEX_SR':
                    f.write("\n**STATS EN FLEX**\n")

                for key, value in gamemodes.items():
                    if key == 'queueType':
                        continue
                    else:
                        f.write(f"**{key}** : {value}\n")
        return ranked_stats

    def print_all_champion_infos(self):
        versions = self.watcher.data_dragon.versions_for_region(self.my_region)
        champions_version = versions['n']['champion']

        current_champ_list = self.watcher.data_dragon.champions(champions_version)
        with open(os.path.join(os.path.dirname(__file__), "tmp.txt"), "w") as f:
            for key, value in current_champ_list.items():
                if key == 'data':
                    for champ_key, champ_value in value.items():
                        f.write(f"**{champ_key}**\n")
                        for infos_key, infos_value in champ_value.items():
                                f.write(f"**{infos_key}** : {infos_value}\n")
                        f.write("\n")
                else:
                    f.write(f"{key} : {value}")

    def print_one_champion_infos(self, champ_name, user:str):
        versions = self.watcher.data_dragon.versions_for_region(self.my_region)
        champions_version = versions['n']['champion']

        current_champ_list = self.watcher.data_dragon.champions(champions_version)
        with open(os.path.join(os.path.dirname(__file__), f"tmp_{user}.txt"), "w") as f:
            for key,value in current_champ_list.items():
                if key == 'data':
                    for champ_key, champ_ in value.items():
                        if champ_key == champ_name:
                            f.write(f"*{champ_name}*\n")
                            for infos_key, infos_ in champ_.items():
                                f.write(f"**{infos_key}** : {infos_}\n")
                            f.write("\n")
                else:
                    continue
    

# fancy way of getting the participants names using their IDs
    # lastMatchId = watcher.match.matchlist_by_puuid(my_region, me['puuid'])[match_number]
    # match = watcher.match.by_id(my_region, lastMatchId)
    # for participantId in match['metadata']['participants']:
    #     summoner_name = watcher.summoner.by_puuid(my_region, participantId)['name']
    #     participantsNames.append(summoner_name)

    def get_a_match_stats(self,match_number):

        lastMatchId = self.watcher.match.matchlist_by_puuid(self.my_region, self.me['puuid'])[match_number]
        match = self.watcher.match.by_id(self.my_region, lastMatchId)

        #the following 6 lines are for getting the items names using their IDs and storing em in a dictionnary
        latestItems = self.watcher.data_dragon.versions_for_region(self.my_region)['n']['item']
        static_items_list = self.watcher.data_dragon.items(latestItems)['data']
        items_dict = {}
        for key in static_items_list:
            
            row = static_items_list[key]
            items_dict[int(key)] = row['name']
        
        participants = []
        for i in match["info"]['participants']:
            participant = {}

            #game related
            game = {}
            game["Durée de la partie"] = f"""{i["timePlayed"]//60} minutes {i["timePlayed"]%60} secondes"""
            game["Game Gagnée"] = i["win"]
            game["Fin de la partie (surrender early)"] = i["gameEndedInEarlySurrender"]
            game["Fin de la partie (surrender)"] = i["gameEndedInSurrender"]
            participant["Game Related"] = game

            #team related
            team = {}
            team["ID de l'équipe"] = i["teamId"]
            participant["Team Related"] = team
            
            #summoner related
            summoner = {}
            summoner["Nom du joueur"] = i["summonerName"]
            summoner["ID de l'icône du summoner"] = i["profileIcon"]
            summoner["Niveau du joueur"] = i["summonerLevel"]
            summoner["ID du joueur"] = i["summonerId"]
            summoner["ID du summoner"] = i["summonerId"]
            summoner["Puuid du summoner"] = i["puuid"]
            summoner["Nom de l'ID Riot"] = i["riotIdName"]
            summoner["Tagline du summoner"] = i["riotIdTagline"]
            summoner["Rôle du summoner"] = i["role"]
            summoner["Position"] = i["lane"]
            summoner["Temps total de l'écran gris mdr"] = i["totalTimeSpentDead"]
            participant["Summoner related"] = summoner
            
            #champion related
            champion_related = {}
            champion_related["Nom du champion joué"] = i["championName"]
            champion_related["Nombre de kills"] = i["kills"]
            champion_related["Nombre de morts"] = i["deaths"]
            champion_related["Nombre d'assistances"] = i["assists"]
            if (champion_related["Nombre de kills"] != 0 or champion_related["Nombre d'assistances"] != 0) and champion_related["Nombre de morts"] != 0:
                champion_related["KDA"] = (champion_related["Nombre de kills"] + champion_related["Nombre d'assistances"]) / champion_related["Nombre de morts"]
            elif champion_related["Nombre de morts"] == 0:
                champion_related["KDA"] = (champion_related["Nombre de kills"] + champion_related["Nombre d'assistances"]) / 1
            champion_related["Nombre de double kills"] = i["doubleKills"]
            champion_related["Nombre de triple kills"] = i["tripleKills"]
            champion_related["Nombre de quadra kills"] = i["quadraKills"]
            champion_related["Nombre de pentakills"] = i["pentaKills"]
            champion_related["Plus gros Multi-kill"] = i["largestMultiKill"]
            champion_related["Nombre de 'killing sprees'"] = i["killingSprees"]
            champion_related["Plus gros Killing spree"] = i["largestKillingSpree"]
            champion_related["Nombre de kills non réels?????????"] = i["unrealKills"]
            champion_related["Experience du champion"] = i["champExperience"]
            champion_related["Niveau du champion"] = i["champLevel"]
            champion_related["Bounty level"] = i["bountyLevel"] 
            champion_related["Plus longue durée en vie"] = i["longestTimeSpentLiving"]
            champion_related["Temps passé à CC d'autres joueurs"] = i["timeCCingOthers"]
            champion_related["Durée de CC totale infligés"] = i["totalTimeCCDealt"]
            champion_related["Nombre de minions tués"] = i["totalMinionsKilled"]
            participant["Champion related"] = champion_related
            
            
            #damage and heals related
            damage_and_heals_related = {}
            damage_and_heals_related["Dégats totaux infligés"] = i["totalDamageDealt"]
            damage_and_heals_related["Dégats totaux infligés aux champions"] = i["totalDamageDealtToChampions"]
            damage_and_heals_related["Dégats totaux shieldés aux alliés"] = i["totalDamageShieldedOnTeammates"]
            damage_and_heals_related["Dégats magiques infligés"] = i["magicDamageDealt"]
            damage_and_heals_related["Dégats magiques infligés aux champions"] = i["magicDamageDealtToChampions"]
            damage_and_heals_related["Dégats magiques reçus"] = i["magicDamageTaken"]
            damage_and_heals_related["Dégats infligés à soi-même"] = i["damageSelfMitigated"]
            damage_and_heals_related["True damage infligés"] = i["trueDamageDealt"]
            damage_and_heals_related["True damage infligés aux champions"] = i["trueDamageDealtToChampions"]
            damage_and_heals_related["True damage reçus"] = i["trueDamageTaken"]
            damage_and_heals_related["Dégats physiques infligés"] = i["physicalDamageDealt"]
            damage_and_heals_related["Dégats physiques infligés aux champions"] = i["physicalDamageDealtToChampions"]
            damage_and_heals_related["Dégats physiques reçus"] = i["physicalDamageTaken"]
            damage_and_heals_related["Dégats totaux reçus"] = i["totalDamageTaken"]
            damage_and_heals_related["Heal total reçu"] = i["totalHeal"]
            damage_and_heals_related["Heal total donné aux alliés"] = i["totalHealsOnTeammates"]
            damage_and_heals_related["Nombre d'unités soignées"] = i["totalUnitsHealed"]
            damage_and_heals_related["Coup critique le plus important"] = i["largestCriticalStrike"]
            participant["Damage/Heals related"] = damage_and_heals_related
            
            #summoner spells and chammpion spells related
            summoner_spells_and_champion_spells_related = {}
            summoner_spells_and_champion_spells_related["Nombre de casts du spell 1"] = i["spell1Casts"]
            summoner_spells_and_champion_spells_related["Nombre de casts du spell 2"] = i["spell2Casts"] 
            summoner_spells_and_champion_spells_related["Nombre de casts du spell 3"] = i["spell3Casts"]
            summoner_spells_and_champion_spells_related["Nombre de casts du spell 4"] = i["spell4Casts"]
            summoner_spells_and_champion_spells_related["Nombre de casts du summoner spell 1"] = i["summoner1Casts"]
            summoner_spells_and_champion_spells_related["Summoner spell 1"] = i["summoner1Id"]
            summoner_spells_and_champion_spells_related["Nombre de casts du summoner spell 2"] = i["summoner2Casts"]
            summoner_spells_and_champion_spells_related["Summoner spell 2"] = i["summoner2Id"]
            participant["Summoner spells/Champion spells related"] = summoner_spells_and_champion_spells_related
            
            #gold related
            gold_related = {}
            gold_related["Or gagné"] = i["goldEarned"]
            gold_related["Or dépensé"] = i["goldSpent"]
            participant["Gold related"] = gold_related
            
            #items related
            items_related = {}
            items_related["Item 1"] = items_dict.get(i["item0"])
            items_related["Item 2"] = items_dict.get(i["item1"]) 
            items_related["Item 3"] = items_dict.get(i["item2"])
            items_related["Item 4"] = items_dict.get(i["item3"])
            items_related["Item 5"] = items_dict.get(i["item4"])
            items_related["Item 6"] = items_dict.get(i["item5"])
            items_related["Ward"] = items_dict.get(i["item6"])
            items_related["Nombre d'items achetés"] = i["itemsPurchased"] 
            items_related["Nombre de consommables achetés"] = i["consumablesPurchased"]
            participant["Items related"] = items_related
            
            #objectives related
            objectives_related = {}
            objectives_related["Nombre de participation à un inhibiteur tué"] = i["inhibitorTakedowns"]
            objectives_related["Nombre d'inhibiteurs perdus"] = i["inhibitorsLost"]
            objectives_related["Nombre d'inhibiteurs tués"] = i["inhibitorKills"]
            objectives_related["Nombre de dragon tués"] = i["dragonKills"]
            objectives_related["Nombre de barons tués"] = i["baronKills"]
            objectives_related["Dégats infligés aux bâtiments"] = i["damageDealtToBuildings"]
            objectives_related["Dégats infligés aux objectifs"] = i["damageDealtToObjectives"]
            objectives_related["Dégats infligés aux tours"] = i["damageDealtToTurrets"]
            objectives_related["Nombre d'objectifs volés"] = i["objectivesStolen"]
            objectives_related["Nombre d'assistances pour voler des objectifs"] = i["objectivesStolenAssists"]
            objectives_related["Nombre de tours détruites"] = i["turretKills"]
            objectives_related["Nombre de tours takedowned"] = i["turretTakedowns"]
            objectives_related["Nombre de tours perdues"] = i["turretsLost"]
            participant["Objectives related"] = objectives_related
            
            #vision related
            vision_related = {}
            vision_related["Nombre de red wards utilisées"] = i["detectorWardsPlaced"]
            # vision_related["Nombre de ping basiques"] = i["basicPings"]
            vision_related["Nombre de blue wards achetées"] = i["sightWardsBoughtInGame"]
            vision_related["Score de vision"] = i["visionScore"]
            vision_related["Nombre de vision wards achetées"] = i["visionWardsBoughtInGame"]
            vision_related["Nombre de wards tuées"] = i["wardsKilled"]
            vision_related["Nombre de wards placées"] = i["wardsPlaced"]
            participant["Vision related"] = vision_related
            
            participants.append(participant)
        return participants

    def get_lastMatch_stats(self):
        return self.get_a_match_stats(self,0)

    def print_a_match_stats(self, match_number, cas):
        participants = self.get_a_match_stats(match_number)
        not_useful = []
        if len(cas)<1 and cas[0] != "0":
            not_useful = ["Team Related, Objectives related"]
        else :
            for i in cas:
                match i:
                    case "0":
                        not_useful.clear()
                        break
                    case "1":
                        cas = "Team Related"
                    case "2":
                        cas = "Summoner related"
                    case "3":
                        cas = "Champion related"
                    case "4":
                        cas = "Damage/Heals related"
                    case "5":
                        cas = "Summoner spells/Champion spells related"
                    case "6":
                        cas = "Gold related"
                    case "7":
                        cas = "Items related"
                    case "8":
                        cas = "Objectives related"
                    case "9":
                        cas = "Vision related"
                    case _:
                        break
                not_useful.append(cas)
        GamePrinted = False
        with open(os.path.join(os.path.dirname(__file__), "tmp.txt"), "w") as f:
            for i in participants:
                f.write("---------------------------------------------------")
                for key, value in i.items():
                    if (GamePrinted and key == "Game Related"):
                        continue
                    if key in not_useful: 
                        continue
                    f.write(f"\n*{key}*\n")
                    count = 0
                    for key2, value2  in value.items():
                        str2 = f"**{str(key2)}** : {str(value2)}"
                        f.write(str2)
                        if count == 0:
                            while len(str2) < 50:
                                f.write(" ")
                                str2 += " "
                            if key2 != list(value.keys())[-1]:
                                f.write(" | ")
                            count += 1
                        else:
                            while len(str2) < 50:
                                f.write(" ")
                                str2 += " "
                            f.write("\n")
                            count = 0
                            continue

                        #si key2 est la derniere clé de value
                        if key2 == list(value.keys())[-1]:
                            f.write("\n")
                    if key == "Game Related":
                        f.write("\n---------------------------------------------------")
                        GamePrinted = True     

    def new_print(self,match_number, cas, user:str, file:bool):
        participants = self.get_a_match_stats(match_number)
        not_useful = []
        if len(cas)<1 and cas[0] != "0":
            not_useful = ["Team Related, Objectives related"]
        else :
            for i in cas:
                match i:
                    case "0":
                        not_useful.clear()
                        break
                    case "1":
                        cas = "Team Related"
                    case "2":
                        cas = "Summoner related"
                    case "3":
                        cas = "Champion related"
                    case "4":
                        cas = "Damage/Heals related"
                    case "5":
                        cas = "Summoner spells/Champion spells related"
                    case "6":
                        cas = "Gold related"
                    case "7":
                        cas = "Items related"
                    case "8":
                        cas = "Objectives related"
                    case "9":
                        cas = "Vision related"
                    case _:
                        break
                not_useful.append(cas)
        
        dataFin = []
        columns = [' ', ' ', ' ']
        data_array = []
        GamePrinted = False
        titre = ""
        for i in participants:
            for key, value in i.items():
                if key in not_useful: 
                    continue
                tmp = []
                if key == "Team Related":
                    continue
                tmp.append(' ')
                tmp.append(' ')
                tmp.append(' ')
                data_array.append(tmp)
                tmp = []
                tmp.append(key)
                tmp.append(" ")
                tmp.append(" ")
                data_array.append(tmp)
                tmp = []
                count = 0
                for key2, value2  in value.items():
                    if GamePrinted and key == "Game Related" and key2.startswith("Durée"):
                        continue
                    if key2.startswith("ID") or key2.startswith("Puuid du") or key2.startswith("Tagline") or key2.startswith("Nom de l'ID Riot"):
                        continue
                    if key2.startswith("Nom du j"):
                        if "\u03b5" in value2:
                            value2 = value2.replace("\u03b5","e")
                    if file:
                        tmp.append(f"{str(key2)} : {str(value2)}")
                    else:
                        tmp.append(f"**{str(key2)}** : {str(value2)}")
                    count+=1
                    if count == 3:
                        data_array.append(tmp)
                        tmp = []
                        count = 0
                    elif key2 == "Nom du champion joué":
                        titre = value2
                    elif key2 == list(value.keys())[-1]:
                        if len(tmp) == 1:
                            tmp.append('')
                            tmp.append('')
                        elif len(tmp) == 2:
                            tmp.append('')
                        data_array.append(tmp)
                        tmp = []
                        count = 0
                        continue
                    
                if key == "Game Related":
                    GamePrinted = True
                # if key == list(i.keys())[-1]:
                #     tmp.append(' ')
                #     tmp.append(' ')
                #     tmp.append(' ')
                #     data_array.append(tmp)
            dataFin.append({'title' : titre, 'data' : data_array})
            data_array = []
        
        list_titre = []  
        for array in dataFin:
            df = pd.DataFrame(array['data'], columns=columns)
            df.index = ["|" for _ in range(len(df))]

            title = array['title']
            list_titre.append(title)
            data_array.append(df)
        
        # Do something with the arrays, such as printing them
        with open(os.path.join(os.path.dirname(__file__), f"tmp_{user}.txt"), "w") as f:
            f.write("-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n")
            for i in range(len(list_titre)):
                f.write("                                                                                                         ")
                f.write(list_titre[i])
                print(data_array[i])
                f.write(str(data_array[i]))
                f.write("\n-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n")
        if file:
            with open(os.path.join(os.path.dirname(__file__), f"tmp_{user}.txt"), 'r') as f:
                lines = f.readlines()

            for i in range(len(lines)):
                # lines[i] = lines[i][:len(lines[i])-1] + '|' + lines[i][len(lines[i])-1:]
                if not lines[i].startswith("-"):
                    lines[i] = lines[i][:len(lines[i])-1] + (154-len(lines[i])-1)*"\t" + '|' + lines[i][len(lines[i])-1:]
            with open(os.path.join(os.path.dirname(__file__), f"tmp_{user}.txt"), 'w') as f:
                f.writelines(lines)

            # df = pd.concat(data_array, keys=list_titre, join='outer')
            # f.write(str(df))

        # df = pd.concat(data_array, keys=list_titre)
        # df.to_csv(os.path.join(os.path.dirname(__file__), "data.csv"))

    def compare_with_opponent(self):
        participants = self.get_lastMatch_stats()
        # à savoir : les 2 top laners sont en premier dans l'ordre de sauvegarde des equipes dans le dictionnaire, et ainsi de suite
        # donc 1er top = participants[0] et 2eme top = participants[5] (cpas ca mais t'as capté genre 0 et 5)
        lane = input("Quels joueurs voulez-vous comparer ? (top, jungle, mid, bot, supp) \n")
        match lane:
            case "top":
                participant1 = participants[0]
                participant2 = participants[5]
            case "jungle":
                participant1 = participants[1]
                participant2 = participants[6]
            case "mid":
                participant1 = participants[2]
                participant2 = participants[7]
            case "bot":
                participant1 = participants[3]
                participant2 = participants[8]
            case "supp":
                participant1 = participants[4]
                participant2 = participants[9]
            case _:
                print("Veuillez entrer un des ces choix : top, jungle, mid, bot, supp")
        stats_to_comp = []
        print("""Quelles stats voulez-vous comparer :
                            1 : Team related
                            2 : Summoner related
                            3 : Champion related
                            4 : Damage/Heals related
                            5 : Summoner spells/Champion spells related
                            6 : Gold related
                            7 : Items related
                            8 : Objectives related
                            9 : Vision related\n""")
        cas = input()
        cas = cas.split()
        for i in cas:
            match i:
                case "0":
                    stats_to_comp.clear()
                    break
                case "1":
                    cas = "Team Related"
                case "2":
                    cas = "Summoner related"
                case "3":
                    cas = "Champion related"
                case "4":
                    cas = "Damage/Heals related"
                case "5":
                    cas = "Summoner spells/Champion spells related"
                case "6":
                    cas = "Gold related"
                case "7":
                    cas = "Items related"
                case "8":
                    cas = "Objectives related"
                case "9":
                    cas = "Vision related"
                case _:
                    break
            stats_to_comp.append(cas)
        for key1, value1 in participant1.items():
            for key2, value2 in participant2.items():
                if key1 == key2 and key1 in stats_to_comp:
                    # print(f"{key1} : {key2}")
                    for key3, value3 in value1.items():
                        for key4, value4 in value2.items():
                            if key3 == key4:
                                print(f"{key3} : {value3}", end = " "*(55-(len(" : ")+len(key3)) + len(str(value3))))
                                print(f"{value4}")
# instance = LeagueApi("itsloimax")
# instance.new_print(1, ["0"], "loimax#7350", True)
# print(instance.current_game())
