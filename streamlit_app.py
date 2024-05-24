import streamlit as st
import pickle
import numpy as np
import sklearn

# Set Streamlit page configuration
def set_page_configuration():
    st.set_page_config(
        page_title="Malaria Detection",
        page_icon="🦟",
        layout="wide",
        initial_sidebar_state="expanded",
    )   
    
# Sidebar
def sidebar():
    with st.sidebar:
        st.markdown("<h1 style='text-align: center;'>🦟 Detect Malaria</h1>", unsafe_allow_html=True)
        st.image("images.png", width=250)
        st.write("Our user-friendly tool analyzes your symptoms and provides a preliminary risk assessment, empowering you to seek medical attention if needed.")
        st.divider()
        st.header("Menu:")
        with st.form("initial_details"):
            name = st.text_input('**Name:**')
            patient_ID = st.text_input('**Patient ID:**')
            st.form_submit_button("Confirm", use_container_width=True)
    
# Function main
def main():
    set_page_configuration()
    sidebar()
    st.markdown("<h1 style='text-align: center;'>Malaria Detection</h1>", unsafe_allow_html=True)
    st.divider()
    values = None
    gender_map = {'': None, 'Female': 2, 'Male': 1}
    fever_intensity_map = {'': 0, 'High Grade': 3, 'Intermittent': 2, 'Low': 1}
    urinal_variation_map = {'': 0, 'Yes': 1, 'No': 0}
    pallor_map = {'': 0, 'Yes': 1, 'No': 0}
    
    with st.form("my_form"):
        left, right = st.columns(2)
        left, right = st.columns(2)
        with left:
            age = st.number_input("Enter your age:", min_value=0)
            gender = st.selectbox('Select your gender:', list(gender_map.keys()), key="gender")
            fever_intensity = st.selectbox('Fever intensity:', list(fever_intensity_map.keys()), key="fever_intensity")
            fever_days = st.number_input("Number of days with fever:", min_value=0)
            headache_days = st.number_input("Number of days with headache:", min_value=0)
            bodyache_days = st.number_input("Number of days with body ache:", min_value=0)
            vomiting_days = st.number_input("Number of days with vomiting:", min_value=0)
            
        with right:
            chills_days = st.number_input("Number of days with chills:", min_value=0)
            rigors_days = st.number_input("Number of days with rigors:", min_value=0)
            abdominal_discomfort_days = st.number_input("Number of days with abdominal discomfort:", min_value=0)
            cough_days = st.number_input("Number of days with cough:", min_value=0)
            urinal_variation = st.selectbox('Any changes in urination?', list(urinal_variation_map.keys()), key="urinal_variation")
            pallor = st.selectbox('Do you have pallor (paleness)?', list(pallor_map.keys()), key="pallor")
            temp = st.number_input("Current body temperature (°F):", min_value=0.0, step=0.1)           
        
        list_of_values = [
                fever_intensity_map[fever_intensity],
                fever_days,
                headache_days,
                bodyache_days,
                vomiting_days,
                abdominal_discomfort_days,
                cough_days,
                urinal_variation_map[urinal_variation],
                pallor_map[pallor],
                chills_days,
                rigors_days,
                temp,
                age,
                gender_map[gender]
            ]
        
        if st.form_submit_button("Confirm item(s) 🔒", type="primary", use_container_width=True):
            if any(value == '' for value in list_of_values):
                st.warning("Please select all options before confirming.")
            else:
                st.success("Form submitted successfully")
                values = list_of_values
            
            
    if values is not None:
        # Values for prediction
        independent_variables = np.array([values])
        model_from_pickle = pickle.load(open('extra_trees_model.pkl','rb'))
        prediction = model_from_pickle.predict(independent_variables)
        if prediction[0] == 0:
            st.info('''
                **Likely no Malaria**  
                The analysis indicates that the patient does not exhibit signs of malaria. 
                It is recommended to continue regular monitoring.
            ''')
        elif prediction[0] == 1:
            st.info('''
                **Likely there is malaria**  
                The analysis suggests the presence of malaria in the patient. 
                Immediate medical attention and further evaluation are advised to ensure proper management and treatment.
            ''')
        else:
            pass
           
            

if __name__ == "__main__":
    main()
