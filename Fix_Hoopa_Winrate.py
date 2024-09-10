import numpy as np

def fix_hoopa_winrate(skillsets_pick_rate, skillsets_win_rate, total_pick_rate, total_win_rate):
    total_matches = 174830

    total_hoopa_matches = total_matches*total_pick_rate/100
    total_hoopa_wins = total_hoopa_matches*total_win_rate/100


    PT_pick_rate = 100 - sum(skillsets_pick_rate)
    if PT_pick_rate < 0:
        PT_pick_rate = 0


    skillsets_pick_rate = np.array([skillsets_pick_rate[0],
                                   skillsets_pick_rate[2],
                                   skillsets_pick_rate[3],
                                   PT_pick_rate,
                                   skillsets_pick_rate[1]])

    skillsets_picks_count = skillsets_pick_rate/100*total_hoopa_matches

    skillsets_win_rate = np.array(skillsets_win_rate)/100

    PH_wins = skillsets_win_rate[0]*skillsets_picks_count[0]
    ST_wins = skillsets_win_rate[2]*skillsets_picks_count[1]
    SH_wins = skillsets_win_rate[3]*skillsets_picks_count[2]
    HH_wins = skillsets_win_rate[1]*skillsets_picks_count[4]

    if PT_pick_rate == 0:
        PT_wins = 0
    else:
        PT_wins = total_hoopa_wins - (PH_wins + ST_wins + SH_wins + HH_wins)


    skillsets_wins_count =np.array([PH_wins,
                                   ST_wins ,
                                   SH_wins,
                                   PT_wins])

    total_releveant_picks = np.sum(skillsets_picks_count[:4])

    true_pick_rate = skillsets_picks_count[:4]/total_releveant_picks

    HF_win_share = true_pick_rate*HH_wins

    true_wins = HF_win_share+skillsets_wins_count

    true_picks = total_hoopa_matches*true_pick_rate

    true_win_rate = true_wins/true_picks

    return np.round(np.array(true_win_rate), 4)*100, np.round(np.array(true_pick_rate), 4)*100


def fix_comfey_winrate(skillsets_pick_rate, skillsets_win_rate, total_pick_rate, total_win_rate):
    total_matches = 100000

    total_comfey_matches = total_matches*total_pick_rate/100

    skillsets_win_rate = np.array(skillsets_win_rate)/100
    skillsets_picks_count = np.array(skillsets_pick_rate)/100*total_comfey_matches
    skillsets_wins_count = skillsets_picks_count*skillsets_win_rate

    true_picks = skillsets_picks_count[0] + skillsets_picks_count[1]
    true_wins = skillsets_wins_count[0] + skillsets_wins_count[1]

    true_pick_rate = true_picks/total_comfey_matches
    true_win_rate = true_wins/true_picks

    return true_pick_rate*100, true_win_rate*100
