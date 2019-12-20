
## ddp_project

- core problem - brief summary of the core problem you try to solve;
Analyse the relationships among researchers in Computer Science who publish in top journals.
- application domain - description of the domain, the data to be handled, and the possible sources;<br>
Historical data about papers published in top journals of each field (e.g. Artificial Intelligence, Machine Learning).
The data to be handled are metadata about papers, like authors, title and year. 
One possible source is DBLP https://dblp.uni-trier.de/ , which provides access to historical meta-data of publications in 
computer science.

- categorization - from both internal (raw data, derived data, algorithms, decision support, decision making) and external (APIs, visualization, interactive dashboard) perspectives;
    - Internal tasks:
        - WebScraping
        - Algorithms to: 
            - parse data
            - build graph
            - compute statistics (e.g. centrality) about authors
    - External tasks:
        - Visualization of graphs and statistics
        
- objective - major objectives that should be achieved in terms of implemented features;
Features to be implemented:
    - web scraper
    - data parser
    - graph builder
    - statistics on the graph
    - interactive/static visualizations of the data
    - filtering options on visualizations    


- development team - students part of the team (max 4).<br>
Berto D'Attoma
Luca Giorgi
