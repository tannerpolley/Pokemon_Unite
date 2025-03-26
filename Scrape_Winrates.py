from bs4 import BeautifulSoup
import os
import json
import pandas as pd
import requests
import numpy as np
import gspread as gc
from Fix_Hoopa_Winrate import fix_hoopa_winrate, fix_comfey_winrate


# Gather overall Win Rate and Pick Rate data from main meta page

with open('Unite API _ Pokémon Unite Meta Tierlist.html', 'r') as fp:
    soup = BeautifulSoup(fp, "html.parser")
    class_str = "sc-eaff77bf-0 fJbBUh"
    column_blocks = soup.find('div', class_=class_str)

    class_str = "sc-17dce764-1 ghZPEN"
    win_rate_block, pick_rate_block, ban_rate_block = column_blocks.find_all('div', class_=class_str)

    class_str = "sc-71f8e1a4-0 iDyfqa"
    pick_rate_num = []
    win_rate_num = []
    ban_rate_num = []
    for pokemon_pick_rate, pokemon_win_rate, pokemon_ban_rate in zip(pick_rate_block.find_all('div', class_=class_str),
                                                                     win_rate_block.find_all('div', class_=class_str),
                                                                     ban_rate_block.find_all('div', class_=class_str)
                                                                     ):
        pick_rate_num.append(float(pokemon_pick_rate.div.text[:-2]))
        win_rate_num.append(float(pokemon_win_rate.div.text[:-2]))
        ban_rate_num.append(float(pokemon_ban_rate.div.text[:-2]))

    pick_rate_name = []
    win_rate_name = []
    ban_rate_name = []
    for pick_mon_name, win_mon_name, ban_mon_name in zip(pick_rate_block.find_all('img'),
                                                         win_rate_block.find_all('img'),
                                                         ban_rate_block.find_all('img')
                                                         ):
        pick_rate_name.append(pick_mon_name['src'][19:-4])
        win_rate_name.append(win_mon_name['src'][19:-4])
        ban_rate_name.append(ban_mon_name['src'][19:-4])


pick_rate_dict = {}
for k, v in zip(pick_rate_name, pick_rate_num):
    pick_rate_dict[k] = v

win_rate_dict = {}
for k, v in zip(win_rate_name, win_rate_num):
    win_rate_dict[k] = v

ban_rate_dict = {}
for k, v in zip(ban_rate_name, ban_rate_num):
    ban_rate_dict[k] = v

combined_dict = {
    'Win Rate': [],
    'Pick Rate': [],
    'Ban Rate': [],
}

names = []
dict_list = [win_rate_dict, pick_rate_dict, ban_rate_dict]
for k, v in win_rate_dict.items():
    for i, k2 in enumerate(combined_dict.keys()):
        combined_dict[k2].append(dict_list[i][k])
    if k == 'Ninetales':
        k3 = 'Alolan Ninetales'
    elif k == 'MrMime':
        k3 = 'Mr. Mime'
    elif k == 'Urshifu_Single':
        k3 = 'Urshifu'
    elif k == 'HoOh':
        k3 = 'Ho-Oh'
    elif k == 'Meowscara':
        k3 = 'Meowscarada'
    elif k == 'Rapidash':
        k3 = 'Galarian Rapidash'
    else:
        k3 = k
    names.append(k3)

df = pd.DataFrame(combined_dict, index=names)

df.to_csv('Unite_Meta.csv')
#
# #%%
#
df = pd.read_csv('Unite_Meta.csv', index_col=0)

win_rate_dict = {}
pick_rate_dict = {}
ban_rate_dict = {}
for i, row in df.iterrows():
    win_rate_dict[i] = row['Win Rate']
    pick_rate_dict[i] = row['Pick Rate']
    ban_rate_dict[i] = row['Ban Rate']

with open("roles.json") as f_in:
    role_dict = json.load(f_in)
    
print(win_rate_dict)
#
# #%%
#
#%%
path = r'C:\Users\Tanner\Documents\git\Pokemon_Unite\Pokemon_Sites'

files = os.listdir(path)

#
# #%%
all_movesets = []

for file in files:
    Pokemon_name = file[35:-5]

    with open(path + '\\' + file, 'r') as fp:

        soup = BeautifulSoup(fp, "html.parser")

        builds = []
        for i, build_block in enumerate(soup.find_all('div', class_='sc-a9315c2e-0 dNgHcB')):
            build_i = {'Name': Pokemon_name, 'Role': role_dict[Pokemon_name]}

            if Pokemon_name == 'Mew' and i == 0:
                move_1_file = 'images/Moves/' + 'Mew' + ' - ' + 'Solar Beam' + '.png'
                move_2_file = 'images/Moves/' + 'Mew' + ' - ' + 'Light Screen' + '.png'
                build_i = {'Name': Pokemon_name, 'Pokemon': 'images/Pokemon/' + Pokemon_name + '.png',
                           'Role': role_dict[Pokemon_name],
                           'Pick Rate': pick_rate_dict[Pokemon_name],
                           'Win Rate': win_rate_dict[Pokemon_name], 'Move Set': 'All',
                           'Move 1': move_1_file, 'Move 2': move_2_file}
                all_movesets.append(build_i)
                continue

            if Pokemon_name == 'Blaziken' and i == 0:
                move_1_file = 'images/Moves/' + 'Blaziken' + ' - ' + 'Overheat' + '.png'
                move_2_file = 'images/Moves/' + 'Blaziken' + ' - ' + 'Blaze Kick' + '.png'
                build_i = {'Name': Pokemon_name, 'Pokemon': 'images/Pokemon/' + Pokemon_name + '.png',
                           'Role': role_dict[Pokemon_name],
                           'Pick Rate': pick_rate_dict[Pokemon_name],
                           'Win Rate': win_rate_dict[Pokemon_name], 'Move Set': 'All',
                           'Move 1': move_1_file, 'Move 2': move_2_file}
                all_movesets.append(build_i)
                continue

            if (Pokemon_name == 'Mew' or Pokemon_name == 'Blaziken') and i > 0:
                continue

            for j, column in enumerate(build_block.find_all('div', class_='sc-a9315c2e-2 SBHRg')):
                text = column.find('p', class_='sc-6d6ea15e-3 hxGuyl').text
                numb = column.find('p', class_='sc-6d6ea15e-4 eZnfiD')

                if numb is not None:
                    numb = numb.text

                if j < 2:
                    if j == 0:
                        numb = str(float(numb[:-2]) * pick_rate_dict[Pokemon_name] / 100) + ' %'

                    build_i[text] = float(numb[:-2])

                elif j == 2:
                    move_1_name = text
                    if move_1_name == 'Dual Wingbeat':
                        Pokemon_name_2 = 'Scyther'
                        build_i['Role'] = 'Speedster'
                        build_i['Name'] = Pokemon_name_2
                    else:
                        Pokemon_name_2 = Pokemon_name

                    # img_tag = column.find('img', {'src': lambda src: src and '.png' in src})
                    # img_url = img_tag['src']
                    # img_url = 'https://uniteapi.dev' + img_url
                    # img_response = requests.get(img_url)
                    move_1_pic_file = 'images/Moves/' + Pokemon_name_2 + ' - ' + move_1_name + '.png'
                    # with open(move_1_pic_file, 'wb') as f:
                    #     f.write(img_response.content)

                elif j == 3:
                    move_2_name = text
                    if move_1_name == 'Dual Wingbeat':
                        Pokemon_name_2 = 'Scyther'
                        build_i['Role'] = 'Speedster'
                    else:
                        Pokemon_name_2 = Pokemon_name

                    # img_tag = column.find('img', {'src': lambda src: src and '.png' in src})
                    # img_url = img_tag['src']
                    # img_url = 'https://uniteapi.dev' + img_url
                    # img_response = requests.get(img_url)
                    move_2_pic_file = 'images/Moves/' + Pokemon_name_2 + ' - ' + move_2_name + '.png'
                    # with open(move_2_pic_file, 'wb') as f:
                    #     f.write(img_response.content)

            if Pokemon_name != 'Mew' or Pokemon_name != 'Blaziken':
                build_i['Move Set'] = move_1_name + '/' + move_2_name
                build_i['Move 1'] = move_1_pic_file
                build_i['Move 2'] = move_2_pic_file
            if move_1_name == 'Surging Strikes':
                Pokemon_name_2 = 'Urshifu_Rapid'
            elif move_1_name == 'Wicked Blow':
                Pokemon_name_2 = 'Urshifu_Single'
            build_i['Pokemon'] = 'images/Pokemon/' + Pokemon_name_2 + '.png'

            all_movesets.append(build_i)

# #%%
#

pd.options.display.float_format = '{:.2f}%'.format
df = pd.DataFrame(all_movesets)

columns_titles = ["Name", "Pokemon", "Move Set", "Win Rate", "Pick Rate", "Role", "Move 1", "Move 2"]
df = df.reindex(columns=columns_titles)

print(df[df["Name"] == 'Comfey'])

#
# Fix Hoopa Winrates

win_rate = win_rate_dict['Hoopa']
pick_rate = pick_rate_dict['Hoopa']

df_hoopa = df[df['Name'] == 'Hoopa']
df_hoopa_fix = fix_hoopa_winrate(df_hoopa, pick_rate, win_rate, pick_rate_dict)
df = df[df['Name'] != 'Hoopa']
df = pd.concat([df, df_hoopa_fix], ignore_index=True)
df = df.sort_values(by='Name').reset_index(drop=True)

# Fix Comfey Winrates
#
# pokemon = df['Move Set'].to_list()
# name = 'Comfey'
#
# indicies = []
# for i in range(len(pokemon)):
#     if pokemon[i] == 'Floral Healing/Magical Leaf':
#         indicies.append(i)
# win_rate = win_rate_dict[name]
# pick_rate = pick_rate_dict[name]
#
# win_rates = []
# pick_rates = []
# for i in indicies:
#     win_rates.append(df.loc[i, 'Win Rate'])
#     pick_rates.append(df.loc[i, 'Pick Rate'] / pick_rate_dict[name] * 100)
#
# pick_rate, win_rate = fix_comfey_winrate(pick_rates, win_rates, pick_rate, win_rate)
# pick_rate = np.round(pick_rate * pick_rate_dict[name] / 100, 4)
#
# df.loc[indicies[0], 'Win Rate'] = win_rate
# df.loc[indicies[0], 'Pick Rate'] = pick_rate
# df.drop(index=indicies[1], inplace=True)

#%%
df['Pick Rate'] = df['Pick Rate'].round(2)
df['Win Rate'] = df['Win Rate'].round(2)
# df = df[df['Pick Rate'] >= .75]
df.to_csv('all_movesets.csv', index=False)
#
#
# #%%
# import gspread
# gc = gspread.service_account(filename='service_account.json')
#
# sh = gc.open("Unite Skillset Winrates")
# worksheet = sh.get_worksheet(0)
# worksheet.clear()
# worksheet.update([df.columns.values.tolist()] + df.values.tolist(), 'A1')
