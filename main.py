import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


SKIP_ROWS = 60

def main():
    st.title("うお")
    st.write("うおうおうおうお")

    thermo_couple_file = st.file_uploader("熱電対データをアップロード", type="csv")
    data_file          = st.file_uploader("CSVファイルをアップロード", type="csv")

    if thermo_couple_file is not None and data_file is not None:
        df_thermo = pd.read_csv(thermo_couple_file, header=None)
        df_data   = pd.read_csv(data_file, skiprows=SKIP_ROWS, header=None, encoding="cp932")

        t      = pd.to_datetime(df_data.iloc[:, 1])
        data   = df_data.iloc[:, 3:43]
        labels = df_thermo.iloc[:, 1]

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(t, data)
        
        ax.legend(labels, bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()

        st.pyplot(fig)





if __name__ == "__main__":
    main()
