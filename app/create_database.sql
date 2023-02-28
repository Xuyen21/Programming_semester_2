DROP TABLE IF EXISTS phdthesis CASCADE;

DROP TABLE IF EXISTS article CASCADE;

DROP TABLE IF EXISTS book CASCADE;

DROP TABLE IF EXISTS mastersthesis CASCADE;

DROP TABLE IF EXISTS incollection CASCADE;

DROP TABLE IF EXISTS proceedings CASCADE;

DROP TABLE IF EXISTS www CASCADE;

DROP TABLE IF EXISTS inproceedings CASCADE;

DROP TABLE IF EXISTS data CASCADE;

DROP TABLE IF EXISTS author CASCADE;

DROP TABLE IF EXISTS entry_author CASCADE;

DROP TABLE IF EXISTS school CASCADE;

DROP TABLE IF EXISTS publisher CASCADE;

DROP TABLE IF EXISTS entry_school CASCADE;

DROP TABLE IF EXISTS entry_publisher CASCADE;

DROP TABLE IF EXISTS ee CASCADE;

DROP TABLE IF EXISTS entry_ee CASCADE;

DROP TABLE IF EXISTS note CASCADE;

DROP TABLE IF EXISTS entry_note CASCADE;

DROP TABLE IF EXISTS isbn CASCADE;

DROP TABLE IF EXISTS entry_isbn CASCADE;

DROP TABLE IF EXISTS pages CASCADE;

DROP TABLE IF EXISTS entry_pages CASCADE;

DROP TABLE IF EXISTS cdrom CASCADE;

DROP TABLE IF EXISTS entry_cdrom CASCADE;

DROP TABLE IF EXISTS cite CASCADE;

DROP TABLE IF EXISTS entry_cite CASCADE;

DROP TABLE IF EXISTS editor CASCADE;

DROP TABLE IF EXISTS entry_editor CASCADE;

DROP TABLE IF EXISTS url CASCADE;

DROP TABLE IF EXISTS entry_url CASCADE;

DROP TABLE IF EXISTS crossref CASCADE;

DROP TABLE IF EXISTS entry_crossref CASCADE;

DROP TABLE IF EXISTS year CASCADE;

DROP TABLE IF EXISTS entry_year CASCADE;

DROP TABLE IF EXISTS title CASCADE;

DROP TABLE IF EXISTS entry_title CASCADE;

DROP TABLE IF EXISTS series CASCADE;

DROP TABLE IF EXISTS entry_series CASCADE;

DROP TABLE IF EXISTS entry;

CREATE TABLE entry(
    id BIGINT GENERATED ALWAYS AS IDENTITY,
    publish_date date NOT NULL,
    key VARCHAR,
    PRIMARY KEY(id)
);

CREATE TABLE phdthesis (
    id BIGINT GENERATED ALWAYS AS IDENTITY,
    entry_id BIGINT NOT NULL,
    title VARCHAR,
    month VARCHAR,
    number VARCHAR,
    series VARCHAR,
    volume VARCHAR,
    PRIMARY KEY (id),
    CONSTRAINT fk_entry
        FOREIGN KEY(entry_id) 
        REFERENCES entry(id)
        ON DELETE CASCADE
);

CREATE TABLE article (
    id BIGINT GENERATED ALWAYS AS IDENTITY,
    entry_id BIGINT NOT NULL,
    title VARCHAR,
    journal VARCHAR,
    number VARCHAR,
    volume VARCHAR,
    month VARCHAR,
    booktitle VARCHAR,
    publnr VARCHAR,
    PRIMARY KEY (id),
    CONSTRAINT fk_entry
        FOREIGN KEY(entry_id) 
        REFERENCES entry(id)
        ON DELETE CASCADE
);

CREATE TABLE book (
    id BIGINT GENERATED ALWAYS AS IDENTITY,
    entry_id BIGINT NOT NULL,
    title VARCHAR,
    series VARCHAR,
    volume VARCHAR,
    booktitle VARCHAR,
    month VARCHAR,
    PRIMARY KEY (id),
    CONSTRAINT fk_entry
        FOREIGN KEY(entry_id) 
        REFERENCES entry(id)
        ON DELETE CASCADE
);

CREATE TABLE mastersthesis (
    id BIGINT GENERATED ALWAYS AS IDENTITY,
    entry_id BIGINT NOT NULL,
    title VARCHAR,
    PRIMARY KEY (id),
    CONSTRAINT fk_entry
        FOREIGN KEY(entry_id) 
        REFERENCES entry(id)
        ON DELETE CASCADE
);

CREATE TABLE incollection (
    id BIGINT GENERATED ALWAYS AS IDENTITY,
    entry_id BIGINT NOT NULL,
    title VARCHAR,
    booktitle VARCHAR,
    number VARCHAR,
    chapter VARCHAR,
    PRIMARY KEY (id),
    CONSTRAINT fk_entry
        FOREIGN KEY(entry_id) 
        REFERENCES entry(id)
        ON DELETE CASCADE
);

CREATE TABLE proceedings (
    id BIGINT GENERATED ALWAYS AS IDENTITY,
    entry_id BIGINT NOT NULL,
    title VARCHAR,
    booktitle VARCHAR,
    series VARCHAR,
    volume VARCHAR,
    number VARCHAR,
    address VARCHAR,
    journal VARCHAR,
    PRIMARY KEY (id),
    CONSTRAINT fk_entry
        FOREIGN KEY(entry_id) 
        REFERENCES entry(id)
        ON DELETE CASCADE
);

CREATE TABLE www (
    id BIGINT GENERATED ALWAYS AS IDENTITY,
    entry_id BIGINT NOT NULL,
    title VARCHAR,
    PRIMARY KEY (id),
    CONSTRAINT fk_entry
        FOREIGN KEY(entry_id) 
        REFERENCES entry(id)
        ON DELETE CASCADE
);

CREATE TABLE inproceedings (
    id BIGINT GENERATED ALWAYS AS IDENTITY,
    entry_id BIGINT NOT NULL,
    title VARCHAR,
    booktitle VARCHAR,
    number VARCHAR,
    volume VARCHAR,
    month VARCHAR,
    PRIMARY KEY (id),
    CONSTRAINT fk_entry
        FOREIGN KEY(entry_id) 
        REFERENCES entry(id)
        ON DELETE CASCADE
);

CREATE TABLE data (
    id BIGINT GENERATED ALWAYS AS IDENTITY,
    entry_id BIGINT NOT NULL,
    title VARCHAR,
    month VARCHAR,
    number VARCHAR,
    PRIMARY KEY (id),
    CONSTRAINT fk_entry
        FOREIGN KEY(entry_id) 
        REFERENCES entry(id)
        ON DELETE CASCADE
);

CREATE TABLE author (
    id BIGINT GENERATED ALWAYS AS IDENTITY,
    name VARCHAR,
    PRIMARY KEY (id)
);

CREATE TABLE entry_author (
    id BIGINT GENERATED ALWAYS AS IDENTITY,
    author_id BIGINT,
    entry_id BIGINT,
    PRIMARY KEY (id),
    CONSTRAINT fk_entry
        FOREIGN KEY(entry_id)
        REFERENCES entry(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_author
        FOREIGN key(author_id)
        REFERENCES author(id)
        ON DELETE CASCADE
);

CREATE TABLE school (
    id BIGINT GENERATED ALWAYS AS IDENTITY,
    name VARCHAR,
    PRIMARY KEY (id)
);

CREATE TABLE entry_school (
    id BIGINT GENERATED ALWAYS AS IDENTITY,
    school_id BIGINT,
    entry_id BIGINT,
    PRIMARY KEY (id),
    CONSTRAINT fk_entry
        FOREIGN KEY(entry_id)
        REFERENCES entry(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_school
        FOREIGN key(school_id)
        REFERENCES school(id)
        ON DELETE CASCADE
);

CREATE TABLE publisher (
    id BIGINT GENERATED ALWAYS AS IDENTITY,
    name VARCHAR,
    PRIMARY KEY (id)
);

CREATE TABLE entry_publisher (
    id BIGINT GENERATED ALWAYS AS IDENTITY,
    publisher_id BIGINT,
    entry_id BIGINT,
    PRIMARY KEY (id),
    CONSTRAINT fk_entry
        FOREIGN KEY(entry_id)
        REFERENCES entry(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_publisher
        FOREIGN key(publisher_id)
        REFERENCES publisher(id)
        ON DELETE CASCADE
);

CREATE TABLE ee (
    id BIGINT GENERATED ALWAYS AS IDENTITY,
    name VARCHAR,
    PRIMARY KEY(id)
);

CREATE TABLE entry_ee (
    id BIGINT GENERATED ALWAYS AS IDENTITY,
    ee_id BIGINT,
    entry_id BIGINT,
    PRIMARY KEY (id),
    CONSTRAINT fk_entry
        FOREIGN KEY(entry_id)
        REFERENCES entry(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_ee
        FOREIGN key(ee_id)
        REFERENCES ee(id)
        ON DELETE CASCADE
);

CREATE TABLE note (
    id BIGINT GENERATED ALWAYS AS IDENTITY,
    name VARCHAR,
    PRIMARY KEY(id)
);

CREATE TABLE entry_note (
    id BIGINT GENERATED ALWAYS AS IDENTITY,
    note_id BIGINT,
    entry_id BIGINT,
    PRIMARY KEY (id),
    CONSTRAINT fk_entry
        FOREIGN KEY(entry_id)
        REFERENCES entry(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_note
        FOREIGN key(note_id)
        REFERENCES note(id)
        ON DELETE CASCADE
);

CREATE TABLE isbn (
    id BIGINT GENERATED ALWAYS AS IDENTITY,
    name VARCHAR,
    PRIMARY KEY(id)
);

CREATE TABLE entry_isbn (
    id BIGINT GENERATED ALWAYS AS IDENTITY,
    isbn_id BIGINT,
    entry_id BIGINT,
    PRIMARY KEY (id),
    CONSTRAINT fk_entry
        FOREIGN KEY(entry_id)
        REFERENCES entry(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_isbn
        FOREIGN key(isbn_id)
        REFERENCES isbn(id)
        ON DELETE CASCADE
);

CREATE TABLE pages (
    id BIGINT GENERATED ALWAYS AS IDENTITY,
    name VARCHAR,
    PRIMARY KEY(id)
);

CREATE TABLE entry_pages (
    id BIGINT GENERATED ALWAYS AS IDENTITY,
    pages_id BIGINT,
    entry_id BIGINT,
    PRIMARY KEY (id),
    CONSTRAINT fk_entry
        FOREIGN KEY(entry_id)
        REFERENCES entry(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_pages
        FOREIGN key(pages_id)
        REFERENCES pages(id)
        ON DELETE CASCADE
);

CREATE TABLE cdrom (
    id BIGINT GENERATED ALWAYS AS IDENTITY,
    name VARCHAR,
    PRIMARY KEY(id)
);

CREATE TABLE entry_cdrom (
    id BIGINT GENERATED ALWAYS AS IDENTITY,
    cdrom_id BIGINT,
    entry_id BIGINT,
    PRIMARY KEY (id),
    CONSTRAINT fk_entry
        FOREIGN KEY(entry_id)
        REFERENCES entry(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_cdrom
        FOREIGN key(cdrom_id)
        REFERENCES cdrom(id)
        ON DELETE CASCADE
);

CREATE TABLE cite (
    id BIGINT GENERATED ALWAYS AS IDENTITY,
    name VARCHAR,
    PRIMARY KEY(id)
);

CREATE TABLE entry_cite (
    id BIGINT GENERATED ALWAYS AS IDENTITY,
    cite_id BIGINT,
    entry_id BIGINT,
    PRIMARY KEY (id),
    CONSTRAINT fk_entry
        FOREIGN KEY(entry_id)
        REFERENCES entry(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_cite
        FOREIGN key(cite_id)
        REFERENCES cite(id)
        ON DELETE CASCADE
);

CREATE TABLE editor (
    id BIGINT GENERATED ALWAYS AS IDENTITY,
    name VARCHAR,
    PRIMARY KEY(id)
);

CREATE TABLE entry_editor (
    id BIGINT GENERATED ALWAYS AS IDENTITY,
    editor_id BIGINT,
    entry_id BIGINT,
    PRIMARY KEY (id),
    CONSTRAINT fk_entry
        FOREIGN KEY(entry_id)
        REFERENCES entry(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_editor
        FOREIGN key(editor_id)
        REFERENCES editor(id)
        ON DELETE CASCADE
);

CREATE TABLE url (
    id BIGINT GENERATED ALWAYS AS IDENTITY,
    name VARCHAR,
    PRIMARY KEY(id)
);

CREATE TABLE entry_url (
    id BIGINT GENERATED ALWAYS AS IDENTITY,
    url_id BIGINT,
    entry_id BIGINT,
    PRIMARY KEY (id),
    CONSTRAINT fk_entry
        FOREIGN KEY(entry_id)
        REFERENCES entry(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_url
        FOREIGN key(url_id)
        REFERENCES url(id)
        ON DELETE CASCADE
);

CREATE TABLE crossref (
    id BIGINT GENERATED ALWAYS AS IDENTITY,
    name VARCHAR,
    PRIMARY KEY(id)
);

CREATE TABLE entry_crossref (
    id BIGINT GENERATED ALWAYS AS IDENTITY,
    crossref_id BIGINT,
    entry_id BIGINT,
    PRIMARY KEY (id),
    CONSTRAINT fk_entry
        FOREIGN KEY(entry_id)
        REFERENCES entry(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_crossref
        FOREIGN key(crossref_id)
        REFERENCES crossref(id)
        ON DELETE CASCADE
);

CREATE TABLE year (
    id BIGINT GENERATED ALWAYS AS IDENTITY,
    name INT,
    PRIMARY KEY(id)
);

CREATE TABLE entry_year (
    id BIGINT GENERATED ALWAYS AS IDENTITY,
    year_id BIGINT,
    entry_id BIGINT,
    PRIMARY KEY (id),
    CONSTRAINT fk_entry
        FOREIGN KEY(entry_id)
        REFERENCES entry(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_year
        FOREIGN key(year_id)
        REFERENCES year(id)
        ON DELETE CASCADE
);

CREATE TABLE title (
    id BIGINT GENERATED ALWAYS AS IDENTITY,
    name VARCHAR,
    PRIMARY KEY(id)
);

CREATE TABLE entry_title (
    id BIGINT GENERATED ALWAYS AS IDENTITY,
    title_id BIGINT,
    entry_id BIGINT,
    PRIMARY KEY (id),
    CONSTRAINT fk_entry
        FOREIGN KEY(entry_id)
        REFERENCES entry(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_title
        FOREIGN key(title_id)
        REFERENCES title(id)
        ON DELETE CASCADE
);

CREATE TABLE series (
    id BIGINT GENERATED ALWAYS AS IDENTITY,
    name VARCHAR,
    PRIMARY KEY(id)
);

CREATE TABLE entry_series (
    id BIGINT GENERATED ALWAYS AS IDENTITY,
    series_id BIGINT,
    entry_id BIGINT,
    PRIMARY KEY (id),
    CONSTRAINT fk_entry
        FOREIGN KEY(entry_id)
        REFERENCES entry(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_series
        FOREIGN key(series_id)
        REFERENCES series(id)
        ON DELETE CASCADE
);