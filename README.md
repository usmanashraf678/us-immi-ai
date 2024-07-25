# USICS scraper
This repo is a scrapy project that scrapes the complete [USICS website](https://www.uscis.gov/) based on its [sitemap](https://www.uscis.gov/sitemap).

## Installation
You should follow the following steps to clone the repo and run it on your PC locally:


### Clone the project
```
git clone https://github.com/usmanashraf678/us-immi-ai
```

### Create Virtual Environment
```
python3 -m venv venv
```

### Install dependencies
```
pip install -r requirements.txt
```

### Activate the Virtual Environment
```
Linux: source venv/bin/activate
Windows: .\venv\Scripts\activate
```


### Run the scraper
The scrapy spider is called `uscis_sitemap`. It can be run using the following:
```
scrapy crawl uscis_sitemap
```

### Output
The results will be saved to the `uscis_scraper/output/htmls/` folder as html files for each page.


## Supporting materials
More details about the project can be found in this youtube video.



