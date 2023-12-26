import streamlit as st
# from pymata4 import pymata4
import time
import pygame
from PIL import Image

st.set_page_config(page_title="Physics behind the wrestling", page_icon='tada:', layout="wide")
st.header('Physics Behind the Wrestling')
st.subheader('More to come !')

container = st.container()
col1, col2, col3 = st.columns([2, 2, 2])

with col1:
    st.header("Force Analysis with Thin-Film Sensor")
    # Initialize Pygame
    pygame.init()

    # Set up display
    width, height = 800, 600

    screen = pygame.Surface((width, height))  # mac has issue with display.set, but seems okay with surface

    pygame.display.set_caption("Force Sensor")

    # Set up colors
    black = (0, 0, 0)
    white = (255, 255, 255)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    screen.fill(white)
    objectmove = st.empty()

    # board = pymata4.Pymata4()
    # board = pymata4.Pymata4(arduino_wait=True)
    #
    # analog_pin_foot_top = 3
    # board.set_pin_mode_analog_input(analog_pin_foot_top)
    # analog_pin_foot_bottom = 2
    # board.set_pin_mode_analog_input(analog_pin_foot_bottom)
    #
    # generate 2 2d grids for the x & y bounds
    #
    # value_foot_top, time_stamp = board.analog_read(analog_pin_foot_top)
    # value_foot_bottom, time_stamp = board.analog_read(analog_pin_foot_bottom)

    # pygame.draw.rect(screen, (int(255 * value_foot_top / 700), 0, 0), (600, 0, 100, 100))
    # pygame.draw.rect(screen, (int(255 * value_foot_bottom / 700), 0, 0), (600, 400, 100, 100))
    # image_name = "Force Sensor.jpeg"
    # pygame.image.save(screen, image_name)
    # image = Image.open(image_name)
    # objectmove.image(image)

with col2:
    st.header("Vernier Video Analysis ")

with col3:
    st.header("Torque Analysis")