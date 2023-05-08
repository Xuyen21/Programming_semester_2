def get_agres_contents(column_name: str = 'publisher'):
    """ return the description of the column which user chooses"""
    if column_name == 'author':
        return """
        The "author" column in the DBLP data refers to the name(s) of the author(s) of a particular publication,
        such as a research paper or a book.\n
        Below is the visualization of authors with the most publication.
        """
    if column_name == 'editor':
        return """The "editor" field in the DBLP database typically refers to the editor(s) of a book or a special issue of a journal.\n
         Below is the visualization of the number of books edited by each editor."""
    if column_name == 'school':
        return """The "school" column in the DBLP data refers to the institution or university where the authors of a publication are affiliated with.
        This information can be useful in visualizing the distribution of research output across different institutions and identifying patterns of collaboration and research partnerships.\n
        Below is the visualization of the universities/ institutions that has the most publications
        """
    if column_name == 'pages':
        return """ The "pages" column in the DBLP data refers to the page numbers of a publication, such as a research paper or a book chapter.
        Visualizing the "pages" column can provide insights into the length and complexity of the publications in the dataset.\n
        Below is the visualization of the distribution of page numbers across the publications.
        This could help you identify whether most publications are short or long, or whether there are a few outliers with very long or very short page numbers.
        """
    if column_name == 'publisher':
        return """ The "publisher" column in the DBLP data refers to the publisher of a publication, such as a book or a conference proceeding.
        Visualizing the "publisher" column can provide insights into the distribution of publications across different publishers and the trends in publishing over time.\n
        Below is the visualization of the distribution of publications across the most popular publishers
        """
