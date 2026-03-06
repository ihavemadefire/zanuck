# Independent Film Distribution Analysis  
### A Data-Driven Decision-Making Project

## Overview

This project analyzes the contemporary independent film distribution landscape using publicly available data. The objective is to explore how independent distributors such as **A24**, **Neon**, and **MUBI** allocate capital across film projects and how those investments translate into both commercial and critical success.

The project culminates in a **data-informed framework for film greenlighting**, illustrating how historical performance data can guide future investment decisions in independent filmmaking.

---

## Analytical Objective

The central research question of this project is:

> How can historical data from independent film distributors inform more disciplined greenlighting decisions for future film projects?

To answer this question, the project analyzes a portfolio of films from three prominent distributors:

- **A24**
- **Neon**
- **MUBI**

By examining relationships between **budget, box office performance, critical reception, and genre**, the analysis identifies patterns of capital efficiency within the independent film market.

---

## Data Sources

The dataset was constructed from several publicly available sources.

### Wikipedia Film Lists
Film lists were scraped from distributor pages:

- https://en.wikipedia.org/wiki/List_of_A24_films
- https://en.wikipedia.org/wiki/List_of_Neon_films
- https://en.wikipedia.org/wiki/List_of_Mubi_films

These pages provided the initial list of film titles and release years.

### OMDb API
The **Open Movie Database API** was used to enrich the dataset with additional metadata including:

- Genre
- IMDb rating
- Metascore
- Runtime
- Box office revenue

### Wikipedia Film Pages
Individual film pages were scraped to retrieve **production budget information** from the film infobox.

---

## Data Pipeline

The dataset was created through several structured stages.

### 1. Film List Scraping

Custom Python scrapers using **BeautifulSoup** extracted film titles and release dates from distributor film lists.

Output files:


a24_released_2010s_2020s.csv
neon_released_2010s_2020s.csv
mubi_released_2016_plus.csv


---

### 2. Seed Dataset Construction

The scraped film lists were merged into a unified dataset containing:


company
title
year


Output file:


seed_films.csv


---

### 3. Metadata Enrichment (OMDb)

Each film was queried against the OMDb API to retrieve additional attributes:

- Genre
- IMDb rating
- Metascore
- Runtime
- Box office revenue

Output file:


films_enriched.csv


---

### 4. Genre Cleaning and Normalization

Genre classifications were standardized to improve analytical clarity.

Key steps included:

- Removing noisy genres such as **Biography**, **Music**, **Short**, and **Talk Show**
- Prioritizing **Horror** classification when present
- Creating a **primary_genre** field to assign each film a dominant genre category

Output file:


films_cleaned.csv


---

### 5. Budget Extraction

Production budgets were scraped from each film’s Wikipedia page by parsing the **infobox table** and locating the row labeled **Budget**.

Budget values were converted into numeric USD values to allow quantitative analysis.

Output file:


films_with_budget.csv


---

### 6. Capital Efficiency Analysis

Capital efficiency was measured using the following metric:


ROI = box_office / budget


This metric measures how effectively each film converted production investment into revenue.

The project identifies the **top 10 most capital-efficient films** in the dataset.

Output file:


top_10_capital_efficient.csv


---

## Visualizations

Three major visualizations were created to analyze the dataset.

### Genre Portfolio Distribution

A stacked bar chart illustrating how each distributor allocates films across genres.  
This visualization highlights the **strategic identity** of each distributor.

---

### Strategy Bubble Map

A scatter plot mapping:


X-axis: Box Office Revenue
Y-axis: IMDb Rating
Bubble Size: Runtime
Color: Genre


This chart illustrates how films perform across **commercial and critical dimensions**.

---

### Efficiency Frontier

A log-scaled scatter plot mapping:


X-axis: Production Budget
Y-axis: Box Office Revenue


Films along the upper boundary represent the **most capital-efficient investments**.

This visualization forms the foundation of the project's **data-informed greenlighting framework**.

---

## Tools and Libraries

This project was implemented in Python using:

- **pandas** — data manipulation and analysis
- **requests** — API calls and HTTP requests
- **BeautifulSoup** — HTML parsing and web scraping
- **seaborn** — statistical visualization
- **matplotlib** — plotting framework
- **tqdm** — progress monitoring for long-running scripts

---

## Key Insight

The analysis suggests that certain genres—particularly **horror and low-budget genre films**—tend to produce significantly higher revenue relative to production cost.

These findings suggest that **strategic portfolio balance**, rather than purely intuitive decision-making, can improve financial outcomes for independent film distributors.

---

## Project Structure


project/
│
├── data/
│ ├── seed_films.csv
│ ├── films_enriched.csv
│ ├── films_cleaned.csv
│ ├── films_with_budget.csv
│ └── top_10_capital_efficient.csv
│
├── scripts/
│ ├── scrape_a24.py
│ ├── scrape_neon.py
│ ├── scrape_mubi.py
│ ├── enrich_with_omdb.py
│ ├── scrape_budget.py
│ └── top_10_capital_efficient.py
│
└── README.md


---

## Author

Jacob Ide  
Data-Driven Decision Making Final Project