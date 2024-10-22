import streamlit as st

from data.dataset_preparation import preprocess_french_text
from models.sentence_embeddings import SentenceEmbeddings
from utils.postgres import PostgresClient


@st.cache_resource
def get_database_connector():
    return PostgresClient()


@st.cache_resource
def get_embedding_model():
    return SentenceEmbeddings()


def main():
    db_connector = get_database_connector()
    model = get_embedding_model()

    # Set up the Streamlit app
    st.title('Cool Gossip Search App')

    # Input field for the query
    query = st.text_input('Enter your search query:')

    # Dropdown to select the number of results (limit to 10)
    limit = st.selectbox('Select number of results (max 10):', [i for i in range(1, 11)], index=4)

    # Button to submit the query
    if st.button('Search'):

        if query:
            processed_query = preprocess_french_text(query)
            embedding = model.encode(processed_query)
            results = db_connector.search_similar_by_embedding(embedding=embedding, n_records=limit)

            # Display the results
            if results:
                for idx, result in enumerate(results, start=1):
                    st.subheader(f"Gossip {idx}")
                    article_preview = " ".join([x for x in result[1].split()[:30]]) + "..."
                    st.write(article_preview)
                    st.markdown(f"[Read more]({result[0]})", unsafe_allow_html=True)
            else:
                st.write("No results found for your query.")
        else:
            st.write("Please enter a query.")


if __name__ == "__main__":
    main()
