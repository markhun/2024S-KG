import pandas as pd
import streamlit as st
from book_recommendations.utils import db, query

st.header("View best rated books by user")

user_id_to_inspect = st.session_state["user_id_to_inspect"]

st.text(f"Best rated books by user ID:{user_id_to_inspect}")

result = db.run_query(query.liked_books.substitute({"user_id": user_id_to_inspect}))
liked_books = pd.DataFrame(result.records, columns=result.keys)
liked_books["book.book_id"] = liked_books["book.book_id"].apply(str)


# Converting links to html tags
def path_to_image_html(path):
    if path is None:
        return ""
    return '<img src="' + path + '" width="100" >'


def path_to_dbpedia_link(path):
    if path is None:
        return ""
    # return '<a href="' + str(path) + ">DBpedia</a>"
    return f'<a href="{path}">DBpedia</a>'


liked_books["book.image_url"] = liked_books["book.image_url"].apply(path_to_image_html)
liked_books["book.dbpedia_resource"] = liked_books["book.dbpedia_resource"].apply(
    path_to_dbpedia_link
)

st.markdown(
    liked_books.to_html(
        escape=False,
        index=False,
        justify="left",
    ),
    unsafe_allow_html=True,
)
