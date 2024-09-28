import pandas as pd
import streamlit as st
from book_recommendations.utils import db, metrics, query, ui

tab_titles = [
    "Collaborative Filtering",
    "GraphSAGE User Embeddings",
    "GraphSAGE Book Embeddings",
    "FastRP Book Embeddings",
]
tab1, tab2, tab3, tab4 = st.tabs(tab_titles)


st.markdown(
    """
    <style>
        div[data-testid="stImageContainer"] {
            display: block;
            margin-left: auto;
            margin-right: auto;
        }
    <style>
    """,
    unsafe_allow_html=True,
)


# # Define HTML and CSS for the tooltip
# html_content = """
# <style>
# .tooltip {
#   position: relative;
#   cursor: pointer;
# }

# .tooltip .tooltiptext {
#   visibility: hidden;
#   width: auto;
#   background-color: black;
#   color: white;
#   text-align: left;
#   border-radius: 6px;
#   padding: 8px 8px;
#   position: absolute;
#   z-index: 1;
#   top: 100%;
#   left: 50%;
#   margin-left: -60px;
#   opacity: 0;
#   transition: opacity 0.3s;
# }

# .tooltip:hover .tooltiptext {
#   visibility: visible;
#   opacity: 1;
# }
# </style>
# """

# # Display HTML in Streamlit
# st.markdown(html_content, unsafe_allow_html=True)

user_id_to_inspect = st.session_state["user_id_to_inspect"]

books_per_row = 8

result = db.run_query(
    query.collbaorative_filtering.substitute({"user_id": user_id_to_inspect})
)
books_filtering = pd.DataFrame(result.records, columns=result.keys)

st.sidebar.header("Recommendation Metrics", divider=True)
st.sidebar.caption(
    "Metrics use the 100 highest scoring recommendations of collaborative filtering as ground truth."
)

with tab1:
    # result = db.run_query(query.collbaorative_filtering.substitute({"user_id": 1}))
    # books_filtering= pd.DataFrame(result.records, columns=result.keys)

    st.header(f"Top {books_per_row*2} Book Recommendations via {tab_titles[0]}:")
    ui.render_books(books_filtering, books_per_row=books_per_row)
    st.markdown(
        "##### Cypher query used to produce these results:\n"
        f"```cypher\n{query.collbaorative_filtering.substitute({'user_id': user_id_to_inspect})}\n```"
    )

with tab2:
    result = db.run_query(query.graphSAGE_similar_users.substitute({"user_id": 1}))
    book_examples = pd.DataFrame(result.records, columns=result.keys)

    st.header(f"Top {books_per_row*2} Book Recommendations via {tab_titles[1]}:")
    ui.render_books(book_examples, books_per_row=books_per_row)
    st.markdown(
        "##### Cypher query used to produce these results:\n"
        f"```cypher\n{query.graphSAGE_similar_users.substitute({'user_id': user_id_to_inspect})}\n```"
    )

    st.sidebar.subheader(tab_titles[1])
    st.sidebar.text(
        "Recall@10:\t"
        + str(metrics.recall_at(books_filtering, book_examples, 10))
        + "\n"
        + "Recall@20:\t"
        + str(metrics.recall_at(books_filtering, book_examples, 20))
        + "\n"
        + "Precision@10:\t"
        + str(metrics.precision_at(books_filtering, book_examples, 10))
        + "\n"
        + "Precision@20:\t"
        + str(metrics.precision_at(books_filtering, book_examples, 20))
    )

with tab3:
    result = db.run_query(
        query.graphSAGE_similar_books.substitute({"user_id": user_id_to_inspect})
    )
    book_examples = pd.DataFrame(result.records, columns=result.keys)

    st.header(f"Top {books_per_row*2} Book Recommendations via {tab_titles[2]}:")
    ui.render_books(book_examples, books_per_row=books_per_row)
    st.markdown(
        "##### Cypher query used to produce these results:\n"
        f"```cypher\n{query.graphSAGE_similar_books.substitute({'user_id': user_id_to_inspect})}\n```"
    )

    st.sidebar.subheader(tab_titles[2])
    st.sidebar.text(
        "Recall@10:\t"
        + str(metrics.recall_at(books_filtering, book_examples, 10))
        + "\n"
        + "Recall@20:\t"
        + str(metrics.recall_at(books_filtering, book_examples, 20))
        + "\n"
        + "Precision@10:\t"
        + str(metrics.precision_at(books_filtering, book_examples, 10))
        + "\n"
        + "Precision@20:\t"
        + str(metrics.precision_at(books_filtering, book_examples, 20))
    )

with tab4:
    result = db.run_query(
        query.fastRP_similar_books.substitute({"user_id": user_id_to_inspect})
    )
    book_examples = pd.DataFrame(result.records, columns=result.keys)

    st.header(f"Top {books_per_row*2} Book Recommendations via {tab_titles[3]}:")
    ui.render_books(book_examples, books_per_row=books_per_row)
    st.markdown(
        "##### Cypher query used to produce these results:\n"
        f"```cypher\n{query.fastRP_similar_books.substitute({'user_id': user_id_to_inspect})}\n```"
    )

    st.sidebar.subheader(tab_titles[3])
    st.sidebar.text(
        "Recall@10:\t"
        + str(metrics.recall_at(books_filtering, book_examples, 10))
        + "\n"
        + "Recall@20:\t"
        + str(metrics.recall_at(books_filtering, book_examples, 20))
        + "\n"
        + "Precision@10:\t"
        + str(metrics.precision_at(books_filtering, book_examples, 10))
        + "\n"
        + "Precision@20:\t"
        + str(metrics.precision_at(books_filtering, book_examples, 20))
    )
