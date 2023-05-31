"""
This module provides descriptions for the various Database Columns.
Created by: Silvan Wiedmer
Crated at: 24.05.2023
"""
column_description: dict = {
    "author": """
        The "author" column in the DBLP data refers to the name(s) of the author(s) of a particular publication,
        such as a research paper or a book.""",
    "editor": """
        The "editor" field in the DBLP database typically refers to the editor(s)
        of a book or a special issue of a journal.""",
    "school": """
        The "school" column in the DBLP data refers to the institution or
        university where the authors of a publication are affiliated with.""",
    "pages": """
        The "pages" column in the DBLP data refers to the page numbers of a publication,
        such as a research paper or a book chapter.""",
    "publisher": """
        The "publisher" column in the DBLP data refers to the publisher of a publication,
        such as a book or a conference proceeding."""
}
def get_column_description(column_name: str = 'author') -> str:
    """
    This function returns the column description selected by the user.
    Parameters:
    - column_name: str = 'author' => the column selected by the user
    Return:
    - str => the column description
    """
    return column_description.get(
        column_name,
        "We were not able to load the according column description."
    )
