# import pygame module in this program
import pygame
import streamlit as st
from PIL import Image
import sys
import time
import numpy as np

# setup page as wide mode
st.set_page_config(layout="wide")

# Initialize Pygame
pygame.init()

# Set up display
width, height = 800, 600
#screenup = pygame.display.set_mode((width, height))
screen = pygame.Surface((width, height))       # mac has issue with display.set, but seems okay with surface
pygame.display.set_caption("Motion on a Ramp")

# Set up colors
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 255)

# setup three columns, left for input, middle right for up and down motion simulation
container = st.container()
col1, col2, col3 = st.columns([1, 2, 2])
g = 9.81   # g constant m/s^2
# square side length is 25
side = 25

#  input parameter and load a ramp diagram
with (col1):
    ramp_diagram = Image.open("ramp_diagram_dis_bmp.bmp")
    st.image(ramp_diagram, caption='Ramp Diagram')
    ramp_angle_degree = st.slider('Ramp angle θ (degree): ', 10, 89, 30)   # small angle run into some accuracy, due to use round 2 or 0.01 for accurancy
    ramp_angle_radian = round(ramp_angle_degree * 3.14 / 180, 2)
    Object_initial_distance = st.number_input('Object Initial Distance D_initial (m) :', 0, 300, 100)
    Static_Friction_Coefficient = st.number_input('Please enter value of $\\mu_s$ (static friction coefficient) : ', 0.00, 3.00, 0.45)
    Kinetic_Friction_Coefficient = st.number_input('Please enter value of $\\mu_k$ (kinetic friction coefficient) : ', 0.00, 2.00, 0.15)


    a_up = - (g * np.sin(ramp_angle_radian) + g * np.cos(ramp_angle_radian) * Kinetic_Friction_Coefficient)
    if np.tan(ramp_angle_radian) >= 5 / 7:   # the screen is 800 * 600, but the ramp is only use 700 * 500, leaving 50 on each side
        dis_from_initial_to_top = 500 / np.sin(ramp_angle_radian) - Object_initial_distance
    else:
        dis_from_initial_to_top = 700 / np.cos(ramp_angle_radian) - Object_initial_distance
    v_initial_max = round(np.sqrt(-2 * a_up * (dis_from_initial_to_top - side)), 1)   # max V to avoid object move out of the scren
    half_v_initial_max = round(v_initial_max / 2, 1)   # set intitial v = Vmax / 2
    Object_initial_up_speed = st.number_input('Object Initial Moving Up Speed V_initial (m/s) :', 0.0, v_initial_max,
                                             half_v_initial_max)

# Set up Ramp vertices
#1 is the ramp point, bottom right point
ramp_vertics_1_x = width - 50    # 750
ramp_vertics_1_y = height - 50   # 550

if ramp_angle_degree == 0:
    # 2 is the highest point
    ramp_vertics_2_x = 50
    ramp_vertics_2_y = ramp_vertics_1_y
    # 3 is the bottom left point
    ramp_vertics_3_x = ramp_vertics_2_x
    ramp_vertics_3_y = ramp_vertics_2_y
elif ramp_angle_degree == 90:
    # 2 is the highest point
    ramp_vertics_2_x = ramp_vertics_1_x
    ramp_vertics_2_y = 50
    #3 is the bottom left point
    ramp_vertics_3_x = ramp_vertics_2_x
    ramp_vertics_3_y = ramp_vertics_1_y
else:
    if np.tan(ramp_angle_radian) >= 5 / 7:
        # 2 is the highest point
        ramp_vertics_2_x = ramp_vertics_1_x - ((height - 100) / np.tan(ramp_angle_radian))
        ramp_vertics_2_y = 50
        #3 is the bottom left point
        ramp_vertics_3_x = ramp_vertics_2_x
        ramp_vertics_3_y = height - 50
    else:
        # 2 is the highest point
        ramp_vertics_2_x = 50
        ramp_vertics_2_y = ramp_vertics_1_y - 700 * np.tan(ramp_angle_radian)
        # 3 is the bottom left point
        ramp_vertics_3_x = ramp_vertics_2_x
        ramp_vertics_3_y = height - 50
# ramp four points position
ramp_vertices = [(ramp_vertics_1_x, ramp_vertics_1_y), (ramp_vertics_2_x, ramp_vertics_2_y),
                (ramp_vertics_3_x, ramp_vertics_3_y)]
# ramp or triangle color is green
triangle_color = green

# calculate move up distance, position array
a_up = - (g * np.sin(ramp_angle_radian) + g * np.cos(ramp_angle_radian) * Kinetic_Friction_Coefficient)
dis_up = - Object_initial_up_speed ** 2 / 2 / a_up
total_t_up = -Object_initial_up_speed / a_up

# animation is made of 50 frames of pictures
step = 25
t1 = np.linspace(0, total_t_up, step)
dis_at_t1 = Object_initial_up_speed * t1 + 1 / 2 * a_up * t1 ** 2
if ramp_angle_degree == 0:
    square_initial_1_x = ramp_vertics_1_x
    Object_initial_height = 0
else:
    square_initial_1_x = ramp_vertics_1_x - Object_initial_distance * np.cos(ramp_angle_radian)
    square_initial_1_y = ramp_vertics_1_y - Object_initial_distance * np.sin(ramp_angle_radian)



# object move up calculation
with col2:
    st.markdown("""
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
    moving_button = st.button('Run Simulation')
    st.success('After click the "Run Simulation", scroll down to the bottom of the screen to see animation')
    objectmove = st.empty()
    # draw the ramp and object with initial position
    square_vertics_1_x = square_initial_1_x - dis_at_t1[0] * np.cos(ramp_angle_radian)
    square_vertics_1_y = square_initial_1_y - dis_at_t1[0] * np.sin(ramp_angle_radian)
    square_vertics_2_x = square_vertics_1_x - side * np.cos(ramp_angle_radian)
    square_vertics_2_y = square_vertics_1_y - side * np.sin(ramp_angle_radian)
    square_vertics_3_x = square_vertics_1_x - side * 1.414 * np.cos(ramp_angle_radian + np.pi / 4)
    square_vertics_3_y = square_vertics_1_y - side * 1.414 * np.sin(ramp_angle_radian + np.pi / 4)
    square_vertics_4_x = square_vertics_1_x + side * np.sin(ramp_angle_radian)
    square_vertics_4_y = square_vertics_1_y - side * np.cos(ramp_angle_radian)

    square_vertices = [(square_vertics_1_x, square_vertics_1_y), (square_vertics_2_x, square_vertics_2_y),
                       (square_vertics_3_x, square_vertics_3_y), (square_vertics_4_x, square_vertics_4_y)]
    object_color = blue
    # Clear the screen
    screen.fill(white)
    # Draw the group line
    pygame.draw.line(screen, black, (0, 555), (800, 555), 10)
    # Draw the ramp
    pygame.draw.polygon(screen, triangle_color, ramp_vertices)
    # Draw the moving square object
    pygame.draw.polygon(screen, object_color, square_vertices)
    # Save Image
    pygame.image.save(screen, "motion_on_a_ramp.bmp")
    image = Image.open("motion_on_a_ramp.bmp")
    # load the image every 0.05 second to make a animation
    objectmove.image(image)



    if moving_button:
        # move up animation
        for i in range(step):
            # moving up
            # Set up square Object vertices
            square_vertics_1_x = square_initial_1_x - dis_at_t1[i] * np.cos(ramp_angle_radian)
            square_vertics_1_y = square_initial_1_y - dis_at_t1[i] * np.sin(ramp_angle_radian)
            square_vertics_2_x = square_vertics_1_x - side * np.cos(ramp_angle_radian)
            square_vertics_2_y = square_vertics_1_y - side * np.sin(ramp_angle_radian)
            square_vertics_3_x = square_vertics_1_x - side * 1.414 * np.cos(ramp_angle_radian + np.pi / 4)
            square_vertics_3_y = square_vertics_1_y - side * 1.414 * np.sin(ramp_angle_radian + np.pi / 4)
            square_vertics_4_x = square_vertics_1_x + side * np.sin(ramp_angle_radian)
            square_vertics_4_y = square_vertics_1_y - side * np.cos(ramp_angle_radian)
            if square_vertics_1_x <= 50 or square_vertics_1_y <= 50:
                exit()
            square_vertices = [(square_vertics_1_x, square_vertics_1_y), (square_vertics_2_x, square_vertics_2_y),
                              (square_vertics_3_x, square_vertics_3_y), (square_vertics_4_x, square_vertics_4_y)]
            object_color = blue
            # Clear the screen
            screen.fill(white)
            # Draw the group line
            pygame.draw.line(screen, black, (0, 555), (800, 555), 10)
            # Draw the ramp
            pygame.draw.polygon(screen, triangle_color, ramp_vertices)
            # Draw the moving square object
            pygame.draw.polygon(screen, object_color, square_vertices)


            # Save Image
            pygame.image.save(screen, "motion_on_a_ramp.bmp")
            image = Image.open("motion_on_a_ramp.bmp")
            # load the image every 0.05 second to make a animation
            objectmove.image(image)
            if i == 0:
                time.sleep(2)     # wait a little bit longer when loading the initial position image frame
            else:
                time.sleep(.25)    # time between each frame of image is 0.05 second

        # move down animation
        if np.sin(ramp_angle_radian) > np.cos(ramp_angle_radian) * Static_Friction_Coefficient:
            # object move down
            a_down = - (g * np.sin(ramp_angle_radian) - g * np.cos(ramp_angle_radian) * Kinetic_Friction_Coefficient)
            dis_from_top_to_bottom = -(square_vertics_1_x - square_initial_1_x) / np.cos(
                ramp_angle_radian) + Object_initial_distance
            time_from_top_to_bottom = np.sqrt(abs(2 * dis_from_top_to_bottom / a_down))
            t2 = np.linspace(0, time_from_top_to_bottom, step)
            dis_at_t2 = - 1 / 2 * a_down * t2 ** 2
            square_top_1_x = square_vertics_1_x
            square_top_1_y = square_vertics_1_y

            for i in range(step):
                # moving down
                # Set up square Object vertices
                square_vertics_1_x = square_top_1_x + dis_at_t2[i] * np.cos(ramp_angle_radian)
                square_vertics_1_y = square_top_1_y + dis_at_t2[i] * np.sin(ramp_angle_radian)
                square_vertics_2_x = square_vertics_1_x - side * np.cos(ramp_angle_radian)
                square_vertics_2_y = square_vertics_1_y - side * np.sin(ramp_angle_radian)
                square_vertics_3_x = square_vertics_1_x - side * 1.414 * np.cos(ramp_angle_radian + np.pi / 4)
                square_vertics_3_y = square_vertics_1_y - side * 1.414 * np.sin(ramp_angle_radian + np.pi / 4)
                square_vertics_4_x = square_vertics_1_x + side * np.sin(ramp_angle_radian)
                square_vertics_4_y = square_vertics_1_y - side * np.cos(ramp_angle_radian)

                square_vertices = [(square_vertics_1_x, square_vertics_1_y),
                                   (square_vertics_2_x, square_vertics_2_y),
                                   (square_vertics_3_x, square_vertics_3_y),
                                   (square_vertics_4_x, square_vertics_4_y)]
                object_color = blue
                # Clear the screen
                screen.fill(white)

                #Draw the group line
                pygame.draw.line(screen, black, (0, 555), (800, 555), 10)
                # Draw the ramp
                pygame.draw.polygon(screen, triangle_color, ramp_vertices)
                # Draw the moving square object
                pygame.draw.polygon(screen, object_color, square_vertices)
                # Save Image
                pygame.image.save(screen, "motion_on_a_ramp.bmp")
                image = Image.open("motion_on_a_ramp.bmp")
                # load the image every 0.05 second to make a animation
                objectmove.image(image)
                time.sleep(.25)  # time between each frame of image is 0.05 second



# object move down calculation
with col3:
    st.header('Object moving up with initial speed')
    st.text('Ramp angle = ' + str(ramp_angle_degree) + ' degrees')
    st.text('V_initial = ' + str(Object_initial_up_speed) + ' m/s')
    st.text('Object initial distance = ' + str(Object_initial_distance) + ' m')
    st.text('Kinetic friction coefficient = ' + str(Kinetic_Friction_Coefficient))
    st.text('Static friction coefficient = ' + str(Static_Friction_Coefficient))
    st.text('Moving up acceleration = ' + str(round(a_up, 2)) + ' m/s^2')
    st.text('Total moving up distance = ' + str(round(dis_up, 2)) + ' m')
    st.text('Total moving up time = ' + str(round(total_t_up, 2)) + ' seconds')

    a_down = - (g * np.sin(ramp_angle_radian) - g * np.cos(ramp_angle_radian) * Kinetic_Friction_Coefficient)
    dis_from_top_to_bottom = dis_up + Object_initial_distance
    time_from_top_to_bottom = np.sqrt(abs(2 * dis_from_top_to_bottom / a_down))
    st.header('Moving Down or Stuck ??? ')
    if np.sin(ramp_angle_radian) <= np.cos(ramp_angle_radian) * Static_Friction_Coefficient:
        st.subheader('Object stuck on top !!!  Because :')
        st.latex(r'\sin(\theta) <= cos(\theta)\mu_s')
    else:
        st.subheader('Object moving down because:')
        st.latex(r'\sin(\theta) > cos(\theta)\mu_s')
        st.text('V_down_initial = 0 m/s')
        st.text('Kinetic friction coefficient = ' + str(Kinetic_Friction_Coefficient))
        st.text('Static friction coefficient = ' + str(Static_Friction_Coefficient))
        st.text('Moving down acceleration = ' + str(round(a_down, 2)) + ' m/s^2')
        st.text('Total moving down distance = ' + str(round(dis_from_top_to_bottom, 2)) + ' m')
        st.text('Total moving down time = ' + str(round(time_from_top_to_bottom, 2)) + ' seconds')







