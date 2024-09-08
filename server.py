import streamlit as st
import pandas as pd

# Set the path to your CSV file
FILE_PATH = 'uploaded.csv'


def load_data(file_path):
    df = pd.read_csv(file_path)

    df['Meeting Host Time'] = pd.to_datetime(df['Meeting Host Time'], errors='coerce')

    df = df.iloc[::-1]
    df['Meeting ID'] = df['Meeting ID'].apply(str)

    # # Reset the index and start from 1
    # df.reset_index(drop=True, inplace=True)
    df.index = df.index + 1  # Start index from 1

    return df


def main():
    st.set_page_config(
        page_title='Zoom To Vimeo',
        layout='wide',
        page_icon='🔥'
    )

    st.title('Zoom to Vimeo Video Uploaded Records')
    data = load_data(FILE_PATH)
    st.write("Data Preview:")
    st.dataframe(data)


if __name__ == "__main__":
    main()
