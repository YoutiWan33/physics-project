import streamlit as st
import matplotlib.pyplot as plt
import math
import numpy as np
from PIL import Image

st.set_page_config(page_title='Ramp', page_icon='tada:', layout="wide")

def up_calculate_motion(time):
    velocity = vi - (9.81*math.sin(theta)+9.81*math.cos(theta)*uk) * time
    position = h/math.sin(theta) + vi*time + 0.5 * -(9.81*math.sin(theta)+9.81*math.cos(theta)*uk) * (time**2)
    return position,velocity

def down_calculate_motion(time):
    velocity = 0 - (9.81*math.sin(theta)-9.81*math.cos(theta)*uk) * (time-total_time_up)
    position = total_distance - 0.5 * (9.81*math.sin(theta)-9.81*math.cos(theta)*uk) * (time**2)
    return position,velocity

# three columns - Inputs, Upwards, Downwards (if not stuck)

input_column, up_column, down_column = st.columns([1, 2, 2])
# input
with input_column:
    ramp_diagram = Image.open("ramp_diagram_dis_bmp.bmp")
    st.image(ramp_diagram, caption='Ramp Diagram')
    g = 9.81
    pi = 3.1415
    uk = input_column.number_input('Please enter value of $\\mu_k$ (kinetic friction coefficient) : ', 0.00, 1000.00, 0.10)
    us = input_column.number_input('Please enter value of $\\mu_s$ (static friction coefficient) : ', 0.00, 1000.00, 0.30)
    vi = input_column.number_input('Please enter value of $v_i$ (m/s) : ', 0, 1000000000, 10)
    theta_degrees = input_column.slider('Please enter value of $\\theta$ (in degrees) : ', 0, 90, 45)
    h = input_column.number_input('Please enter value of initial distance (m) : ', 0, 1000000000, 10)

    theta = theta_degrees/180*pi
    a_up = -(g*math.sin(theta)+g*math.cos(theta)*uk)
    a_down = -(g*math.sin(theta)-g*math.cos(theta)*uk)
    total_distance = -(vi ** 2) / (2 * a_up)
    total_distance_down = total_distance + h
    total_time_up = -vi / a_up
    total_time_down = np.sqrt(2 * total_distance_down/-a_down)
    # st.write(total_time_up,total_distance)
    # solve for vf
    vf = total_time_down * a_down
    # load a ramp diagram
    # ramp_diagram = Image.open("ramp_diagram.bmp")
    # st.image(ramp_diagram, caption='Ramp Diagram')

# upwards travel - time bar, x & y position on ramp, speed, equation
with up_column:
    st.title("Travel Up")
    st.text('Object moving up')
    t = np.linspace(0, total_time_up, 300)
    dist_at_t_up = vi * t + (1 / 2) * (a_up) * (t ** 2) + h
    velocity_at_t_up = vi + a_up * t
    st.text('Moving up acceleration = ' + str(round(a_up, 2)) + ' m/s^2')
    st.text('Moving up initial velocity = ' + str(round(vi, 2)) + ' m/s')
    st.text('Moving up final velocity = 0 m/s')
    st.text('Total moving up time = ' + str(round(total_time_up, 2)) + ' seconds')
    st.text('total moving up distance= ' + str(round(total_distance, 2)) + ' m')
    #graph distance

    fig_up = plt.figure(1)
    plt.plot(t, dist_at_t_up)
    plt.xlabel('Time (sec)')
    plt.ylabel('Distance (m)')
    plt.xlim(0,round(total_time_up, 2))
    plt.ylim(h, round(total_distance + h, 2))
    plt.title('Distance (from the bottom of the ramp to object) Vs Time')
    st.write(fig_up)

    #graph velocity

    fig_up_2 = plt.figure(2)
    plt.plot(t, velocity_at_t_up)
    plt.xlabel('Time (sec)')
    plt.ylabel('Velocity (m/s)')
    plt.xlim(0, round(total_time_up, 2))
    plt.ylim(0, round(vi, 2))
    plt.title('Velocity Vs Time')
    st.write(fig_up_2)


# # downwards travel - stuck?, x & y position on ramp, speed, equation
with down_column:
    st.title("Travel Down ???")

    t = np.linspace(0, total_time_down, 300)
    dist_at_t_down = dist_at_t_up[-1] - (1 / 2) * (-a_down) * (t ** 2)
    velocity_at_t_down = a_down * t

    # stuck?
    if g * np.sin(theta) > us * g * np.cos(theta):
        st.text("Object NOT Stuck at Top of Ramp")
        # graph distance with respect to time
        st.text('Moving down acceleration = ' + str(round(a_down, 2)) + ' m/s^2')
        st.text('Moving down initial velocity = 0 m/s')
        st.text('Moving down finial velocity = ' + str(round(velocity_at_t_down[-1],2)) + ' m/s')
        st.text('Total moving down time = ' + str(round(total_time_down, 2)) + ' seconds')
        st.text('total moving down distance= ' + str(round(total_distance_down, 2)) + ' m')
        fig_down_distance = plt.figure(3)
        plt.plot(t, dist_at_t_down)
        plt.xlabel('Time (sec)')
        plt.ylabel('Distance (m)')
        plt.xlim(0, round(total_time_down, 2))
        plt.ylim(0, round(total_distance_down, 2))
        plt.title('Distance (from the bottom of the ramp to object) Vs Time')
        st.write(fig_down_distance)
        # graph velocity with respect to time
        fig_down_velocity = plt.figure(4)

        plt.plot(t, velocity_at_t_down)
        plt.xlabel('Time (sec)')
        plt.ylabel('Distance (m)')
        plt.xlim(0, round(total_time_down, 2))
        plt.ylim(0, round(vf, 2))
        plt.title('Velocity Vs Time')
        st.write(fig_down_velocity)

        # set x-axis as ramp and y-axis as normal y-axis
    else:
        st.text("Object Stuck at Top of Ramp")

# Manage font, organization, etc
input_column.markdown(
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

up_column.markdown(
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

down_column.markdown(
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
