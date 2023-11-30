import streamlit as st
import numpy as np
import pygame
import sys
import math
import pygame
import streamlit as st
from PIL import Image
import sys
import time
import numpy as np

st.set_page_config(page_title="Pendulum Animation", page_icon='tada:', layout="wide")
st.header('Pendulum Animation')
st.subheader('Coming soon !')

input_column, up_column, down_column = st.columns([1, 2, 2])

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
red = (255, 0, 0)



with input_column:
    # Draw a line on the Pygame surface
    line_color = white
    line_start = (400, 0)
    line_end = (600, 450)
    line_width = 15
    pygame.draw.line(screen, line_color, line_start, line_end, line_width)

    # Draw a circle on the Pygame surface
    circle_color = red  # Red
    circle_radius = 50
    circle_center = (600, 450)
    pygame.draw.circle(screen, circle_color, circle_center, circle_radius)

    # Convert Pygame surface to PIL Image
    image_data = pygame.image.tostring(screen, 'RGB')
    image = Image.frombytes('RGB', (width, height), image_data)
    # Display the image in Streamlit
    st.image(image, caption="Pendulum", use_column_width=True)



