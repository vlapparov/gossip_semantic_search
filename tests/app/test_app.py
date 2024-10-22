from streamlit.testing.v1 import AppTest


def test_no_interaction():
    at = AppTest.from_file("app/app.py")
    at.run()
    assert len(at.text_input) == 1
    assert at.text_input[0].value == ""
    assert at.text_input[0].label == "Enter your search query:"
    assert at.selectbox[0].label == "Select number of results (max 10):"
    assert at.selectbox[0].value == 5
    assert at.button[0].label == "Search"


def test_result_output():
    """
    Test the output of the app after input. The data is supposed to be static and ingested.
    """
    at = AppTest.from_file("app/app.py")
    at.run()
    at.text_input[0].input("Messi").run()
    at.selectbox[0].select(3).run()
    at.button[0].click().run()
    print(at.markdown[0].value)
    assert at.markdown[0].value.startswith("Lionel Messi : 8 buts en 5 matchs")
    assert len(at.text_input) == 1
    assert at.button[0].value
    assert len(at.subheader) == 3
    assert at.text_input[0].value == "Messi"
    assert at.text_input[0].label == "Enter your search query:"
    assert at.selectbox[0].label == "Select number of results (max 10):"
    assert at.selectbox[0].value == 3
    assert at.button[0].label == "Search"
