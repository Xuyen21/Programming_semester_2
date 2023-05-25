column_description: dict = {
    "author": """
        The "author" column in the DBLP data refers to the name(s) of the author(s) of a particular publication,
        such as a research paper or a book.""",
    "editor": """
        The "editor" field in the DBLP database typically refers to the editor(s) of a book or a special issue of a journal.""",
    "school": """The "school" column in the DBLP data refers to the institution or university where the authors of a publication are affiliated with.
        This information can be useful in visualizing the distribution of research output across different institutions and identifying patterns of collaboration and research partnerships.""",
    "pages": """
        The "pages" column in the DBLP data refers to the page numbers of a publication, such as a research paper or a book chapter.
        Visualizing the "pages" column can provide insights into the length and complexity of the publications in the dataset.
        This could help you identify whether most publications are short or long, or whether there are a few outliers with very long or very short page numbers.""",
    "publisher": """
        The "publisher" column in the DBLP data refers to the publisher of a publication, such as a book or a conference proceeding.
        Visualizing the "publisher" column can provide insights into the distribution of publications across different publishers and the trends in publishing over time."""
}
def get_column_description(column_name: str = 'author') -> str:
    """
    This function returns the column description selected by the user.
    Parameters:
    - column_name: str = 'author' => the column selected by the user
    Return:
    - str => the column description
    """
    return column_description.get(column_name, "We were not able to load the according column description.")