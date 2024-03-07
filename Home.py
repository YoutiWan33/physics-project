
import streamlit as st

# .... set webpage a wide display .....
st.set_page_config(page_title='Home', page_icon='tada:', layout="wide")
# ...... sidebar success .......
st.sidebar.success("Select a simulation above.")

#..... Header .......
st.header('Welcome to Youti\'s Physics Website :wave:', divider='rainbow')
st.markdown(
    """
    # Hello, please read below: 
    ### 👈 On the sidebar, there are various different explorations into fundamental physics principles. 
    ### Each exploration will include a description of the physics involved and a simulation. 
    ### Feel free to play around with various input variables within the simulations.
    
    # Who am I?
    ### I am currently a Junior (IV-Form) at [The Lawrenceville School](https://www.lawrenceville.org) in Lawrenceville, NJ.
    ### I’m a physics student --- currently taking Honors Physics / Mechanics and Theory with Dr. Voss. I look forward to studying physics in college.
    ### I'm a wrestler --- 3-year varsity wrestler & 3x National Prep Qualifier. More importantly, I'm a student of the sport, seeking to fully understand moves rather than just doing them.
    
    # Additional information (for coding nerds):
    ### This website is made with Streamlit and Python. 
    """)
