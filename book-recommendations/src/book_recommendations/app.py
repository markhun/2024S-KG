from pathlib import Path

import streamlit as st
from PIL import Image

package_dir = Path(__file__).resolve().parents[0]
logo = Image.open(package_dir / "assets" / "books_emoji.png")

st.logo(logo)

st.set_page_config(layout="wide")

user_id_to_inspect = st.sidebar.number_input(
    label="User ID to recommend for:", min_value=1, value=1, step=1
)

st.session_state["user_id_to_inspect"] = user_id_to_inspect

pg = st.navigation(
    [
        st.Page("views/recommendations.py", title="Recommendations"),
        st.Page("views/view_database.py", title="DB Viewer"),
    ]
)

pg.run()
