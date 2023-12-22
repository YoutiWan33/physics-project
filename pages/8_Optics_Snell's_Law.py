import streamlit as st
import pygame
from PIL import Image
import numpy as np
import math

# Function to draw a dashed line
def draw_dashed_line(surface, color, start_pos, end_pos,
dash_length=5, gap_length=5):
    dx = end_pos[0] - start_pos[0]
    dy = end_pos[1] - start_pos[1]
    distance = max(1, int(pygame.math.Vector2(dx, dy).length()))
    unit = pygame.math.Vector2(dx, dy) / distance
    dash_count = distance // (dash_length + gap_length)

    for i in range(dash_count):
        start = start_pos + unit * (i * (dash_length + gap_length))
        end = start_pos + unit * (i * (dash_length + gap_length) + dash_length)
        pygame.draw.line(surface, color, start, end, 2)

# Function to draw a line with an arrowhead
def draw_arrow_line(surface, color, start_pos, end_pos, arrow_size=30):
    pygame.draw.line(surface, color, start_pos, end_pos, 4)

    # Calculate the angle of the line
    angle = math.atan2(end_pos[1] - start_pos[1], end_pos[0] - start_pos[0])

    # Calculate the position of the arrowhead
    arrowhead1 = (end_pos[0] - arrow_size * math.cos(angle - math.pi / 6),
                  end_pos[1] - arrow_size * math.sin(angle - math.pi / 6))
    arrowhead2 = (end_pos[0] - arrow_size * math.cos(angle + math.pi / 6),
                  end_pos[1] - arrow_size * math.sin(angle + math.pi / 6))

    # Draw the arrowhead polygon
    pygame.draw.polygon(surface, color, [end_pos, arrowhead1, arrowhead2])


st.set_page_config(page_title='Snells Law', page_icon='tada:', layout="wide")

# three columns - A, B, Output (output with graph)
input_column, output_column = st.columns([1, 2])

# Inputs
with input_column:
    # Incident Angle
    incident_angle = st.slider('Incident Angle (degrees)', 0, 90, 45)

    # Create a list of options
    options = ['Vacuum', 'Air', 'Water','Glass','Sapphire','Diamond']

    # Median 1
    # Use st.selectbox to create a select box
    selected_option_1 = st.selectbox('Select an option for Median 1:', options)

    # Display the selected option
    st.write('You selected:', selected_option_1)

    # Median 2
    # Use st.selectbox to create a select box
    selected_option_2 = st.selectbox('Select an option for Median 2:', options)

    # Display the selected option
    st.write('You selected:', selected_option_2)

    st.image('IndexRefractionTable.png')

    st.image('snellslawdiagram.png')

# Calculation
with (output_column):
    # if statements to convert median to n-value
    if selected_option_1 == 'Vacuum':
        n_value_1 = 1.00000
    elif selected_option_1 == 'Air':
        n_value_1 = 1.00029
    elif selected_option_1 == 'Water':
        n_value_1 = 1.33
    elif selected_option_1 == 'Glass':
        n_value_1 = 1.52
    elif selected_option_1 == 'Sapphire':
        n_value_1 = 1.77
    elif selected_option_1 == 'Diamond':
        n_value_1 = 2.42

    if selected_option_2 == 'Vacuum':
        n_value_2 = 1.00000
    elif selected_option_2 == 'Air':
        n_value_2 = 1.00029
    elif selected_option_2 == 'Water':
        n_value_2 = 1.33
    elif selected_option_2 == 'Glass':
        n_value_2 = 1.52
    elif selected_option_2 == 'Sapphire':
        n_value_2 = 1.77
    elif selected_option_2 == 'Diamond':
        n_value_2 = 2.42

    # calculate for refraction angle
    incident_angle_radian = incident_angle * np.pi / 180
    if n_value_1 * np.sin(incident_angle_radian) / n_value_2 > 1:
        st.markdown('No Refraction. Only Reflection')
    else:
        refraction_angle_radian = np.arcsin(n_value_1 * np.sin(incident_angle_radian) / n_value_2)
        refraction_angle = refraction_angle_radian * 180 / np.pi
        refraction_angle = round(refraction_angle,2)
        st.markdown('Refraction Angle (degrees): ' + str(refraction_angle))

    # Initialize Pygame
    pygame.init()

    # Set up display
    width, height = 800, 600
    screen = pygame.Surface((width, height))
    pygame.display.set_caption("Light Reflection and Refraction")

    # Set up colors
    black = (0, 0, 0)
    white = (255, 255, 255)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    red = (255, 0, 0)

    screen.fill(white)
    objectmove = st.empty()

    # Set up font
    font_size = 55
    font = pygame.font.Font(None, font_size)
    # Set up text
    text1 = "n1: " + selected_option_1
    text2 = "n2: " + selected_option_2
    # text color is black
    text_color = (0, 0, 0)
    # Render text
    text_surface1 = font.render(text1, True, text_color)
    text_surface2 = font.render(text2, True, text_color)
    # Get text rectangle
    text_rect1 = text_surface1.get_rect()  # Set the position of the text
    text_rect1.bottomleft = (50, 280)
    text_rect2 = text_surface2.get_rect()  # Set the position of the text
    text_rect2.topleft = (50, 330)
    # Blit the text onto the screen
    screen.blit(text_surface1, text_rect1)
    screen.blit(text_surface2, text_rect2)

    # Draw the line between two media
    pygame.draw.line(screen, black, (0, 300), (800, 300), 10)
    # dashed line
    draw_dashed_line(screen,black,(400,0),(400,600))

     # draw incident light and refraction light
    if incident_angle == 90:
        incident_start = (0,300)
        incident_end = (400, 300)
        refraction_start = incident_end
        refraction_end = (800,300)
        reflection_start = incident_end
        reflection_end = (800, 300)
    else:
        incident_start = (400 - np.sin(incident_angle_radian) * 300,300 - np.cos(incident_angle_radian) * 300)
        incident_end = (400,300)
        refraction_start = incident_end
        refraction_end = (400 + np.sin(refraction_angle_radian) * 300,300 + np.cos(refraction_angle_radian) * 300)
        reflection_start = incident_end
        reflection_end = (400 + np.sin(incident_angle_radian) * 300,300 - np.cos(incident_angle_radian) * 300)

    draw_arrow_line(screen, blue, incident_start, incident_end)
    draw_arrow_line(screen, green, reflection_start, reflection_end)

    if n_value_1 * np.sin(incident_angle_radian) / n_value_2 <= 1:
        draw_arrow_line(screen, red, refraction_start, refraction_end)

    image_name = "light reflection and refraction.jpeg"
    pygame.image.save(screen, image_name)
    image = Image.open(image_name)
    objectmove.image(image)