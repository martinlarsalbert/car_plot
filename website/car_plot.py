from flask import Flask, render_template, request
import pandas as pd
from bokeh.plotting import figure
from bokeh.transform import factor_cmap, factor_mark
from bokeh.models import HoverTool
from bokeh.models import ColumnDataSource

from bokeh.embed import components

app = Flask(__name__)


def load_data():
    # Load the Iris Data Set
    df_cars = pd.read_csv('data/cars_publish.csv', index_col=0)
    return df_cars


df_cars = load_data()
numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
y_columns = list(df_cars.select_dtypes(include=numerics))

# Create the main plot
def create_figure(y_column,x_column):

    df_cars = load_data()
    source = ColumnDataSource(data=df_cars)

    hover = HoverTool(
        tooltips=[
            ("Modell", "@Modell"),
            ("price", "@price"),

        ]
    )

    p = figure(title='Cars', tools=[hover])

    #x_column = 'Tillverkningsår'
    #y_column = 'price'

    markers = ['circle']

    p.scatter(x=x_column, y=y_column, source=source,
              legend="car type",
              marker=factor_mark('car type', markers=markers, factors=df_cars['car type'].unique()),
              color=factor_cmap('car type', palette='Category10_3', factors=df_cars['car type'].unique()),
              size=8, alpha=0.25)

    p.xaxis.axis_label = x_column
    p.yaxis.axis_label = y_column
    return p


# Index page
@app.route('/')
def index():
    # Determine the selected feature
    y_column = request.args.get("y_column")
    if y_column == None:
        y_column = "price"

    x_column = request.args.get("x_column")
    if x_column == None:
        x_column = "Tillverkningsår"

    # Create the plot
    plot = create_figure(y_column, x_column)

    # Embed plot into HTML via Flask Render
    script, div = components(plot)
    return render_template("plot.html", script=script, div=div,y_column = y_column,x_column = x_column,y_columns = y_columns)


# With debug=True, Flask server will auto-reload
# when there are code changes
if __name__ == '__main__':
    app.run(port=5000, debug=True)