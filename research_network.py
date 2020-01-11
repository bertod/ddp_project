import pandas as pd
from ResearcherNetwork.scraper import Scraper


link_dict = {}
df_links = pd.read_csv("links.csv", sep=";")

for index, row in df_links.iterrows():
    # get html code from url
    #if index == 0:
    print("Downloading ", row['name'], "-", row['year'])
    scraper_instance = Scraper()
    html_content = scraper_instance.get_html_from_url(url=row['link'])
    # searching for links inside html page
    scraper_instance.scrape(target_tag="href", html_page=html_content, target_title=row['name'])
    #else:
        #print("skip link")
