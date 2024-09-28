import string

import pandas as pd
import streamlit as st

image_with_tooltip = string.Template(
    """
<div class="tooltip">
  <img src="$image_url" alt="Image" style="width:100px;height:auto;;margin: auto;display: block;">
  <span class="tooltiptext">
    Tooltip text </br>
    Second line </br>
    And the last line
  </span>
</div>
"""
)

image_without_tooltip = string.Template(
    """
<div>
  <img src="$image_url" alt="Image" style="width:100px;height:auto;;margin: auto;display: block;">
</div>
"""
)


def _chunk_dataframe(df, chunk_size):
    chunks = list()
    num_chunks = len(df) // chunk_size + 1
    for i in range(num_chunks):
        chunks.append(df[i * chunk_size : (i + 1) * chunk_size])
    return chunks


def render_books(books_to_render: pd.DataFrame, books_per_row=10):

    books_chunked = _chunk_dataframe(books_to_render, books_per_row)

    books: pd.DataFrame = books_chunked[0]
    columns = st.columns(books_per_row, gap="medium", vertical_alignment="bottom")
    for idx in range(0, len(books)):
        col = columns[idx]
        with col:
            st.markdown(
                f"<div style='text-align: center;'><strong>{books.iloc[idx]['Title']}</strong></div>",
                unsafe_allow_html=True,
            )
            # st.container(height=10, border=False)
            st.markdown(
                image_without_tooltip.substitute(
                    {"image_url": books.iloc[idx]["image_url"]}
                ),
                unsafe_allow_html=True,
            )
            # st.image(books.iloc[idx]["image_url"])
            st.text(
                "Avg.Rating: "
                + str(round(books.iloc[idx]["average_rating"], 2))
                + "\n"
                + "Score: "
                + str(round(books.iloc[idx]["score"], 2))
            )

    books: pd.DataFrame = books_chunked[1]
    columns = st.columns(books_per_row, gap="medium", vertical_alignment="bottom")

    for idx in range(0, len(books)):
        col = columns[idx]
        with col:
            st.markdown(
                f"<div style='text-align: center;'><strong>{books.iloc[idx]['Title']}</strong></div>",
                unsafe_allow_html=True,
            )
            # st.container(height=10, border=False)
            st.markdown(
                image_without_tooltip.substitute(
                    {"image_url": books.iloc[idx]["image_url"]}
                ),
                unsafe_allow_html=True,
            )
            # st.image(books.iloc[idx]["image_url"])
            st.text(
                "Avg.Rating: "
                + str(round(books.iloc[idx]["average_rating"], 2))
                + "\n"
                + "Score: "
                + str(round(books.iloc[idx]["score"], 2))
            )

    st.divider()
