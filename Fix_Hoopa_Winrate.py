import numpy as np
import pandas as pd


def fix_hoopa_winrate(df_hoopa, total_pick_rate, total_win_rate, pick_rate_dict):
    total_matches = 100000
    total_hoopa_matches = total_matches * total_pick_rate / 100
    total_hoopa_wins = total_hoopa_matches * total_win_rate / 100
    pick_rates = df_hoopa['Pick Rate']
    if "Phantom Force/Trick" in list(df_hoopa['Move Set']):
        missing_moveset = "Shadow Ball/Hyperspace Hole"
    if "Shadow Ball/Hyperspace Hole" in list(df_hoopa['Move Set']):
        missing_moveset = "Phantom Force/Trick"

    missing_pick_rate = 100 - sum(pick_rates / (pick_rate_dict['Hoopa'] / 100))
    if missing_pick_rate < 0:
        missing_pick_rate = 0

    hoopa_dic = {'Move Set': [], 'Win Rate': [], 'Pick Rate': [], 'Win Count': [], 'Pick Count': []}
    for i, row in df_hoopa.iterrows():
        hoopa_dic['Win Rate'].append(row['Win Rate'])
        hoopa_dic['Pick Rate'].append(row['Pick Rate'] / (pick_rate_dict['Hoopa'] / 100))
        hoopa_dic['Move Set'].append(row['Move Set'])
    hoopa_dic['Pick Rate'].append(missing_pick_rate)
    hoopa_dic['Move Set'].append(missing_moveset)

    all_moves_pick_rate = np.array(hoopa_dic['Pick Rate'])

    for i in range(len(all_moves_pick_rate)):
        hoopa_dic['Pick Count'].append(all_moves_pick_rate[i]/100*total_hoopa_matches)

    winrates = list(df_hoopa['Win Rate'])
    for i in range(len(winrates)):
        hoopa_dic['Win Count'].append(winrates[i]/100*hoopa_dic['Pick Count'][i])

    if missing_pick_rate == 0:
        hoopa_dic['Win Count'].append(0)
    else:
        hoopa_dic['Win Count'].append(total_hoopa_wins - sum(hoopa_dic['Win Count']))

    hoopa_dic['Win Rate'].append(hoopa_dic['Win Count'][-1]*100 / hoopa_dic['Pick Count'][-1])

    df_hoopa_all = pd.DataFrame(hoopa_dic)

    true_wins_count = 0
    true_picks_count = 0
    true_movesets = []
    for i, row in df_hoopa_all.iterrows():
        moveset = row['Move Set']
        if moveset != 'Hyperspace Fury/Hyperspace Fury':
            true_wins_count += float(row['Win Count'])
            true_picks_count += float(row['Pick Count'])

    true_pick_rate = []
    win_share = []
    true_wins = []
    true_picks = []
    true_win_rate = []
    move_1 = []
    move_2 = []
    move_sets = []
    name = []
    Pokemon = []
    Role = []
    HH_df = df_hoopa_all[df_hoopa_all['Move Set'] == 'Hyperspace Fury/Hyperspace Fury']
    HH_wins = HH_df['Win Count'].to_numpy()[0]

    for i, row in df_hoopa_all.iterrows():
        moveset = row['Move Set']
        if moveset == 'Hyperspace Fury/Hyperspace Fury':
            true_pick_rate.append(0 / true_picks_count)
            win_share.append(0)
            true_wins.append(0)
            true_picks.append(0)
            true_win_rate.append(0)
            move_sets.append(moveset)
            move_1.append(0)
            move_2.append(0)
            name.append('Hoopa')
            Pokemon.append('images/Pokemon/Hoopa.png')
            Role.append('Supporter')

        else:
            true_pick_rate_i = row['Pick Count'] / true_picks_count
            true_pick_rate.append(true_pick_rate_i)
            win_share_i = true_pick_rate_i * HH_wins
            win_share.append(win_share_i)
            true_win_i = win_share_i + float(row['Win Count'])
            true_wins.append(true_win_i)
            true_pick_i = total_hoopa_matches * true_pick_rate_i
            true_picks.append(true_pick_i)
            true_win_rate_i = true_win_i / true_pick_i
            true_win_rate.append(true_win_rate_i)
            move_sets.append(moveset)
            move_1_i, move_2_i = moveset.split('/')
            move_1.append('images/Moves/Hoopa' + ' - ' + move_1_i + '.png')
            move_2.append('images/Moves/Hoopa' + ' - ' + move_2_i + '.png')
            name.append('Hoopa')
            Pokemon.append('images/Pokemon/Hoopa.png')
            Role.append('Supporter')

    new_dic = {"Name": name, "Pokemon": Pokemon, "Move Set": move_sets,
               "Win Rate": np.round(np.array(true_win_rate)*100, 4), "Pick Rate": np.round(np.array(true_pick_rate)*100*(pick_rate_dict['Hoopa'] / 100), 4), "Role": Role,
               "Move 1": move_1, "Move 2": move_2}

    df = pd.DataFrame(new_dic)
    df.drop(df[df['Move Set'] == 'Hyperspace Fury/Hyperspace Fury'].index, inplace=True)

    return df


def fix_comfey_winrate(skillsets_pick_rate, skillsets_win_rate, total_pick_rate, total_win_rate):
    total_matches = 100000
    print(skillsets_pick_rate)
    total_comfey_matches = total_matches * total_pick_rate / 100

    skillsets_win_rate = np.array(skillsets_win_rate) / 100
    skillsets_picks_count = np.array(skillsets_pick_rate) / 100 * total_comfey_matches
    skillsets_wins_count = skillsets_picks_count * skillsets_win_rate

    true_picks = skillsets_picks_count[0] + skillsets_picks_count[1]
    true_wins = skillsets_wins_count[0] + skillsets_wins_count[1]

    true_pick_rate = true_picks / total_comfey_matches
    true_win_rate = true_wins / true_picks

    return true_pick_rate * 100, true_win_rate * 100
