from bs4 import BeautifulSoup
import os
import json
import pandas as pd
import numpy as np
from Fix_Hoopa_Winrate import fix_hoopa_winrate, fix_comfey_winrate


#%%

# Gather overall Win Rate and Pick Rate data from main meta page

with open('Unite API _ Pokémon Unite Meta Tierlist.html', 'r') as fp:

    soup = BeautifulSoup(fp, "html.parser")

    class_str = "sc-dec2f4e-0 izzWFH"
    pick_rate_block, win_rate_block = soup.find_all('div', class_=class_str)

    class_str = "sc-906f67df-0 epwwQi"
    pick_rate_num = []
    win_rate_num = []
    for pokemon_pick_rate, pokemon_win_rate in zip(pick_rate_block.find_all('div', class_=class_str), win_rate_block.find_all('div', class_=class_str)):
        pick_rate_num.append(float(pokemon_pick_rate.div.text[:-2]))
        win_rate_num.append(float(pokemon_win_rate.div.text[:-2]))

    pick_rate_name = []
    win_rate_name = []
    for pick_mon_name, win_mon_name in zip(pick_rate_block.find_all('img'), win_rate_block.find_all('img')):
        pick_rate_name.append(pick_mon_name['src'][47:-4])
        win_rate_name.append(win_mon_name['src'][47:-4])


    # Change File Names that dont match

pick_rate_name[pick_rate_name.index('Ninetales')] = 'Alolan Ninetales'
pick_rate_name[pick_rate_name.index('MrMime')] = 'Mr. Mime'
pick_rate_name[pick_rate_name.index('Urshifu_Single')] = 'Urshifu'

win_rate_name[win_rate_name.index('Ninetales')] = 'Alolan Ninetales'
win_rate_name[win_rate_name.index('MrMime')] = 'Mr. Mime'
win_rate_name[win_rate_name.index('Urshifu_Single')] = 'Urshifu'

pick_rate_dict = {}
for k, v in zip(pick_rate_name, pick_rate_num):
    pick_rate_dict[k] = v

win_rate_dict = {}
for k, v in zip(win_rate_name, win_rate_num):
    win_rate_dict[k] = v

#%%

with open("roles.json") as f_in:
    role_dict = json.load(f_in)

#%%

path = r'C:\Users\Tanner\Google Drive\Documents\Programming\Python\Python_Scripts\Pokemon_Unite\Pokemon_Sites'

files = os.listdir(path)
print(len(files))

#%%
all_movesets = []

for file in files:
    name = file[35:-5]

    with open(path + '\\' + file, 'r') as fp:

        soup = BeautifulSoup(fp, "html.parser")

        builds = []
        for i, build_block in enumerate(soup.find_all('div', class_='sc-a9315c2e-0 dNgHcB')):
            build_i = {'Pokemon': name, 'Role': role_dict[name]}

            if name == 'Mew' and i == 0:
                build_i = {'Pokemon': name, 'Role': role_dict[name], 'Pick Rate': pick_rate_dict[name],
                           'Win Rate': win_rate_dict[name], 'Skill Set': 'All'}
                all_movesets.append(build_i)
                continue

            if name == 'Mew' and i > 0:
                continue

            for j, column in enumerate(build_block.find_all('div', class_='sc-a9315c2e-2 SBHRg')):
                text = column.find('p', class_='sc-7bda52f2-3 bjWUWj').text
                numb = column.find('p', class_='sc-7bda52f2-4 hVtnmp')

                if numb is not None:
                    numb = numb.text

                if j < 2:
                    if j == 0:
                        numb = str(float(numb[:-2]) * pick_rate_dict[name] / 100) + ' %'

                    build_i[text] = float(numb[:-2])

                elif j == 2:
                    Skill_1 = text

                elif j == 3:
                    Skill_2 = text

            if name != 'Mew':

                build_i['Skill Set'] = Skill_1 + '/' + Skill_2

            all_movesets.append(build_i)

#%%

pd.options.display.float_format = '{:.2f}%'.format
df = pd.DataFrame(all_movesets)

columns_titles = ["Role", "Pokemon", "Win Rate","Pick Rate", "Skill Set"]
df = df.reindex(columns=columns_titles)


# Fix Hoopa Winrates

pokemon = df['Pokemon'].to_list()
indicies = []
for i in range(len(pokemon)):
    if pokemon[i] == 'Hoopa':
        indicies.append(i)

win_rate = win_rate_dict['Hoopa']
pick_rate = pick_rate_dict['Hoopa']

win_rates = []
pick_rates = []
for i in indicies:
    win_rates.append(df.iloc[i, 2])
    pick_rates.append(df.iloc[i, 3]/pick_rate_dict['Hoopa']*100)


win_rates, pick_rates = fix_hoopa_winrate(pick_rates, win_rates, pick_rate, win_rate)
# print(win_rates)
pick_rates = np.round(pick_rates*pick_rate_dict['Hoopa']/100, 4)


skillsets = ['Phantom Force/Hyperspace Hole', 'Shadow Ball/Trick', 'Shadow Ball/Hyperspace Hole', 'Phantom Force/Trick']
for i, j in zip(indicies, range(len(win_rates))):
    df.iloc[i, 2] = win_rates[j]
    df.iloc[i, 3] = pick_rates[j]
    df.iloc[i, 4] = skillsets[j]

# Fix Comfey Winrates

pokemon = df['Skill Set'].to_list()
name = 'Comfey'

indicies = []
for i in range(len(pokemon)):
    if pokemon[i] == 'Floral Healing/Magical Leaf':
        indicies.append(i)
win_rate = win_rate_dict[name]
pick_rate = pick_rate_dict[name]


win_rates = []
pick_rates = []
for i in indicies:
    win_rates.append(df.iloc[i, 2])
    pick_rates.append(df.iloc[i, 3]/pick_rate_dict[name]*100)

pick_rate, win_rate = fix_comfey_winrate(pick_rates, win_rates, pick_rate, win_rate)
pick_rate = np.round(pick_rate*pick_rate_dict[name]/100, 4)

df.iloc[indicies[0], 2] = win_rate
df.iloc[indicies[0], 3] = pick_rate
df.drop(index=indicies[1], inplace=True)

#
pokemon = df['Skill Set'].to_list()
indicies = []
for i in range(len(pokemon)):
    if pokemon[i] == 'Dual Wingbeat/Double Hit':
        indicies.append(i)

df.iloc[indicies[0], 0] = 'Speedster'
df.iloc[indicies[0], 1] = 'Scyther'

#
pokemon = df['Skill Set'].to_list()
indicies = []
for i in range(len(pokemon)):
    if pokemon[i] == 'Surging Strikes/Liquidation':
        indicies.append(i)

df.iloc[indicies[0], 4] = 'Rapid Strike Style'

indicies = []
for i in range(len(pokemon)):
    if pokemon[i] == 'Wicked Blow/Throat Chop':
        indicies.append(i)

df.iloc[indicies[0], 4] = 'Single Strike Style'


#%%
df['Pick Rate'] = df['Pick Rate'].round(2)
df['Win Rate'] = df['Win Rate'].round(2)
df = df[df['Pick Rate'] >= .75]
df.to_csv('all_movesets.csv', index=False)


