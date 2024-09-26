from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Read the CSV file when the application starts
df = pd.read_csv('all_movesets.csv')
sortable_columns = df.columns.tolist()  # Ensure this is defined at the top

@app.route('/', methods=['GET'])
def index():
    # Get filter parameters from the request
    selected_roles = request.args.getlist('roles')
    win_rate_min = request.args.get('win_rate_min', type=float)
    win_rate_max = request.args.get('win_rate_max', type=float)
    pick_rate_min = request.args.get('pick_rate_min', type=float)
    pick_rate_max = request.args.get('pick_rate_max', type=float)
    sort_column = request.args.get('sort_column', default='Win Rate')
    sort_order = request.args.get('sort_order', 'desc')

    # Start with the full dataframe
    filtered_df = df.copy()

    # Filter by roles if any are selected
    if selected_roles:
        filtered_df = filtered_df[filtered_df['Role'].isin(selected_roles)]

    # Filter by Win Rate
    if win_rate_min is not None:
        filtered_df = filtered_df[filtered_df['Win Rate'] >= win_rate_min]
    if win_rate_max is not None:
        filtered_df = filtered_df[filtered_df['Win Rate'] <= win_rate_max]

    # Filter by Pick Rate
    if pick_rate_min is not None:
        filtered_df = filtered_df[filtered_df['Pick Rate'] >= pick_rate_min]
    if pick_rate_max is not None:
        filtered_df = filtered_df[filtered_df['Pick Rate'] <= pick_rate_max]

    # Sorting
    # Exclude image columns from sorting
    image_columns = ['Pokemon', 'Move 1', 'Move 2']
    sortable_columns = [col for col in df.columns if col not in image_columns]

    if sort_column in sortable_columns:
        filtered_df = filtered_df.sort_values(by=sort_column, ascending=(sort_order == 'desc'))

    # Exclude the index when passing data to the template
    data = filtered_df.to_dict(orient='records')
    columns = filtered_df.columns.tolist()
    roles = ['Attacker', 'Speedster', 'All-Rounder', 'Supporter', 'Defender']

    return render_template(
        'index.html',
        data=data,
        columns=columns,
        roles=roles,
        selected_roles=selected_roles,
        win_rate_min=win_rate_min if win_rate_min is not None else '',
        win_rate_max=win_rate_max if win_rate_max is not None else '',
        pick_rate_min=pick_rate_min if pick_rate_min is not None else '',
        pick_rate_max=pick_rate_max if pick_rate_max is not None else '',
        sort_column=sort_column,
        sort_order=sort_order,
        sortable_columns=sortable_columns
    )

if __name__ == '__main__':
    app.run(debug=True)
