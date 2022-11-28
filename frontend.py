from flask import Flask, render_template, request
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import PointDrawTool, LassoSelectTool, BoxSelectTool, TapTool
import sqlite3
import pandas as pd
import json
from backend import produce_graph_values, tissue_conductivity_value,tissue_e_infinity_value,tissue_e_static_value,tissue_tau_value

app = Flask(__name__)


def get_graph_values():
    dat = sqlite3.connect('database.db')
    query = dat.execute("SELECT * From store")
    cols = [column[0] for column in query.description]
    results = pd.DataFrame.from_records(data=query.fetchall(), columns=cols)
    return results


@app.route('/', methods=['GET', 'POST'])
def home():
    tissue = 1000
    # code to collect the 4 Debye inputs
    if request.method == "POST":

        if request.form.get('action') == 'SUBMIT':
            default_value = 0
            print(request.data)
            conductivity = request.form.get('debye1', default_value)
            e_static = request.form.get('debye2', default_value)
            e_infinity = request.form.get('debye3', default_value)
            tau = request.form.get('debye4', default_value)
            tissue = request.form.get('Tissue', default_value)
            with open("Debye/parameters.json", 'w+') as file:
                print("writing new json values")
                data = {'conductivity': conductivity, 'e-static': e_static, 'e-infinity': e_infinity, 'tau': tau}
                print(data)
                json.dump(data, file)
            produce_graph_values()

    results = get_graph_values()
    # code to produce the graph for the webpage
    x = list(results['frequency'])
    y1 = list(results['permittivity'])
    y2 = list(results['conductivity'])

    plot = figure(width=800, height=400, x_axis_type="log", y_axis_type="log", toolbar_location="below",
                  x_axis_label="Frequency", y_axis_label="y")

    plot.line(x, y1, legend_label="relative permittivity", color="blue", line_width=4)

    plot.line(x, y2, legend_label="conductivity", color="red", line_width=4)

    permittivity_graph = plot.circle(x, y1, legend_label="relative permittivity", color="navy", size=2)

    conductivity_graph = plot.circle(x, y2, legend_label="conductivity", color="brown", size=2)

    plot.yaxis.ticker = [1, 10, 100]

    adjust_graph_area = PointDrawTool(renderers=[permittivity_graph,conductivity_graph])

    plot.add_tools(adjust_graph_area,LassoSelectTool(),BoxSelectTool(),TapTool())

    script, div = components(plot)
    kwargs = {'script': script, 'div': div}

    return render_template("home.html", **kwargs, tissue_conductivity=tissue_conductivity_value(tissue), tissue_e_static=tissue_e_static_value(tissue), tissue_e_infinity=tissue_e_infinity_value(tissue), tissue_tau=tissue_tau_value(tissue) )


if __name__ == "__main__":
    app.run(debug=True)
