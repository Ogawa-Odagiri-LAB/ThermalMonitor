import streamlit as st

def init_page(version):
    """ ページの初期化 """
    _init_page_size()
    _init_header(version)
    _init_footer()
    _init_padding()
    _init_css_class()


def no_copy_content(content):
    """ コピー不可文字 """
    return st.markdown(f'<p class="no-copy">{content}</p>', unsafe_allow_html=True)


def _init_page_size():
    """ ページサイズを規定 """
    st.set_page_config(layout="wide")


def _init_header(version):
    """ ヘッダーにタイトル・バージョンを記載 """
    css_code = """
        <style>
        [data-testid="stHeader"]::before {
            content: "Thermal Monitor vVERSION_STR";
            position: absolute;
            left: 20px;
            top: 18px;
            font-weight: bold;
            font-size: 22px;
            color: #666;
        }
        </style>
    """.replace("VERSION_STR", str(version))
    
    st.markdown(css_code, unsafe_allow_html=True)


def _init_footer():
    """ フッターを非表示 """
    st.markdown("""
        <style>
        footer, [data-testid="stFooter"] {
            display: none !important;
        }
        </style>
    """, unsafe_allow_html=True)


def _init_padding():
    """ paddingの設定 """
    st.markdown("""
        <style>
        .block-container {
            padding-top: 2.5rem !important;
        }
        </style>
    """, unsafe_allow_html=True)


def _init_css_class():
    """ cssクラスの定義 """
    st.markdown("""
        <style>
        .no-copy-text {
            display: inline-block;
            -webkit-user-select: none !important;
            -moz-user-select: none !important;
            -ms-user-select: none !important;
            user-select: none !important;
        }
        .no-copy-text::before {
            content: attr(data-text);
        }

        [data-testid="stExpander"] summary {
            -webkit-user-select: none !important;
            -moz-user-select: none !important;
            -ms-user-select: none !important;
            user-select: none !important;
        }
        </style>
    """, unsafe_allow_html=True)


