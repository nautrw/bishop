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

for _ in range(generation):
    algorithm.move()

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
st.subheader("Heatmap")
fig = px.imshow(algorithm.graph, text_auto=True, color_continuous_scale="Viridis")
st.plotly_chart(fig)

st.divider()
st.subheader("Scatter Plot")
fig = px.scatter(graph_df, x="x", y="y", size="value", color="value", color_continuous_scale="plasma")
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
    ]
)
st.plotly_chart(fig)
