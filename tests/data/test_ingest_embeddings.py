import pandas as pd

from data.ingest_embeddings import preprocess_article_data


def test_preprocess_article_data():
    # Sample DataFrame to test
    df = pd.DataFrame({
        "url": ["http://example.com/1", "http://example.com/2", None, "http://example.com/1"],
        "raw_text": ["Article 1 text", "Article 2 text", "Article 3 text", "Article 1 text"],
        "author": ["Author 1", "Author 2", "Author 3", "Author 1"]
    })

    # Expected DataFrame after processing (removing NaN and duplicates)
    expected_df = pd.DataFrame({
        "url": ["http://example.com/1", "http://example.com/2"],
        "raw_text": ["Article 1 text", "Article 2 text"],
        "author": ["Author 1", "Author 2"]
    })

    # Resetting index for consistency when comparing DataFrames
    expected_df = expected_df.reset_index(drop=True)

    # Run the function and compare the output DataFrame to the expected DataFrame
    processed_df = preprocess_article_data(df)
    processed_df = processed_df.reset_index(drop=True)  # Reset index to compare correctly

    pd.testing.assert_frame_equal(processed_df, expected_df)
