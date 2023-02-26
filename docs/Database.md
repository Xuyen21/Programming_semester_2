
# Database dblp

This file gives an overview of the dblp PostgreSQL database.

## Code Snippets

### entry

```SQL
DROP TABLE IF EXISTS entry;

CREATE TABLE entry(
    id BIGINT GENERATED ALWAYS AS IDENTITY,
    publish_date date NOT NULL,
    key VARCHAR,
    PRIMARY KEY(id)
);
```

### phdthesis

```SQL
DROP TABLE IF EXISTS phdthesis;

CREATE TABLE phdthesis (
    id BIGINT GENERATED ALWAYS AS IDENTITY,
    entry_id BIGINT NOT NULL,
    title VARCHAR,
    year INT,
    month INT,
    publisher VARCHAR,
    number INT,
    pages INT,
    isbn VARCHAR,
    series VARCHAR,
    volume INT,
    note VARCHAR,
    PRIMARY KEY (id),
    CONSTRAINT fk_entry
        FOREIGN KEY(entry_id) 
        REFERENCES entry(id)
);
```

### author

```SQL
DROP TABLE IF EXISTS author;

CREATE TABLE author (
    id BIGINT GENERATED ALWAYS AS IDENTITY,
    name VARCHAR,
    PRIMARY KEY (id)
);
```

### entry_author

```SQL
DROP TABLE IF EXISTS entry_author;

CREATE TABLE entry_author (
    id BIGINT GENERATED ALWAYS AS IDENTITY,
    author_id BIGINT,
    entry_id BIGINT,
    PRIMARY KEY (id),
    CONSTRAINT fk_entry
        FOREIGN KEY(entry_id) 
        REFERENCES entry(id),
    CONSTRAINT fk_author
        FOREIGN key(author_id)
        REFERENCES author(id)
);
```

### ee

```SQL
DROP TABLE IF EXISTS ee;

CREATE TABLE ee (
    id BIGINT GENERATED ALWAYS AS IDENTITY,
    url VARCHAR,
    PRIMARY KEY(id)
);
```

### entry_ee

```SQL
DROP TABLE IF EXISTS entry_ee;

CREATE TABLE entry_ee (
    id BIGINT GENERATED ALWAYS AS IDENTITY,
    ee_id BIGINT,
    entry_id BIGINT,
    PRIMARY KEY (id),
    CONSTRAINT fk_entry
        FOREIGN KEY(entry_id) 
        REFERENCES entry(id),
    CONSTRAINT fk_ee
        FOREIGN key(ee_id)
        REFERENCES ee(id)
);
```



## Multiple Instances

+ cdrom: `str`
+ cite: `str`
+ publisher: `str`
+ author: `str` => Done
+ note: `str`
+ school: `str` => Done
+ editor: `str` => Done
+ url: `str` or `url` => Done
+ ee: `str` or `url` => Done
+ crossref: `str` or `url` => Done

## ERD

```mermaid
---
title: Database Overview
---
erDiagram

    entry ||--|| phdthesis: is
    entry ||--|| article: is
    entry ||--|| book: is
    entry ||--|| mastersthesis: is
    entry ||--|| incollection: is
    entry ||--|| proceedings: is
    entry ||--|| www: is
    entry ||--|| inproceedings: is

    article }o--|| entry_author: has
    phdthesis }o--|| entry_author: has
    book }o--|| entry_author: has
    mastersthesis }o--|| entry_author: has
    incollection }o--|| entry_author: has
    proceedings }o--|| entry_author: has
    www }o--|| entry_author: has
    inproceedings }o--|| entry_author: has

    entry_author ||--o{ author: has

    phdthesis }o--|| entry_school: "made by"
    book }o--|| entry_school: "made by"
    mastersthesis }o--|| entry_school: "made by"
    proceedings }o--|| entry_school: "made by"

    entry_school ||--o{ school: has

    article }o--|| entry_editor: has
    book }o--|| entry_editor: has
    proceedings }o--|| entry_editor: has
    www }o--|| entry_editor: has
    inproceedings }o--|| entry_editor: has

    entry_editor ||--o{ editor: has

    article }o--|| entry_url: has
    book }o--|| entry_url: has
    incollection }o--|| entry_url: has
    proceedings }o--|| entry_url: has
    www }o--|| entry_url: has
    inproceedings }o--|| entry_url: has

    entry_url ||--o{ url: has

    article }o--|| entry_ee: has
    phdthesis }o--|| entry_ee: has
    book }o--|| entry_ee: has
    mastersthesis }o--|| entry_ee: has
    incollection }o--|| entry_ee: has
    proceedings }o--|| entry_ee: has
    www }o--|| entry_ee: has
    inproceedings }o--|| entry_ee: has

    entry_ee ||--o{ ee: has

    article }o--|| entry_crossref: has
    book }o--|| entry_crossref: has
    incollection }o--|| entry_crossref: has
    www }o--|| entry_crossref: has
    inproceedings }o--|| entry_crossref: has

    entry_crossref ||--o{ crossref: has

    entry {
        bigint id PK
        date publish_date
    }

    article {
        bigint entry_id FK
        int pages
        int year
        string journal
        int number
        string url
        int volume
        string drossref
        int month
        char note
        char cdrom
        char editor
        char cite
        char booktitle
        int publnr
        int publisher
        char ee
    }

    phdthesis {
        bigint entry_id FK
        char title
        int year
        char publisher
        int number
        int pages
        str isbn
        int month
        char series
        int volume
        char note
    }

    book {
        bigint entry_id FK
        char title
        char school
        int year
        char publisher
        char series
        char volume
        char isbn
        char ee
        int pages
        char note
        char editor
        char booktitle
        char url
        char crossref
        int month
        char cite
        char cdrom
    }

    mastersthesis {
        bigint entry_id FK
        char title
        int year
        char school
        char ee
        char note
    }

    incollection {
        bigint entry_id FK
        char title
        int pages
        int year
        char booktitle
        char ee
        char crossref
        char url
        char cite
        char publisher
        int number
        char note
        char drom
        char chapter
    }

    proceedings {
        bigint entry_id FK
        char editor
        char title
        char publisher
        int year
        char sibn
        char ee
        char url
        char booktitle
        char series
        char volume
        int volume
        int number
        char note
        char pages
        char school
        char address
        char journal
        char cite
    }

    www {
        bigint entry_id FK
        char title
        char url
        char note
        char crossref
        char cite
        char ee
        int year
        char editor
    }

    inproceedings {
        bigint entry_id FK
        char title
        char booktitle
        char year
        char url
        char crossref
        char ee
        char pages
        char cite
        char cdrom
        char note
        char editor
        int number
        int volume
        int month
    }

    entry_author {
        bigint id PK
        bigint author_id FK
        bigint entry_id FK
    }

    author {
        bigint id PK
        char name
    }

    entry_school {
        bigint id PK
        bigint school_id FK
        bigint entry_id FK
    }

    school {
        bigint id PK
        char name
    }

    entry_editor {
        bigint id PK
        bigint editor_id FK
        bigint entry_id FK
    }

    editor {
        bigint id PK
        char name
    }

    entry_url {
        bigint id PK
        bigint url_id FK
        bigint entry_id FK
    }

    url {
        bigint id PK
        char url
    }

    entry_ee {
        bigint id PK
        bigint ee_id FK
        bigint entry_id FK
    }

    ee {
        bigint id PK
        char url
    }

    entry_crossref {
        bigint id PK
        bigint crossref_id FK
        bigint entry_id FK
    }

    crossref {
        bigint id PK
        char url
    }
```
