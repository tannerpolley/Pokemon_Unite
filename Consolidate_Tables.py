import pandas as pd
import numpy as np

df_builds = pd.read_csv('all_builds.csv')
df_winrates = pd.read_csv('all_movesets.csv')

pokemons_1 = df_winrates['Pokemon'].to_list()
skill_sets_1 = df_winrates['Skill Set'].to_list()
win_rates = df_winrates['Win Rate'].to_list()
pick_rates = df_winrates['Pick Rate'].to_list()
roles = df_winrates['Role'].to_list()

pokemons_2 = df_builds['Pokemon'].to_list()
skill_sets_2 = df_builds['Skill Set'].to_list()
paths = df_builds['Path'].to_list()
held_items = df_builds['Held Items'].to_list()
battle_item_sets = df_builds['Battle Items'].to_list()

count = 0
new_df = []
for i in range(len(skill_sets_1)):
    for j in range(len(skill_sets_2)):

        pokemon_1 = pokemons_1[i]
        skill_set_1 = skill_sets_1[i]
        win_rate = win_rates[i]
        pick_rate = pick_rates[i]
        role = roles[i]

        pokemon_2 = pokemons_2[j]
        skill_set_2 = skill_sets_2[j].split(' ')
        path = paths[j]
        held_item_set_1 = held_items[j]
        battle_item_set = battle_item_sets[j]

        if role == 'Attacker' and path == 'Path Damage':
            path = 'Bot Damage'

        if role == 'Attacker' and path == 'Anywhere Damage':
            path = 'Center/Bot Damage'

        if role == 'All-Rounder' and path == 'Anywhere Damage':
            path = 'Center/Top Damage'

        if role == 'All-Rounder' and path == 'Path Damage':
            path = 'Top Damage'

        if (role == 'Speedster' or role == 'Defender') and path == 'Anywhere Damage':
            path = 'Center/Top Damage'

        if role == 'Defender' and path == 'Path Damage':
            path = 'Top Damage'

        if role == 'Supporter' and path == 'Path Damage':
            path = 'Bot Damage'

        if (role == 'Defender' or role == 'Supporter') and path == 'Path Tank':
            path = 'Bot Tank'

        if (role == 'Supporter' or role == 'Defender') and (path == 'Path Support' or path == 'Anywhere Support'):
            path = 'Top Support'

        if '/' in skill_set_2:
            skill_set_2.remove('/')

        k = 0
        matched_names = []

        for name in skill_set_2:
            if name in skill_set_1 and pokemon_1 == pokemon_2:
                matched_names.append(name)
                k += 1
        if skill_set_2 and skill_set_1 == 'All':
            k += 1

        if k > 1 or (pokemon_1 and pokemon_2 == 'Mew' and skill_set_1 and skill_set_2 == 'All'):
            count += 1
            build = {
            'Pokemon':pokemon_2,
            'Role': role,
            'Path': path,
            'Skill Set': skill_set_1,
            'Win Rate': win_rate,
            'Pick Rate': pick_rate,
            'Held Items': held_item_set_1,
            'Battle Items': battle_item_set
            }
            if pokemon_2 == 'Mimikyu':
                print(build)
            new_df.append(build)


#%%

df_total = pd.DataFrame(new_df)


from pandasgui import show

show(df_total)

