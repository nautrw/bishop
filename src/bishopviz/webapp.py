import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from bishopviz.algorithm import DrunkenBishopAlgorithm
from bishopviz.charsets import CHARACTER_SETS
from bishopviz.globals import GRAPH_HEIGHT, GRAPH_WIDTH
from bishopviz.hash import bytes_to_pairs, text_md5

st.header("Drunken Bishop Algorithm Randomart")

feed = st.text_area(
    "Feed",
    placeholder="Put some text here to visualize its randomart",
)

hash = text_md5(feed)
st.write(f"Hash from text: {hash.hexdigest()}")

byte_pairs = bytes_to_pairs(hash.digest())

algorithm = DrunkenBishopAlgorithm(GRAPH_WIDTH, GRAPH_HEIGHT, byte_pairs)

generation = st.slider("Generation", min_value=0, max_value=64, step=1, value=64, help="Change the slider to view the algorithm at a specific generation.")

movements_dict = {"Generation": [], "Left": [], "Right": [], "Up": [], "Down": [], "Net Horizontal Movement": [], "Net Vertical Movement": [], "x": [], "y": []}

for i in range(generation):
    algorithm.move()

    movements_dict["Generation"].append(i)
    movements_dict["Left"].append(algorithm.times_left)
    movements_dict["Right"].append(algorithm.times_right)
    movements_dict["Up"].append(algorithm.times_up)
    movements_dict["Down"].append(algorithm.times_down)

    movements_dict["Net Horizontal Movement"].append(algorithm.times_right - algorithm.times_left)
    movements_dict["Net Vertical Movement"].append(algorithm.times_down - algorithm.times_up)

    movements_dict["x"].append(algorithm.bishop_x)
    movements_dict["y"].append(algorithm.bishop_y)

movements_df = pd.DataFrame(movements_dict)

graph_dict = {"x": [], "y": [], "value": []}
for y, row in enumerate(algorithm.graph):
    for x, tile in enumerate(row):
        graph_dict["x"].append(x)
        graph_dict["y"].append(y)
        graph_dict["value"].append(tile)
graph_df = pd.DataFrame(graph_dict)

charset = st.selectbox("Character Set", ("ascii", "ascii_alt", "emoji", "emoji2", "emoji3", "emoji4", "greek", "cyrillic", "katakana", "math", "blocks", "faces", "cars", "plants"))
accomodate_large_chars = charset in ["emoji", "emoji2", "emoji3", "emoji4", "katakana", "faces", "cars", "plants"]
st.code(algorithm.draw_graph(CHARACTER_SETS[charset], show_start=True, show_end=True, show_current_position=True, accomodate_large_chars=accomodate_large_chars, colorize=False), language="None", width="content")

st.divider()
st.subheader("Position over time")
fig = px.line(movements_df, x="Generation", y=["x", "y"])
st.plotly_chart(fig)

st.divider()
st.subheader("Movements Over Time")
fig = px.area(movements_df, x="Generation", y=["Left", "Right", "Up", "Down"])
st.plotly_chart(fig)

st.divider()
st.subheader("Directional Bias")
st.write("Negative horizontal values are leftward, positive are right. Negative vertical values are upward, negative are downward.")
fig = px.line(movements_df, x="Generation", y=["Net Horizontal Movement", "Net Vertical Movement"])
st.plotly_chart(fig)

st.divider()
st.subheader("Heatmap")
fig = px.imshow(algorithm.graph, text_auto=True, color_continuous_scale="Viridis")
fig.update_layout(xaxis_title="x", yaxis_title="y", coloraxis_colorbar_title="Visits")
st.plotly_chart(fig)

st.divider()
st.subheader("Scatter Plot")
fig = px.scatter(graph_df, x="x", y="y", size="value", color="value", color_continuous_scale="plasma")
fig.update_layout(xaxis_title="x", yaxis_title="y", coloraxis_colorbar_title="Visits")
st.plotly_chart(fig)

st.divider()
st.subheader("3D Surface Plot")
fig = go.Figure(
    data=[
        go.Surface(
            x=graph_df.x,
            y=graph_df.y,
            z=graph_df.values,
            colorscale="Viridis",
            contours={
                "z": {
                    "show": True,
                    "usecolormap": True,
                    "highlightcolor": "white",
                    "project_z": True,
                }
            },
        )
    ],
)
fig.update_layout(
    scene={
        "zaxis_title": "Visits",
        "xaxis_title": "x",
        "yaxis_title": "y",
    },
)
st.plotly_chart(fig)
