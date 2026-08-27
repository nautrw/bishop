import plotly.express as px
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

generation = st.slider("Generation", min_value=1, max_value=64, step=1, value=64, help="Change the slider to view the algorithm at a specific generation.")

for _ in range(generation):
    algorithm.move()

fig = px.imshow(algorithm.graph, text_auto=True, color_continuous_scale="Viridis")

st.plotly_chart(fig)
