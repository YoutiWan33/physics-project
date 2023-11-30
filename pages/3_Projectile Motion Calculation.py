import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import streamlit.components.v1 as components
import matplotlib.animation as animation
import time

# ..................................Page Header Format Start.......................................................

# .....This page name /str ......
page_str = "Projectile Motion Simulation"                          # Input
subheader_str = "Abcefef"                                       # Input

# ...... set page title, page icon and wide screen.....
st.set_page_config(page_title=page_str, page_icon='tada:', layout="wide")

# .....Display this page's sidebar name...............
st.sidebar.header(page_str)

# .....Display this page's name...............
html_str1 = f"""
<style>
p.a {{
  font: bold 60px Arial;
}}
</style>
<p class="a">{page_str}</p>
"""
st.markdown(html_str1, unsafe_allow_html=True)

# .....Display this page's subheader...............
html_str2 = f"""
<style>
p.a {{
  font: bold 25px Arial;
}}
</style>
<p class="a">{subheader_str}</p>
"""
st.markdown(html_str2, unsafe_allow_html=True)

# ..............................Page Header Format End..........................................................

container = st.container()
col1, col2 = st.columns([1, 3])
with col1:
    V_int = st.number_input('Initial Velocity (m/s)', -1000000, 1000000, 30)
    H_int = st.number_input('Initial Height (m)', 0, 1000000, 10)
    Theta_int = st.slider('Initial Angle (degree)', 0, 90, 45)
    st.markdown(
        """
        <style>

        text {
            font-size: 5rem !important;
        }
        input {
            font-size: 2rem !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )



def update(frame):
    # for each frame, update the data stored on each artist.
    fly_t = t[:frame + 1]
    x_pos = x_dis[:frame + 1]
    y_pos = y_dis[:frame + 1]
    vertical_speed = v_vertical[:frame + 1]
    if frame == 0:
        time_str = '0.0'
    else:
        time_str = str(round(t[frame], 2))
    lab = 'Time:' + time_str + ' seconds'
    X_pos_text = 'X_Position: ' + str(round(x_dis[frame], 2)) + ' m'
    Y_pos_text = 'Y_Position: ' + str(round(y_dis[frame], 2)) + ' m'
    graph.set_data(x_dis[:frame + 1], y_dis[:frame + 1])
    L.get_texts()[0].set_text(lab + '\n' + X_pos_text + '\n' + Y_pos_text)  # Update label each at frame
    return graph



with col2:
    m = st.markdown("""
    <style>
    div.stButton > button:first-child {
        background-color: #0099ff;
        color:#ffffff;
    }
    div.stButton > button:hover {
        background-color: #00ff00;
        color:#ff0000;
        }
    </style>""", unsafe_allow_html=True)

    button = st.button("Run Simulation for Vertical Distance (m) Vs. Horizontal Distance (m)")
    st.success('It may take about 10 seconds to run the simulation')

    if button:
        g = 9.81  # m / s^2
        Theta_rad_int = Theta_int * np.pi / 180
        V_x_int = V_int * np.cos(Theta_rad_int)
        V_y_int = V_int * np.sin(Theta_rad_int)
        TimefromInttoApex = V_y_int / g
        DisfromInttoApex = V_y_int * V_y_int / 2 / g
        DisfromApextoGround = DisfromInttoApex + H_int
        TimefromApextoGround = np.sqrt(2 / g * DisfromApextoGround)
        TotalTime = TimefromInttoApex + TimefromApextoGround
        TotalHorizontalDistance = V_x_int * TotalTime

        fig, ax = plt.subplots()

        frame_par = 40
        t = np.linspace(0, TotalTime, frame_par)
        y_dis = H_int + V_y_int * t - 1 / 2 * g * t * t
        x_dis = V_x_int * t
        v_vertical = V_y_int - g * t

        ax.set(xlim=[0, int(1.1 * TotalHorizontalDistance)], ylim=[0, int(1.35 * DisfromApextoGround)], xlabel='X [m]',
               ylabel='Y [m]')
        plt.title('Vertical Distance vs. Horizontal Distance')

        graph, = plt.plot([], [], color="gold", lw=1, marker='o', markersize=3, label='Time: 0 second')
        L = plt.legend(loc=1)  # Define legend objects


        st.write('Time from Initial to Highest  = ', round(TimefromInttoApex, 2), 'Second')
        st.write('Time from Highest to Ground = ', round(TimefromApextoGround, 2), 'Second')
        st.write('Total Time in the Air = ', round(TotalTime, 2), 'Second')



        ani = animation.FuncAnimation(fig=fig, func=update, frames=frame_par, interval=15)
        # ...... ani.save(filename="C:/Users/xiongyi/PycharmProjects/Webpage\pages/html_example.html", writer="html")
        # convert animation to html and display
        components.html(ani.to_jshtml(), height=1000)






