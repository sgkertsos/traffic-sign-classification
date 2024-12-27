import streamlit as st
from predict_service_functions import predict_traffic_sign

def main():
    # Set browser tab title
    st.set_page_config(page_title="Traffic sign classification app", menu_items=None, page_icon="random")
    
    # Set page title
    st.markdown('### Traffic sign classification app')

    # Select a file to upload to the classification web service
    uploaded_file = st.file_uploader("Choose a file", ['jpg', 'png'])
    if uploaded_file is not None:
        response = predict_traffic_sign(uploaded_file)
        st.write(f"Class Index is {response['class_index']} and class name is {response['class_name']}")

if __name__ == "__main__":
    main()