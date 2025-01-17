import pandas as pd
from lxml import etree
import os
import sys
import argparse
import webbrowser
from ResearcherNetwork.graph import GraphBuilder
from ResearcherNetwork.statistics import StatisticsGrabber
from ResearcherNetwork.system_builder import ConcreteAnalyzerBuilder, Director
from ResearcherNetwork.html_generator import StaticHtml


def run(datasource="dblp",
        scraper_output_path="ResearcherNetwork/resources/",
        links_file_path="resources/links.csv",
        output_file_path="ResearcherNetwork/resources/parser_out.txt",
        statistics_output_file="ResearcherNetwork/resources/statistics_out.txt",
        run_html=1):
    df_links = pd.read_csv(links_file_path, sep=";")

    if datasource.lower() == "dblp":
        builder = ConcreteAnalyzerBuilder()
        director = Director()
        director.builder = builder
        director.build_dblp_analyzer()
        source_analyzer = builder.product
    else:
        print("we are sorry but {] is not supported. At the moment you can select only DBLP"
              "New ones might be available in the future".format(datasource))
        sys.exit()

    avenue_list = []
    year_list = []
    print("I'm going to run the web scraper. It might take time..."
          "so don't worry if it seems stuck, because it isn't actually")
    for index, row in df_links.iterrows():
        if row['name'] not in avenue_list:
            avenue_list.append(row['name'])
        if row['year'] not in year_list:
            year_list.append(row['year'])
        print("Downloading ", row['name'], "-", row['year'])
        source_analyzer.parts['scraper'].run_scrape(target_tag="href", url=row['link'], html_page=None,
                                                    target_title=row['name'], path_to_save=scraper_output_path)

    html_generator = StaticHtml(datasource=datasource,
                                html_output_file="static.html", year_list=year_list, avenue_list=avenue_list)

    folders = df_links.name.unique()

    fout = open(output_file_path, 'w')
    print("The scraping is Done. Now it's time to parse data.")
    for folder in folders:
        for file in sorted(os.listdir(scraper_output_path + folder)):
            context = etree.iterparse(scraper_output_path + folder + "/" + file,
                                      load_dtd=True, html=True, events=["start", "end"])
            source_analyzer.parts['parser'].run_fast_iter(context, fout=fout, years=year_list)
    fout.close()

    g = GraphBuilder(output_file_path, output=scraper_output_path)  # output_file_path is the parser output file

    s = StatisticsGrabber(file=output_file_path, output_file_path=statistics_output_file)
    print("\nComputing Statistics...")
    statistics_dict = s.get_statistics(graph_builder=g)
    print("Done! You can find them in {}".format(s.output_file_path))
    html_generator.write_statistics(statistics_dict)

    while True:
        print(
            "\nYou can either generate a static image file visualizing the graph or see an interactive visualization.")
        print("What would you like to do? (1) Static Image (2) Interactive Window (q) to quit")
        choice = input("> ")
        if choice == "1":
            while True:
                print("\nYou can either use NetworkX or Graph-Tool.")
                print("What would you like to do? (1) NetworkX (2) Graph-Tool (q) to quit")
                choice_sv = input("> ")
                if choice_sv == "1":
                    g.snap_with_networkx()
                    html_generator.add_graph_image(lib_name="networkx", output_path=g.output_path)
                    break
                elif choice_sv == "2":
                    g.snap_with_graphtool()
                    html_generator.add_graph_image(lib_name="graphtool", output_path=g.output_path)
                    break
                elif choice_sv == "q":
                    break
                else:
                    print("\nI didn't understand your choice, use either 1 or 2. Enter q to quit.")
                    continue
        elif choice == "2":
            while True:
                print("\nYou can either use NetworkX, Graph-Tool or Bokeh.")
                print("What would you like to do? (1) NetworkX (2) Graph-Tool (3) Bokeh (q) to quit")
                choice_iv = input("> ")
                if choice_iv == "1":
                    g.draw_with_networkx()
                    break
                elif choice_iv == "2":
                    g.draw_with_graphtool()
                    break
                elif choice_iv == "3":
                    g.draw_with_bokeh()
                    break
                elif choice_iv == "q":
                    break
                else:
                    print("\nI didn't understand your choice, use either 1, 2 or 3. Enter q to quit.")
                    continue
        elif choice == "q":
            html_generator.close_page()
            if run_html == 1:
                print("Now, I'm going to open the static html page with 3"
                      "statistics and static graphs (if you chose them)")
                try:
                    print("opening..")
                    url = "file:///{}".format(os.path.abspath(html_generator.html_output_file))
                    webbrowser.open(url, new=1)
                except:
                    print("ops..something with opening your browser went wrong. "
                          "Open {} to visualize the page.".format(os.path.abspath(html_generator.html_output_file)))
                    pass
            else:
                print("You'll find the static html page at the following "
                      "path:{}".format(os.path.abspath(html_generator.html_output_file)))
                print("Goodbye...")
            break
        else:
            print("\nI didn't understand your choice, use either 1 or 2. Enter q to quit.")
            continue


if __name__ == "__main__":
    """
    This is the main function called when the project is run via CLI. 
    It calls the run() method (see above) which is in charge of
    calling all the modules in the project (e.g. Scraper, graph builder etc)   
    """
    # run()
    print("Welcome to Research Network builder\n")
    arguments = argparse.ArgumentParser('DBLP Researcher Graph Builder')
    arguments.add_argument('-o', '--origin',
                           default="dblp",
                           help='Source of data. Default value: dblp ')
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
    arguments.add_argument('-t', '--statsout',
                           default="ResearcherNetwork/resources/statistics_out.txt",
                           help='output file path where statistics have to been saved, '
                                'default value: ResearcherNetwork/resources/statistics_out.txt ')
    arguments.add_argument('-r', '--runhtml',
                           default=1,
                           help='if you want me to open the static html '
                                'page with results after you quit, pass 1. Otherwise 0')
    args = arguments.parse_args()

    run(args.origin, args.scraperout, args.linksfile, args.parserout, args.statsout, args.runhtml)
