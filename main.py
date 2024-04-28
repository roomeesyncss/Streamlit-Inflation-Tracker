import streamlit as st
import pandas as pd
import plotly.express as px


data = pd.read_csv("inflation.csv", header=0)

data = data.melt(id_vars=["Series Name", "Series Code", "Country Name", "Country Code"], var_name="Year", value_name="Inflation Rate")
data["Year"] = data["Year"].str.extract(r'(\d+)', expand=False).astype(int)  # Extract year from column names

st.set_page_config(page_title="Inflation Rate Visualization", layout="wide")
st.title("Inflation Rate Visualization")

st.sidebar.header("Select Countries Please")
selected_countries = st.sidebar.multiselect("Choose countries", data["Country Name"].unique(), default=["India", "China"])

st.sidebar.header("Plot Settings")
type = st.sidebar.selectbox("Select Plot Type", ["Line Plot", "Area Plot"])
plot_height = st.sidebar.slider("Plot Height", 300, 800, 500)
show_legend = st.sidebar.checkbox("Show Legend", True)
legend_position = st.sidebar.selectbox("Legend Position", ["top-left", "top-right", "bottom-left", "bottom-right"])

filtered_data = data[data["Country Name"].isin(selected_countries)]


if type == "Line Plot":
    plot_func = px.line
else:
    plot_func = px.area

fig = plot_func(filtered_data, x="Year", y="Inflation Rate", color="Country Name", height=plot_height)
fig.update_layout(
    title="Inflation Rate Over Time",
    xaxis_title="Year",
    yaxis_title="Inflation Rate (%)",
    showlegend=show_legend,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)


if legend_position == "top-left":
    fig.update_layout(legend=dict(orientation="h", yanchor="top", y=0.99, xanchor="left", x=0.01))
elif legend_position == "top-right":
    fig.update_layout(legend=dict(orientation="h", yanchor="top", y=0.99, xanchor="right", x=0.99))
elif legend_position == "bottom-left":
    fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=0.01, xanchor="left", x=0.01))
else:
    fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=0.01, xanchor="right", x=0.99))

# Display the plot
st.plotly_chart(fig, use_container_width=True)

# Display the data table
st.header("Data Table")
st.write(filtered_data)