from bs4 import BeautifulSoup
import os
import pandas as pd

path = r"C:\Users\Tanner\Google Drive\Documents\Programming\Python\Python_Scripts\Pokemon_Unite\Pokemon_Builds"

files = os.listdir(path)
all_builds = []
for file in files:

    name = file[14:-42]

    if name == 'Mr. Mime':

        file = file + '\\' + 'mr.mime' + '.htm'

    else:
        file = file + '\\' + name.lower() + '.htm'

    try:
        with open(path + '\\' + file, 'r') as fp:

            soup = BeautifulSoup(fp, "html.parser")

            for i, build_block in enumerate(soup.find_all('div', class_='build')):
                build_i = {'Pokemon': name}
                # print(build_block.prettify())

                Build_Title = build_block.find('h3', class_='title').text[7:]
                Build_Path = build_block.find('p', class_='lane').text[6:]
                abilities_list = []
                for abilities in build_block.find_all('div', class_='ability'):
                    ability_name = abilities.find('div', class_='info').h2
                    print(ability_name)
                    abilities_list.append(ability_name)

                build_i['Skill Set'] = abilities_list[-2] + '/' + abilities_list[-1]
                build_i['Path'] = Build_Path

                Held_Items = []
                for held_item in build_block.find_all('div', class_='popper items held'):

                    Held_Items.append(held_item.h2.text)

                build_i['Held Items'] = Held_Items

                Battle_Items = []
                for battle_item in build_block.find_all('div', class_='popper items battle'):

                    Battle_Items.append(battle_item.h2.text)

                build_i['Battle_Items'] = Battle_Items


                all_builds.append(build_i)


    except:
        print(f'No Html file found for this pokemon: {name}')

print(all_builds)
df = pd.DataFrame(all_builds)
print(df)
#%%

# df = pd.DataFrame(all_builds)
# df.to_csv('all_builds_1.csv', index=False)






