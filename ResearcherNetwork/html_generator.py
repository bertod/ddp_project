class StaticHtml:
    def __init__(self, datasource, html_output_file="static.html", year_list=[0], avenue_list=['']):
        self.html_output_file = html_output_file
        self.datasource = datasource
        self.htmlf = open(self.html_output_file, "w+")
        if len(year_list) > 1:
            year_span = "years: from " + str(min(year_list)) + " to " + str(max(year_list))
        else:
            year_span = "year: " + str(year_list[0])

        header = "<html><head><script type=\"text/javascript\" src=\"scripts.js\"></script>\n" \
                 "<link rel=\"stylesheet\" type=\"text/css\" href=\"style.css\">" \
                 "<title>Researcher Network Builder</title></head><body>\n" \
                 "<div class=\"headrow_home\"><h1>" + self.datasource.upper() + " Researcher Network</h1>\n"
        header += "<h2>Development of Data Products Project </h2>\n" \
                  "<h3><i>years: " + year_span + "<br>\navenues: " + ', '.join(avenue_list) + "</i></h3><br><br><br>"

        self.htmlf.write(header)
        self.statistics_dict = None

    def close_page(self):
        self.htmlf.write("\n<p> Developed by Berto D'Attoma and Luca Giorgi</p>")
        self.htmlf.write("\n</body>\n</html>")
        self.htmlf.close()

    def write_statistics(self, statistics_dict):
        self.statistics_dict = statistics_dict
        self.htmlf.write("\n<br><div class=\"headrow\"><h1>Baseline Statistics</h1></div>\n")
        self.htmlf.write(
            "<button id = 'statistics_show' class = 'button' onclick=\"myFunction('statistics')\">Show/Hide</button>")
        self.htmlf.write("\n<div id = 'statistics' style=\"display : block\">")
        self.htmlf.write("<p> In the table below, some baseline statistics "
                         "computed on data extracted from the selected DataSource"
                         " are reported."
                         "</p><br>")
        self.htmlf.write(
            "\n<table class=\"blueTable\">\n<thead><tr><td>Statistic title</td><td>Value</td><tr></thead>\n")
        self.print_details()
        self.htmlf.write(
            "\n</table>\n<br>\n")
        self.htmlf.write("\n</div>")
        # self.htmlf.close()

    def add_graph_image(self, lib_name, output_path):
        self.htmlf.write("\n<br><div class=\"headrow\"><h1>" + lib_name + " Static Graph</h1></div>\n")
        self.htmlf.write(
            "<button id = 'graph" + lib_name + "'_show' class = 'button' "
                                               "onclick=\"myFunction('" + lib_name + "')\">Show/Hide</button>")
        self.htmlf.write("\n<div id = '" + lib_name + "' style=\"display : block\">")
        image_path = "{}{}_graph.png".format(output_path, lib_name)
        self.htmlf.write("<p>Below the static graph, generated with " + lib_name + " library.</p> \
        <br><table class = 'tableImg'><tr><td><img src='" + image_path + "' width = '1500' height = '700'></td></tr></table>")
        self.htmlf.write("\n</div>")

    def print_details(self):
        for column_name, value in self.statistics_dict.items():
            if column_name in ["papers_authors_count"] or type(value['value']) == dict:
                row = self.print_inner_table(value, column_name)
                self.htmlf.write(row)
            else:
                self.htmlf.write("<tr><td>" + value['title'] + "</td><td>" + str(value['value']))

    def print_inner_table(self, value, column_name):
        dots_id_title = "dots_" + column_name
        btn_id_title = "myBtn_" + column_name
        more_id_title = "more_" + column_name
        row = "<tr><td>" + value['title'] + "</td><td>"
        row_count = 0
        if len(value['value']) > 5:
            row += "<button onclick=\"readMore('" + dots_id_title + "','" + \
                   more_id_title + "','" + btn_id_title + "' )\" id=\"" + btn_id_title + "\">" \
                   "load more</button><table class = \"rankingTable\">\n"
        else:
            row += "<table class = \"rankingTable\">\n"

        if all(isinstance(item, tuple) for item in value['value']):
            for a, c in value['value']:
                row += "<tr><td>" + a + "</td><td>" + str(c) + "</td></tr>\n"
                if row_count == 5:
                    # row += "<span id = \"dots\"></span></table>" \
                    row += "<span id =" + dots_id_title + "></span></table>" \
                           "<span id = \"" + more_id_title + "\"><table class = \"rankingTable\">"
                row_count += 1
            row += "</span></table></td></tr>"
        else:
            for a, c in value['value'].items():
                row += "<tr><td>" + str(a) + "</td><td>" + str(c) + "</td></tr>\n"
                if row_count == 5:
                    # row += "<span id = \"dots\"></span></table>" \
                    row += "<span id =\"" + dots_id_title + "\"></span></table>" \
                           "<span id = \"" + more_id_title + "\"><table class = \"rankingTable\">"
                row_count += 1
            row += "</span></table></td></tr>"
        return row
