import streamlit as st
import pandas as pd


def main():
    # Load the dataset (can be replaced with your own backend or database)
    data = pd.read_csv('data/processed/processed.csv')
    data = data.dropna()
    data = data.drop_duplicates(subset=['raw_text'])

    # Set up the Streamlit app
    st.title('Semantic Search Application')

    # Input field for the query
    query = st.text_input('Enter your search query:')

    # Dropdown to select the number of results (limit to 10)
    limit = st.selectbox('Select number of results (max 10):', [i for i in range(1, 11)], index=4)

    # Button to submit the query
    if st.button('Search'):

        if query:
            # Filter the data based on the query (simple string match for demonstration)
            filtered_data = data[data['url'].str.contains(query, case=False, na=False)]

            # Limit the results to the user-specified number
            limited_results = filtered_data.head(limit).to_dict(orient='records')
            for x in limited_results:
                print(x, end='\n---------\n')
            print(limited_results)

            # Display the results
            if limited_results:
                for result in limited_results:
                    st.subheader(result['raw_text'][:200])
                    st.write(result['processed_text'][:200])  # Show a snippet of content (first 200 characters)
                    st.markdown(f"[Read more]({result['url']})", unsafe_allow_html=True)
            else:
                st.write("No results found for your query.")
        else:
            st.write("Please enter a query.")


if __name__ == "__main__":
    main()