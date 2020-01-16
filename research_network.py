import pandas as pd
from lxml import etree
import os
import argparse
from ResearcherNetwork.scraper import ConcreteScraperDblpCreator
from ResearcherNetwork.parser import ConcreteParserDblpCreator
from ResearcherNetwork.parser import Parser


def run(scraper_output_path="ResearcherNetwork/resources/",
        links_file_path="resources/links.csv",
        output_file_path="ResearcherNetwork/resources/parser_out.txt"):
    df_links = pd.read_csv(links_file_path, sep=";")
    for index, row in df_links.iterrows():
        # get html code from url
        # if index == 0:
        print("Downloading ", row['name'], "-", row['year'])
        scraper_instance = ConcreteScraperDblpCreator()
        html_content = scraper_instance.get_html_from_url(url=row['link'])
        # searching for links inside html page
        scraper_instance.run_scrape(target_tag="href", html_page=html_content,
                                     target_title=row['name'], path_to_save=scraper_output_path)

    parser_instance = ConcreteParserDblpCreator()
    folders = df_links.name.unique()

    fout = open(output_file_path, 'w')

    for folder in folders:
        for file in sorted(os.listdir(scraper_output_path + folder)):
            context = etree.iterparse(scraper_output_path + folder + "/" + file,
                                      load_dtd=True, html=True, events=["start", "end"])
            parser_instance.run_fast_iter(context, parser_instance.run_process_element, fout=fout)
    fout.close()


if __name__ == "__main__":
    run()
    arguments = argparse.ArgumentParser('DBLP Researcher Graph Builder')
    arguments.add_argument('-s', '--scraperout',
                           default="ResearcherNetwork/resources/",
                           help='output path of the scraper, default value: ResearcherNetwork/resources/ ')
    arguments.add_argument('-l', '--linksfile',
                           default="resources/links.csv",
                           help='file containing the url links to be scraped')
    arguments.add_argument('-p', '--parserout',
                           default="ResearcherNetwork/resources/parser_out.txt",
                           help='output file path of the parser, '
                                 'default value: ResearcherNetwork/resources/parser_out.txt ')
    args = arguments.parse_args()

    run(args.scraperout, args.linksfile, args.parserout)
