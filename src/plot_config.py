import streamlit as st
import pandas as pd


ASPECT_LISTS = ["Auto", "Square", "Equal"]
FONT_LISTS   = ["Times New Roman, serif", "Arial"]

LINE_LABELS   = ["solid", "dash", "dot", "dashdot"]
MARKER_LABELS = ["none", "circle", "square", "diamond", "triangle-up", "triangle-down", "cross", "x"]

LEGENDS_LOCATIONS = ["外・上", "外・下", "外・右", "外・左", "内・右上", "内・左上", "内・右下", "内・左下", "カスタム"]


def show_contents():
    """ 設定の描画 """

    load_config     = _show_load_config()
    region_config   = _show_region_config()
    title_config    = _show_design_config()
    legend_config   = _show_legend_config(load_config)
    axis_config     = _show_axis_config()
    location_config = _show_location_config()
    note_config     = _show_note_config()

    return {
        "load"    : load_config,
        "region"  : region_config,
        "title"   : title_config,
        "legend"  : legend_config,
        "axis"    : axis_config,
        "location": location_config,
        "note"    : note_config
    }


def _show_load_config():
    """ データ読み込み設定 """

    with st.expander("データ読込"):
        data_file  = st.file_uploader("CSVファイルをアップロード", type="csv")
        has_header = st.toggle("1行目をヘッダとして使用", value=True)
        skip_rows  = st.number_input("読み飛ばす行数", min_value=0, value=0)
        skip_cols  = st.number_input("読み飛ばす列数", min_value=0, value=0)

    return {
        "file"      : data_file,
        "has_header": has_header,
        "skip_rows" : skip_rows,
        "skip_cols" : skip_cols
    }


def _show_region_config():
    """ グラフ領域の設定 """

    with st.expander("グラフ領域"):
        aspect_mode = st.selectbox("アスペクト比", ASPECT_LISTS, key="aspect_mode_select")
        font_family = st.selectbox("フォント", FONT_LISTS, key="font_familiy")

    return {
        "aspect_mode": aspect_mode,
        "font_family": font_family
    }


def _show_design_config():
    """ デザイン設定 """

    with st.expander("タイトル"):
        col1, col2 = st.columns([3, 1])
        with col1:
            label = st.text_input("タイトル", key="title_label_input")
        with col2:
            size  = st.number_input("文字サイズ", min_value=10, max_value=50, value=20, key="title_size_input")

    return {
        "label": label,
        "size" : size,
    }


def _show_legend_config(load_config):
    """ 凡例設定 """

    with st.expander("凡例"):

        col_show, col_font = st.columns(2)
        with col_show:
            show_legend = st.toggle("凡例を表示する", value=True, key="show_legend_check")
        with col_font:
            legend_font_size = st.number_input("文字サイズ", min_value=6, max_value=30, value=12, step=1, key="legend_font_size_input")

        st.divider()

        data_file  = load_config.get("file")
        has_header = load_config.get("has_header", True)
        skip_rows  = load_config.get("skip_rows", 0)
        skip_cols  = load_config.get("skip_cols", 0)

        legend_keys = []
        if data_file is not None:
            try:
                header_option = 0 if has_header else None
                df_preview = pd.read_csv(
                    data_file, 
                    header=header_option, 
                    skiprows=skip_rows, 
                    nrows=1
                ).iloc[:, skip_cols:]
                data_file.seek(0)

                if has_header:
                    legend_keys = [str(col) for col in df_preview.columns[1:]]
                else:
                    legend_keys = [f"data {i+1}" for i in range(len(df_preview.columns)-1)]

            except Exception:
                legend_keys = []

        if "legend_style" not in st.session_state:
            st.session_state.legend_style = {}

        # visibility一括制御
        button_all_visible, button_all_invisible, _ = st.columns([1.7, 1.7, 5])
        if button_all_visible.button("すべて表示", use_container_width=True):
            for key in legend_keys:
                st.session_state[f"visibility_{key}"] = True

        if button_all_invisible.button("すべて非表示", use_container_width=True):
            for key in legend_keys:
                st.session_state[f"visibility_{key}"] = False

        default_colors = ["#1B365D", "#8B0000", "#008080", "#E67E22", "#2E4053", "#8E44AD"]

        # ヘッダの描画
        col_ratio = [2.4, 0.6, 0.8, 1.0, 1.5, 1.7]
        h_name, h_visibility, h_color, h_width, h_line, h_mark = st.columns(col_ratio)
        h_name       .caption("凡例名")
        h_visibility .caption("表示")
        h_color      .caption("色")
        h_width      .caption("太さ")
        h_line       .caption("線種")
        h_mark       .caption("マーカー")

        # 初期化・描画
        for i, key in enumerate(legend_keys):
            if key not in st.session_state.legend_style:
                st.session_state.legend_style[key] = {
                    "label"     : key,
                    "visibility": True,
                    "color"     : default_colors[i % len(default_colors)],
                    "width"     : 2.0,
                    "linestyle" : "solid",
                    "marker"    : "none"
                }

            current = st.session_state.legend_style[key]
            col_name, col_visibility, col_color, col_width, col_linestyle, col_mark = st.columns(col_ratio, vertical_alignment="center")
            
            with col_name:
                label = st.text_input("名前", value=current["label"], key=f"name_{key}", label_visibility="collapsed")
            with col_visibility:
                is_visible = st.toggle("表示", value=current["visibility"], key=f"visibility_{key}", label_visibility="collapsed")
            with col_color:
                color = st.color_picker("色", value=current["color"], key=f"color_{key}", label_visibility="collapsed")
            with col_width:
                width = st.number_input("太さ", value=current["width"], key=f"width_{key}", label_visibility="collapsed")
            with col_linestyle:
                selected_line_label   = st.selectbox("線種", LINE_LABELS, key=f"linestyle_{key}", label_visibility="collapsed")
            with col_mark:
                selected_marker_label = st.selectbox("マーカー", MARKER_LABELS, key=f"marker_{key}", label_visibility="collapsed")
                
            st.session_state.legend_style[key] = {
                "label"     : label,
                "visibility": is_visible,
                "color"     : color,
                "width"     : width,
                "linestyle" : selected_line_label,
                "marker"    : selected_marker_label
            }

    return {
        "show" : show_legend,
        "size" : legend_font_size,
        "style": st.session_state.legend_style
    }


def _show_axis_config():
    """ 軸設定 """

    with st.expander("軸"):
        st.markdown("**X軸**")
        col_x1, col_x2, col_x3 = st.columns([2.5, 1.2, 2])
        with col_x1:
            x_label = st.text_input("軸ラベル", value="", key="x_label_input")
            x_grid  = st.toggle("グリッド線を表示", value=True, key="x_grid_toggle")
            x_log   = st.toggle("対数スケール", value=False, key="x_log_toggle")
        with col_x2:
            x_label_size = st.number_input("ラベルサイズ", min_value=8, max_value=40, value=20, key="xlabel_size_input")
            x_tick_size  = st.number_input("目盛サイズ", min_value=8, max_value=40, value=14, key="xtick_size_input")
        with col_x3:
            x_auto  = st.toggle("範囲を自動設定", value=True, key="x_auto_toggle")
            if not x_auto:
                x_min = st.number_input("最小値", value=0.0, key="x_min_input")
                x_max = st.number_input("最大値", value=100.0, key="x_max_input")
            else:
                x_min, x_max = None, None

        st.divider()

        st.markdown("**Y軸**")
        col_y1, col_y2, col_y3 = st.columns([2.5, 1.2, 2])
        with col_y1:
            y_label = st.text_input("タイトル", value="", key="y_label_input")
            y_grid  = st.toggle("グリッド線を表示", value=True, key="y_grid_toggle")
            y_log   = st.toggle("対数スケール", value=False, key="y_log_toggle")
        with col_y2:
            y_label_size  = st.number_input("ラベルサイズ", min_value=8, max_value=40, value=20, key="ylabel_size_input")
            y_tick_size   = st.number_input("目盛サイズ", min_value=8, max_value=40, value=14, key="ytick_size_input")
        with col_y3:
            y_auto  = st.toggle("範囲を自動設定", value=True, key="y_auto_toggle")
            if not y_auto:
                y_min = st.number_input("最小値", value=0.0, key="y_min_input")
                y_max = st.number_input("最大値", value=100.0, key="y_max_input")
            else:
                y_min, y_max = None, None

    return {
        "x": {
            "label"     : x_label,
            "label_size": x_label_size,
            "tick_size" : x_tick_size,
            "show_grid" : x_grid,
            "is_log"    : x_log,
            "autorange" : x_auto,
            "range"     : [x_min, x_max] if not x_auto else None
        },
        "y": {
            "label"     : y_label,
            "label_size": y_label_size,
            "tick_size" : y_tick_size,
            "show_grid" : y_grid,
            "is_log"    : y_log,
            "autorange" : y_auto,
            "range"     : [y_min, y_max] if not y_auto else None
        }
    }


def _show_location_config():
    """ 配置設定 """

    with st.expander("配置"):
        col_pos1, col_pos2 = st.columns(2)
        with col_pos1:
            legend_preset = st.selectbox(
                "凡例位置",
                LEGENDS_LOCATIONS,
                key="legend_preset_select"
            )

            if legend_preset == "カスタム":
                col_c1, col_c2 = st.columns(2)
                with col_c1:
                    custom_x = st.number_input("X位置 (0=左端, 1=右端)", value=1.02, key="legend_custom_x")
                with col_c2:
                    custom_y = st.number_input("Y位置 (0=下端, 1=上端)", value=1.00, key="legend_custom_y")
            else:
                custom_x, custom_y = None, None

        with col_pos2:
            if legend_preset == "外・上" or legend_preset == "外・下":
                legend_cols = st.number_input(
                    "一列あたりの凡例数", 
                    min_value=1, max_value=10, value=5, step=1, 
                    key="legend_cols_input"
                )
            else:
                legend_cols = 0

        return {
            "preset"     : legend_preset,
            "cols"       : legend_cols,
            "x"          : custom_x,
            "y"          : custom_y
        }


def _show_note_config():
    """ メモ設定 """

    with st.expander("メモ"):
        content = st.text_area("Note")  

    return {
        "content": content
    }
