import streamlit as st
import src.style as style
import src.plot_config as plot_config
import src.plot as plot


CONTAINER_HEIGHT = 700

VERSION = "1.0.0"

style.init_page(version=VERSION)
col_left, col_middle, col_right = st.columns([5.25, 0.5, 4.25])


def main():

    with col_right:
        st.subheader("グラフ設定")
        with st.container(height=CONTAINER_HEIGHT):
            config = plot_config.show_contents()

    with col_left:
        plot.show(config)


if __name__ == "__main__":
    main()