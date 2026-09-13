import math
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def show(config):
    """ グラフの描画 """

    load_config   = config.get("load",   {})
    legend_config = config.get("legend", {})

    graph_file   = load_config  .get("file", None)
    has_header   = load_config  .get("has_header", True)
    skip_rows    = load_config  .get("skip_rows", 0)
    skip_cols    = load_config  .get("skip_cols", 0)
    legend_style = legend_config.get("style", {})

    fig = go.Figure()
    num_traces = 0

    if graph_file is not None:
        header_option = 0 if has_header else None
    
        graph_data = pd.read_csv(
            graph_file, 
            header=header_option, 
            skiprows=skip_rows
        ).iloc[:, skip_cols:]

        x_data      = graph_data.iloc[:, 0]  if graph_data.shape[1] > 1 else graph_data.index
        target_cols = graph_data.columns[1:] if graph_data.shape[1] > 1 else graph_data.columns
        num_traces  = len(target_cols)

        for i, col in enumerate(target_cols):
            col_key = str(col) if has_header else f"data {i+1}"
            
            style = legend_style.get(col_key, {})
            
            label         = style.get("label", col_key)
            is_visible    = style.get("visibility", True)
            color         = style.get("color", "#1B365D")
            width         = style.get("width", 2)
            linestyle     = style.get("linestyle", "solid")
            marker_symbol = style.get("marker", "none")

            has_marker    = marker_symbol != "none"
            mode          = "lines+markers" if has_marker else "lines"
            marker_symbol = marker_symbol   if has_marker else "circle"

            trace_args = dict(
                x=x_data,
                y=graph_data[col],
                name=label,
                visible=is_visible,
                mode=mode,
                line=dict(color=color, width=width, dash=linestyle),
                marker=dict(symbol=marker_symbol, color=color, size=6)
            )

            fig.add_trace(go.Scatter(**trace_args))

    _set_layout_font(fig, config)
    _set_title(fig, config, num_traces)
    _set_x_axis(fig, config)
    _set_y_axis(fig, config)

    aspect_mode = config.get("region", {}).get("aspect_mode", "Auto")
    width       = "content" if aspect_mode == "Square" else "stretch"

    with open("js/load-mathjax.js", "r") as f:
        js = f.read()
        st.iframe(f"<script>{js}</script>", height=10)

    st.plotly_chart(fig, width=width, config={"scrollZoom": False})


def _set_layout_font(fig, config):
    """ 全体レイアウトとフォント設定 """

    region_config   = config.get("region", {})
    legend_config   = config.get("legend", {})
    location_config = config.get("location", {})

    aspect_mode = region_config.get("aspect_mode", "Auto")
    font_family = region_config.get("font_family", "Times New Roman, serif")

    show_legend = legend_config.get("show", True)

    args = dict(
        template="simple_white",
        font=dict(
            family=font_family,
            size=14,
            color="black"
        ),
        height=800,
        showlegend=show_legend
    )

    if show_legend:
        legend_font_size = legend_config.get("size", 12)

        preset = location_config.get("preset", "外・上")
        cols   = location_config.get("cols", 5)

        if   preset == "外・上":
            legend_dict = dict(x=0.5, y=1.03, xanchor="center", yanchor="bottom", orientation="h")
        elif preset == "外・下":
            legend_dict = dict(x=0.5, y=-0.03, xanchor="center", yanchor="top", orientation="h")
        elif preset == "外・右":
            legend_dict = dict(x=1.03, y=0.5, xanchor="left", yanchor="middle", orientation="v")
        elif preset == "外・左":
            legend_dict = dict(x=-0.03, y=0.5, xanchor="right", yanchor="middle", orientation="v")
        elif preset == "内・右上":
            legend_dict = dict(x=0.98, y=0.98, xanchor="right", yanchor="top", orientation="v")
        elif preset == "内・左上":
            legend_dict = dict(x=0.02, y=0.98, xanchor="left", yanchor="top", orientation="v")
        elif preset == "内・右下":
            legend_dict = dict(x=0.98, y=0.02, xanchor="right", yanchor="middle", orientation="v")
        else: # 内・右下
            legend_dict = dict(x=0.02, y=0.02, xanchor="left", yanchor="middle", orientation="v")

        if legend_dict.get("orientation") == "h":
            legend_dict["entrywidth"] = 1.0 / max(1, cols)
            legend_dict["entrywidthmode"] = "fraction"

        legend_dict.update(dict(
            font=dict(size=legend_font_size),
            bgcolor="rgba(255, 255, 255, 0.8)",
            bordercolor="black",
            borderwidth=1.0
        ))

        args["legend"] = legend_dict
        
    if aspect_mode == "Square":
        args["width"]  = 800
        args["height"] = 800
        fig.update_yaxes(scaleanchor=None)

    elif aspect_mode == "Equal":
        args["height"] = 800
        fig.update_yaxes(scaleanchor="x", scaleratio=1)

    fig.update_layout(**args)


def _set_title(fig, config, num_traces):
    """ タイトルと動的トップマージン・正方形アスペクト比の補正 """

    title_config    = config.get("title", {})
    legend_config   = config.get("lenged", {})
    location_config = config.get("location", {})
    region_config   = config.get("region", {})

    graph_title = title_config.get("label", "")
    title_size  = title_config.get("size", 20)
    preset      = location_config.get("preset", "外・上")
    cols        = location_config.get("cols", 5)
    aspect_mode = region_config.get("aspect_mode", "Auto")
    show_legend = legend_config.get("show", True)

    left_margin   = 60
    right_margin  = 40
    bottom_margin = 50

    title_height  = int(title_size * 1.5) if graph_title else 0
    legend_height = 0

    if show_legend and preset == "外・上" and num_traces > 0:
        rows = math.ceil(num_traces / max(1, cols))
        legend_height = rows * 22 + 10

    top_margin = max(60, title_height + legend_height)

    layout_update = dict(
        title=dict(
            text=graph_title,
            x=0.5,
            y=0.98,
            yref="container",
            xanchor="center",
            yanchor="top",
            font=dict(size=title_size, color="black")
        ),
        margin=dict(t=top_margin, b=bottom_margin, l=left_margin, r=right_margin)
    )

    if aspect_mode == "Square":
        target_plot_size = 800
        
        total_width  = target_plot_size + left_margin + right_margin
        total_height = target_plot_size + top_margin + bottom_margin

        layout_update["width"]  = total_width
        layout_update["height"] = total_height

    fig.update_layout(**layout_update)


def _set_x_axis(fig, config):
    """ X軸の設定 """

    axis_config  = config.get("axis", {}).get("x", {})
    label        = axis_config.get("label", "")
    label_size   = axis_config.get("label_size", 10)
    tick_size    = axis_config.get("tick_size", 8)
    show_grid    = axis_config.get("show_grid", True)
    is_log       = axis_config.get("is_log", False)
    autorange    = axis_config.get("autorange", True)
    ax_range     = axis_config.get("range", None)

    args = dict(
        title=dict(
            text=label,
            font=dict(size=label_size, color="black")
        ),
        tickfont=dict(size=tick_size, color="black"),
        type="log" if is_log else "linear",
        showline=True,
        linewidth=1.2,
        linecolor="black",
        mirror=True,
        ticks="outside",
        tickwidth=1.2,
        tickcolor="black",
        showgrid=show_grid,
        gridcolor="#E5E5E5",
        gridwidth=0.5
    )

    if is_log:
        args["exponentformat"] = "power"
        args["showexponent"]   = "all"

    if not autorange and ax_range is not None:
        args["range"] = ax_range

    fig.update_xaxes(**args)


def _set_y_axis(fig, config):
    """ Y軸の設定 """

    axis_config  = config.get("axis", {}).get("y", {})
    label        = axis_config.get("label", "")
    label_size   = axis_config.get("label_size", 10)
    tick_size    = axis_config.get("tick_size", 8)
    show_grid    = axis_config.get("show_grid", True)
    is_log       = axis_config.get("is_log", False)
    autorange    = axis_config.get("autorange", True)
    ax_range     = axis_config.get("range", None)

    args = dict(
        title=dict(
            text=label,
            font=dict(size=label_size, color="black")
        ),
        tickfont=dict(size=tick_size, color="black"),
        type="log" if is_log else "linear",
        showline=True,
        linewidth=1.2,
        linecolor="black",
        mirror=True,
        ticks="outside",
        tickwidth=1.2,
        tickcolor="black",
        showgrid=show_grid,
        gridcolor="#E5E5E5",
        gridwidth=0.5
    )

    if is_log:
        args["exponentformat"] = "power"
        args["showexponent"]   = "all"

    if not autorange and ax_range is not None:
        args["range"] = ax_range

    fig.update_yaxes(**args)