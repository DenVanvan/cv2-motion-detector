from videocapture import df_timestamp
from bokeh.plotting import show, figure, output_file
from bokeh.models import ColumnDataSource

df_timestamp['Start_str'] = df_timestamp['Start'].dt.strftime('%Y-%m-%d %H-%M-%S')
df_timestamp['End_str'] = df_timestamp['End'].dt.strftime('%Y-%m-%d %H-%M-%S')

cds_timestamp = ColumnDataSource(df_timestamp)


viz = figure(width = 1000, height = 350, title = 'Object motion detected time', x_axis_type = 'datetime', tools = ['pan', 'hover'], tooltips = 'The object appeared at "@Start_str" and disappeared at "@End_str"')
viz.yaxis.minor_tick_out = 1
viz.title.text_font_size = '50'
viz.title.align = 'center'
# viz.ygrid[0].ticker.desired_num_ticks= 1

viz.quad(left = 'Start', right = "End", bottom = 0, top = 1, color = 'green', source = cds_timestamp)

show(viz)
