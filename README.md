# USICS scraper
This repo is a scrapy project that scrapes the complete [USICS website](https://www.uscis.gov/) based on its [sitemap](https://www.uscis.gov/sitemap).

## Installation
In order to run the project, make sure you've got the relevant dependencies installed using the `requirements.txt` file.

```
pip install -r requirements.txt
```

## Running

The scrapy spider is called `uscis_sitemap`. It can be run using the following:

```
scrapy crawl uscis_sitemap
```

The results will be saved to the `uscis_scraper/output/htmls/` folder as html files for each page.


## Supporting materials
More details about the project can be found in this youtube video.



