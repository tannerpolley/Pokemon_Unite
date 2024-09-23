from flask import Flask, render_template, request
import pandas as pd

# Step 1: Load the Excel data into a pandas DataFrame
df = pd.read_csv('all_movesets.csv')

# Step 2: Initialize the Flask app
app = Flask(__name__)

# Step 3: Create a route for the home page
@app.route('/', methods=['GET', 'POST'])
def index():
    # Retrieve role filters and other filters from the request (if any)
    selected_roles = request.form.getlist('role') if request.method == 'POST' else []
    column_filter = request.form.get('column_filter', '')
    filter_operator = request.form.get('filter_operator', 'contains')
    value_filter = request.form.get('value_filter', '')

    # Filter the DataFrame based on selected roles
    filtered_df = df.copy()
    if selected_roles:
        filtered_df = filtered_df[filtered_df['Role'].isin(selected_roles)]

    # Filter the DataFrame based on column values and operator
    if column_filter and value_filter:
        try:
            # Numeric comparison for greater than / less than
            if filter_operator == 'greater_than':
                filtered_df = filtered_df[filtered_df[column_filter].astype(float) > float(value_filter)]
            elif filter_operator == 'less_than':
                filtered_df = filtered_df[filtered_df[column_filter].astype(float) < float(value_filter)]
            # Textual or exact match filter
            else:
                filtered_df = filtered_df[filtered_df[column_filter].astype(str).str.contains(value_filter, case=False, na=False)]
        except ValueError:
            # Handle cases where conversion to float fails (non-numeric data)
            pass

    # Convert the filtered DataFrame to HTML and add bootstrap classes for styling
    table_html = filtered_df.to_html(classes='table table-striped table-bordered', index=False)

    # Get column names for column-specific filtering
    columns = df.columns.tolist()

    return render_template('index.html', table=table_html, selected_roles=selected_roles, columns=columns, column_filter=column_filter, filter_operator=filter_operator, value_filter=value_filter)

# Step 4: Run the app
if __name__ == '__main__':
    app.run(debug=True)
