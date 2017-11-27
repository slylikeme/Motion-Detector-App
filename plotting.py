from motion_detector import df
from bokeh.plotting import figure, output_file, show
from bokeh.models import HoverTool, ColumnDataSource


# convert datetime to strings
df["Start_string"] = df["Start"].dt.strftime("%Y-%m-%d %H:%M:%S")
df["End_string"] = df["End"].dt.strftime("%Y-%m-%d %H:%M:%S")

# convert dataframe to ColumnDataSource object
cds = ColumnDataSource(df)

# params for plotting
p = figure(x_axis_type="datetime", height=100, width=500,
           responsive=True, title="Motion Graph")

# remove unnecessary tick lines from y-axis
p.yaxis.minor_tick_line_color = None

# remove grid from graph
p.ygrid[0].ticker.desired_num_ticks = 1

# create hover object
hover = HoverTool(tooltips=[("Start", "@Start_string"), ("End", "@End_string")])
p.add_tools(hover)

# plot a quad glyph to visualize datetime
q = p.quad(left="Start", right="End", bottom=0, top=1, color="Green", source=cds)

# write html file to local directory and display graph
output_file("TimeGraph.html")
show(p)
