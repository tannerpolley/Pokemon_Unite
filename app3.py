import streamlit as st
import pandas as pd
import base64
from pathlib import Path
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode
import streamlit.components.v1 as components

st.set_page_config(layout="wide", page_title="Pokemon Unite Meta Tierlist")

st.markdown("""
<style>
.big-header {
    font-size: 200px !important;
    font-weight: bold !important;
    text-align: center !important;
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
}
</style>
""", unsafe_allow_html=True)

def zoom_aggrid_container(zoom_level: float = 1.5):
    return components.html(f"""
        <div style="zoom: {zoom_level}; transform-origin: top left;">
            <script>
                const container = window.parent.document.querySelectorAll('iframe[srcdoc]')[0].parentNode;
                container.style.zoom = '{zoom_level}';
                container.style.transformOrigin = 'top left';
            </script>
        </div>
    """, height=0)

# === Inject Zoom Wrapper ===
components.html("""
    <div style="zoom: 1.5; transform-origin: top left;">
        <div id="ag-grid-container"></div>
    </div>
""", height=0)

# === Load Data ===
@st.cache_data
def load_data():
    df = pd.read_csv("all_movesets.csv")

    def fix_path(p):
        return str(Path("static") / Path(p))

    df["Pokemon"] = df["Pokemon"].apply(fix_path)
    df["Move 1"] = df["Move 1"].apply(fix_path)
    df["Move 2"] = df["Move 2"].apply(fix_path)
    return df

df = load_data()

with open("date.txt", "r") as f:
    date = f.read()

# === Sidebar Filters ===
st.sidebar.header("Filters")
name_filter = st.sidebar.text_input("Search by Name")
roles = ["Attacker", "Speedster", "All-Rounder", "Supporter", "Defender"]
selected_roles = [role for role in roles if st.sidebar.checkbox(role, value=False, key=role)]
pick_rate_min = st.sidebar.number_input("Min Pick Rate (%)", min_value=0.0, max_value=100.0, value=0.0)

# === Apply Filtering & Sort by Win Rate Descending ===
filtered_df = df.copy()
if name_filter:
    filtered_df = filtered_df[filtered_df["Name"].str.lower() == name_filter.lower()]
if selected_roles:
    filtered_df = filtered_df[filtered_df["Role"].isin(selected_roles)]
filtered_df = filtered_df[filtered_df["Pick Rate"] >= pick_rate_min]
filtered_df = filtered_df.sort_values(by="Win Rate", ascending=False).reset_index(drop=True)

# === Convert Images to Base64 ===
def image_to_base64_url(path):
    try:
        with open(path, "rb") as f:
            return "data:image/png;base64," + base64.b64encode(f.read()).decode()
    except Exception:
        return ""

filtered_df["__Pokemon_img"] = filtered_df["Pokemon"].apply(image_to_base64_url)
filtered_df["__Move1_img"] = filtered_df["Move 1"].apply(image_to_base64_url)
filtered_df["__Move2_img"] = filtered_df["Move 2"].apply(image_to_base64_url)

# === Display DataFrame ===
df_display = filtered_df[["Name", "Move Set", "Win Rate", "Pick Rate", "Role"]].copy()
df_display["Move 1"] = filtered_df["__Move1_img"]
df_display["Move 2"] = filtered_df["__Move2_img"]
df_display["__Pokemon_img"] = filtered_df["__Pokemon_img"]  # for Name+Image combo rendering
df_display.insert(1, "Pokemon", filtered_df["__Pokemon_img"])

# === JavaScript Renderers ===
# name_with_img_renderer = JsCode("""
# function (params) {
#     if (params.data.__Pokemon_img) {
#         return `<span>
#             <img src="${params.data.__Pokemon_img}" width="40" style="vertical-align:middle; margin-right:8px;" />
#             ${params.value}
#         </span>`;
#     } else {
#         return params.value;
#     }
# }
# """)

image_only_renderer = JsCode("""
function (params) {
    if (params.value) {
        return `<img src="${params.value}" style="max-height: 80%; max-width: 80%; object-fit: contain; display: block; margin: auto;" />`;
    } else {
        return "";
    }
}
""")

column_style = {
    "fontSize": "30px",
    "textAlign": "center",
    "display": "flex",
    "justifyContent": "center",
    "alignItems": "center"
}


# === Grid Options ===
gb = GridOptionsBuilder.from_dataframe(df_display)
gb.configure_column("Pokemon", cellRenderer=image_only_renderer, autoHeight=True, cellStyle=column_style)
gb.configure_column("Name", cellStyle=column_style)
gb.configure_column("Move 1", cellRenderer=image_only_renderer, autoHeight=True, cellStyle=column_style)
gb.configure_column("Move 2", cellRenderer=image_only_renderer, autoHeight=True, cellStyle=column_style)
gb.configure_column("Win Rate", type=["numericColumn", "sortable"], cellStyle=column_style)
gb.configure_column("Pick Rate", type=["numericColumn", "sortable"], cellStyle=column_style)
gb.configure_column("Move Set", cellStyle=column_style)
gb.configure_column("Role", cellStyle=column_style)
gb.configure_column("__Pokemon_img", hide=True)
gb.configure_default_column(wrapText=True, autoHeight=True)

grid_options = gb.build()
grid_options["rowHeight"] = 100 # 👈 adjust as needed (default is ~25)
grid_options["defaultColDef"]["headerStyle"] = {
    "fontSize": "180px",
    "fontWeight": "bold",
    "textAlign": "center",
    "justifyContent": "center",
    "display": "flex",
    "alignItems": "center"
}

# === Main Title ===
st.title("Pokemon Unite Meta Moveset Tierlist")
st.caption(f"Data comes from Unite API as of {date}")
st.markdown("---")

# === Render Grid ===
zoom_aggrid_container(1.5)
AgGrid(
    df_display,
    gridOptions=grid_options,
    allow_unsafe_jscode=True,
    theme="streamlit",
    fit_columns_on_grid_load=True,  # 👈 disable default fitting
    columns_auto_size_mode="FIT_CONTENTS",  # 👈 auto-size to largest value
    height=900
)
