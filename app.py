from flask import Flask, render_template, request
import pandas as pd
from Scrape_Winrates import date

app = Flask(__name__)

# Read the CSV file when the application starts
df = pd.read_csv('all_movesets.csv')
sortable_columns = df.columns.tolist()  # Ensure this is defined at the top

with open("date.txt", "r") as f:
    date = f.read()


@app.route('/', methods=['GET'])
def index():
    # Get filter parameters from the request
    selected_roles = request.args.getlist('roles')
    name_filter = request.args.get('name', '')
    pick_rate_min = request.args.get('pick_rate_min', type=float)
    pick_rate_max = request.args.get('pick_rate_max', type=float)
    sort_column = request.args.get('sort_column', default='Win Rate')
    sort_order = request.args.get('sort_order', 'desc')

    # Start with the full dataframe
    filtered_df = df.copy()

    # Filter by roles if any are selected
    if selected_roles:
        filtered_df = filtered_df[filtered_df['Role'].isin(selected_roles)]

    # Filter data based on Name filter
    if name_filter:
        filtered_df = filtered_df[filtered_df['Name'].str.lower() == name_filter.lower()]  # Filter case-insensitive

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
        filtered_df = filtered_df.sort_values(by=sort_column, ascending=(sort_order == 'asc'))

    # Exclude the index when passing data to the template
    data = filtered_df.to_dict(orient='records')
    columns = filtered_df.columns.tolist()
    roles = ['Attacker', 'Speedster', 'All-Rounder', 'Supporter', 'Defender']

    header_text = f'Data comes from Unite API as of {date}'

    return render_template(
        'index.html',
        data=data,
        columns=columns,
        roles=roles,
        name=name_filter,
        selected_roles=selected_roles,
        pick_rate_min=pick_rate_min if pick_rate_min is not None else '',
        pick_rate_max=pick_rate_max if pick_rate_max is not None else '',
        sort_column=sort_column,
        sort_order=sort_order,
        sortable_columns=sortable_columns,
        header_text=header_text
    )


if __name__ == '__main__':
    app.run(debug=True)
