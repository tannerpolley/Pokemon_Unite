from flask import Flask, render_template, request
import pandas as pd
import ast

app = Flask(__name__)

# Load the exploded CSV once at startup
df = pd.read_csv('all_movesets.csv')

# Read header date\
with open('date.txt', 'r') as f:
    date = f.read().strip()

with open('matches.txt', 'r') as f:
    matches = float(f.read().strip())

# Define which columns are battle-item details vs static
battle_item_cols = ['Battle Item', 'Pick Rate.1', 'Win Rate.1']
static_columns = [c for c in df.columns if c not in battle_item_cols]

# For filtering options
roles = ['Attacker', 'Speedster', 'All-Rounder', 'Supporter', 'Defender']

@app.route('/', methods=['GET'])
def index():
    # --- 1) pull filter & sort params ---
    selected_roles = request.args.getlist('roles')
    name_filter    = request.args.get('name', '').strip()
    pick_min       = request.args.get('pick_rate_min', default=1.0, type=float)
    pick_max       = request.args.get('pick_rate_max', type=float)
    sort_col       = request.args.get('sort_column', default='Win Rate')
    sort_order     = request.args.get('sort_order',  default='desc')

    # --- 2) apply filters ---
    df_filt = df.copy()
    if selected_roles:
        df_filt = df_filt[df_filt['Role'].isin(selected_roles)]
    if name_filter:
        df_filt = df_filt[df_filt['Name'].str.lower() == name_filter.lower()]
    if pick_min is not None:
        df_filt = df_filt[df_filt['Pick Rate'] >= pick_min]
    if pick_max is not None:
        df_filt = df_filt[df_filt['Pick Rate'] <= pick_max]
    if sort_col in static_columns + battle_item_cols:
        asc = (sort_order == 'asc')
        df_filt = df_filt.sort_values(by=sort_col, ascending=asc)

    def ensure_list(cell):
        """
        If `cell` is a Python-list literal string, parse and return as a list.
        Otherwise, wrap the original value in a single-element list.
        """
        if isinstance(cell, str) and cell.strip().startswith('['):
            try:
                parsed = ast.literal_eval(cell)
                if isinstance(parsed, list):
                    return parsed
            except (ValueError, SyntaxError):
                pass
        return [cell]

    df_filt['Move 1'] = df_filt['Move 1'].apply(ensure_list)
    df_filt['Move 2'] = df_filt['Move 2'].apply(ensure_list)

    # --- 3) group into movesets ---
    movesets = []
    # group by both Name and Move Set so each unique build stays separate
    for (name, moveset_name), grp in df_filt.groupby(['Name', 'Move Set'], sort=False):
        static = {col: grp.iloc[0][col] for col in static_columns}
        items = sorted(
            grp[battle_item_cols].to_dict('records'),
            key=lambda r: r['Pick Rate.1'],
            reverse=True
        )
        movesets.append({
            'static': static,
            'items': items
        })



    header_text = f'Data comes from Unite API as of {date} with {matches:.0f} total games analyzed.'

    # Pass movesets + column definitions to template
    return render_template(
        'index.html',
        movesets=movesets,
        static_columns=static_columns,
        battle_item_cols=battle_item_cols,
        roles=roles,
        name=name_filter,
        selected_roles=selected_roles,
        pick_rate_min=pick_min or '',
        pick_rate_max=pick_max or '',
        sort_column=sort_col,
        sort_order=sort_order,
        header_text=header_text
    )

if __name__ == '__main__':
    app.run(debug=True)
