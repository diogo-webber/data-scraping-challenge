[challenge_source]: https://medium.com/@meigarom/o-projeto-de-data-engineering-para-o-seu-portfólio-c186c7191823
[books_website]: http://books.toscrape.com

<img src="https://i.imgur.com/zm2paNE.png" align="left" width="185px"/>

# Data Scraping Practice

> A small project that uses the [**Scrapy**](https://scrapy.org) module to scrape a book catalog.

Challenge Instructions: [**Medium [PT-BR]**][challenge_source]

<br>

## What does this script do?

* Extracts book data from [**books.toscrape**][books_website] website to a CSV file;
* Import the data to a Postgres database table;
<br>

## Prerequisites

* Python >=3.9
* Docker-compose
<br>

## Setup

**1.** Install the dependencies.
```sh
  python -m pip install -r requirements.txt
```
<br>

**2.** Initialize the **postgres** databases.
```sh
   docker-compose up -d
```

<br>

## Usage

Just run:

```sh
   python main.py
```

<br>

## What I've learned with this project?

   > * Small study of data types to create the database table.
   > * Initial learning of the powerful [**Scrapy**](https://scrapy.org) library for data scraping.
   > * I used the python context manager feature in the database class.
