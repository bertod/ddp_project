# Notes

Interesting and helfpul for researcher, we only ask you to better specify few points:
* About the graph, how (if) you intend to display the graph
* Explain which type of statistics you intend to implement (and show) about authors
* Explain the type (level) of visual interaction you would like to provide


# ddp_project

- core problem - brief summary of the core problem you try to solve;
Analyse the relationships among researchers in Computer Science who publish in top journals.
- application domain - description of the domain, the data to be handled, and the possible sources;
Historical data about papers published in top journals of each field (e.g. Artificial Intelligence, Machine Learning).
The data to be handled are metadata about papers, like authors, title and year. 
One possible source is DBLP https://dblp.uni-trier.de/ , which provides access to historical meta-data of publications in 
computer science.

## categorization
From both internal (raw data, derived data, algorithms, decision support, decision making) and external (APIs, visualization, interactive dashboard) perspectives;
    - Internal tasks:
        - WebScraping
        - Algorithms to: 
            - parse data
            - build graph
            - compute statistics (e.g. centrality) about authors
    - External tasks:
        - Visualization of graphs and statistics
        
## objective
Major objectives that should be achieved in terms of implemented features:
    - web scraper
    - data parser
    - graph builder
    - statistics on the graph
    - interactive/static visualizations of the data
    - filtering options on visualizations    


## Development team
Berto D'Attoma, Luca Giorgi
