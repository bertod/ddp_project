# Notes

Interesting and helfpul for researcher, we only ask you to better specify few points:
* About the graph, how (if) you intend to display the graph
    - Build a graph representation internally (Probably with adjacency lists, since I am guessing a matrix would be very sparse and a waste of space)
    - Build a visual representation with either [NetworkX](https://networkx.github.io/) or [Graph-Tool](https://graph-tool.skewed.de/) starting from our internal view of the graph. Graph-Tool provides [dynamic visualizations](https://graph-tool.skewed.de/static/doc/demos/animation/animation.html#interactive-visualizations) and instead NetworkX seems to only provide [static visualizations](https://networkx.github.io/documentation/stable/reference/drawing.html), albeit with the possibility to import its output format into more specialized pieces of software for interactive visualizations.
* Explain which type of statistics you intend to implement (and show) about authors
    - As of now, the only statistic we have settled on is author centrality in the graph. Starting from that we might also compare the change in centrality YoY or aggregate data from multiple years, but it still has not been defined.
* Explain the type (level) of visual interaction you would like to provide
    - Regarding author centrality (and more "baseline" statistics, i.e. number of authors, papers etc.) we are aiming for an interactive webpage that enables the user to filter the data from which statistics are computed and gets back appropriate visualizations for each stat. We still have not set in stone how we want this to look, and implementing a dynamic webpage might prove too much work given the timeframe, in which case we might produce static visualizations when running the code and then show them in a static document or html page.


# ddp_project

- core problem - brief summary of the core problem you try to solve;

    - Analyse the relationships among researchers in Computer Science who publish in top journals.
    
- application domain - description of the domain, the data to be handled, and the possible sources;

    - Historical data about papers published in top journals of each field (e.g. Artificial Intelligence, Machine Learning).
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
