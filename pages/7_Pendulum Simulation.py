import math
import pygame
import cv2
import os
import streamlit as st
from PIL import Image
import numpy as np
import ffmpeg
# for windows import moviepy.editor as moviepy


# Function to load image from file path
def load_image_from_path(image_path):
    image = Image.open(image_path)
    return np.array(image)


# Function to load all images from a folder
def load_images_from_folder(folder_path):
    images = []
    for filename in sorted(os.listdir(folder_path)):
        img_path = os.path.join(folder_path, filename)
        if os.path.isfile(img_path) and filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            images.append(load_image_from_path(img_path))
    return images


# Function to convert images to an AVI video
def convert_images_to_video(images, output_video_path, fps=40):    # 40 frames per second
    height, width, _ = images[0].shape
    fourcc = cv2.VideoWriter_fourcc(*"MJPG")
    video = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

    for img in images:
        video.write(img)

    cv2.destroyAllWindows()
    video.release()




# Function to convert AVI to MP4 using FFmpeg
# for mac
def convert_avi_to_mp4(input_avi_path, output_mp4_path):
    (
        ffmpeg.input(input_avi_path)
        .output(output_mp4_path)
        .run()
    )


# Function to convert AVI to MP4 using FFmpeg
# for windows
#def convert_avi_to_mp4(input_avi_path, output_mp4_path):
#    clip = moviepy.VideoFileClip(input_avi_path)
#    clip.write_videofile(output_mp4_path)


# Function to remove a file
def remove_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)


# Function to draw dashed line
def draw_dashed_line(surface, color, start_pos, end_pos, width=1, dash_length=15):
    x1, y1 = start_pos
    x2, y2 = end_pos
    dx = x2 - x1
    dy = y2 - y1
    distance = max(abs(dx), abs(dy))
    dx = dx / distance
    dy = dy / distance
    step = dash_length
    for i in range(0, distance, dash_length * 2):
        x1n = int(x1 + dx * step)
        y1n = int(y1 + dy * step)
        x2n = int(x1 + dx * step * 2)
        y2n = int(y1 + dy * step * 2)
        pygame.draw.line(surface, color, (x1n, y1n), (x2n, y2n), width)
        x1 = x2n + dx * step
        y1 = y2n + dy * step


# video output avi and mp4 name
output_video_path_avi = "pendulum output.avi"
output_video_path_mp4 = "pendulum output.mp4"
folder_name = "pendulum images"
if not os.path.exists(folder_name):
    os.mkdir(folder_name)

st.set_page_config(page_title="Pendulum Animation", page_icon='tada:', layout="wide")
st.header('Pendulum Animation')


input_column, math_column, simulation_column = st.columns([1, 2, 2])



# Set up colors
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 255)
red = (255, 0, 0)

# Define the font
font = pygame.font.SysFont(None, 72)

with input_column:
    st.header('Input Parameter')
    L = st.number_input('Please enter the length of the white string L (m): ', 0.05, 5.0, 0.25, 0.05)
    m = st.number_input('Please enter the mass of the red ball (kg)', 1, 1000000, 15, 1)
    theta = st.number_input(
        'Please enter the initial angle ' + r'$\theta_0$' + ' (degree), ' + '0 <= ' r'$\theta_0$' + ' <= 30 degrees',
        0.1, 30.1, 25.0, 0.1, format="%.1f")
    theta_radius = theta / 180 * math.pi

    # Initialize Pygame
    pygame.init()

    # Set up display
    width, height = 800, 600

    # screenup = pygame.display.set_mode((width, height))
    screen = pygame.Surface((width, height))  # mac has issue with display.set, but seems okay with surface
    pygame.display.set_caption("Motion on a Ramp")

    # Draw the white string solid line on the Pygame surface
    line_color = white
    line_start_x = int(width / 2)
    line_start_y = 0
    line_start = (line_start_x, line_start_y)
    L_pixel = int(height * 0.8)
    line_end_x = int(line_start_x + L_pixel * math.sin(theta_radius))
    line_end_y = int(line_start_y + L_pixel * math.cos(theta_radius))
    line_end = (line_end_x, line_end_y)
    line_width = int(height / 50)
    pygame.draw.line(screen, line_color, line_start, line_end, line_width)

    # Draw the label "L"
    label_text1 = "L"
    label_surface = font.render(label_text1, True, white)
    label_rect = label_surface.get_rect()
    label_rect.topleft = (int((line_start_x + line_end_x) / 2 + 30) , int((line_start_y + line_end_y) / 2))
    screen.blit(label_surface, label_rect)

    # Draw the white string vertical dashed line on the Pygame surface
    draw_dashed_line(screen, white, (line_start_x, line_start_y), (line_start_x, L_pixel), width=15, dash_length=15)

    # Draw the label "theta" in latex
    label_text2 = 'θ'
    label_surface = font.render(label_text2, True, white)
    label_rect = label_surface.get_rect()
    label_rect.topleft = (405, 200)
    screen.blit(label_surface, label_rect)

    # Draw a circle on the Pygame surface
    circle_color = red  # Red
    circle_radius = 25
    circle_center = (line_end_x, line_end_y)
    pygame.draw.circle(screen, circle_color, circle_center, circle_radius)

    # Draw the label "m"
    label_text3 = "m"
    label_surface = font.render(label_text3, True, white)
    label_rect = label_surface.get_rect()
    label_rect.topleft = (line_end_x + 50, line_end_y)
    screen.blit(label_surface, label_rect)

    # Convert Pygame surface to PIL Image
    image_data = pygame.image.tostring(screen, 'RGB')
    image = Image.frombytes('RGB', (width, height), image_data)
    # Display the image in Streamlit
    st.image(image)



with math_column:
    st.header('Force Analysis and Equation of Motion')
    st.image("Pendulum force analysis.jpg")
    st.latex(r'Component\ of\ the\ gravitational\ force\ along\ the\ tangential\ direction')
    st.latex(r'F = ma_t = -mg\sin(\theta)')
    st.latex(r'a_t = -g \sin(\theta)')
    st.latex(r'where\ a_t\ is\ the\ acceleration\ along\ tangential\ direction')
    st.latex(r'The\ negative\ sign\ implies\ that')
    st.latex(r'a_t\ and\ θ\ always\ point\ to opposite\ direction')
    st.latex(r's\ is\ the\ arc\ length\ corresponding\ to\ θ\ angle.')
    st.latex(r's = L \theta')
    st.latex(r'v = \frac{ds}{dt}= L \frac{d\theta}{dt}')
    st.latex(r'a_t = \frac{d^2s}{dt^2} = L \frac{d^2\theta}{dt^2}')
    st.latex(r'-g\sin(\theta) = L\frac{d^2\theta}{dt^2}')
    st.latex(r'when\ \theta\ is\ a\ small\ angle')
    st.latex(r'\sin(\theta) \approx \theta')
    st.latex(r'\frac{{d^2\theta}}{{dt^2}} + \frac{g}{L} \theta = 0')
    st.latex(r'when\ t = 0,\ the\ initial\ angle\ =\ \theta_0')
    st.latex(r'so\ the\ solution\ is\ :')
    st.latex(r'\boxed{\theta(t) = \theta_0 \cos\left(\sqrt{\frac{g}{L}} t\right)}')

with simulation_column:
    # define "Run simulation" Button style
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
    button = st.button('Run Simulation')
    st.success('The simulation movie has 40 frames per second. It may take about 3 seconds to run the movie, thanks for your patience.')
    g = 9.8                             # 9.8 m /s^2
    T = 2 * math.pi * math.sqrt(L/g)    # period of the pendulum
    if button:
        st.write("The period for this pendulum oscillation is {:.2f} seconds.".format(T))
        st.write("click the movie and choose <strong><span style='border: 1px solid black; padding: 2px;'>loop</span></strong> mode for continuous oscillation", unsafe_allow_html=True)

        num_points = int(T / (1 / 40))  # Adjust the number of points as needed
        time_values = np.linspace(0, T, num_points)
        count = 0
        # Function to convert images to an AVI video  def convert_images_to_video(images, output_video_path, fps=30):  # 30 frames per second

        for t in time_values:
            count = count + 1
            theta_value = theta_radius * math.cos(math.sqrt(g/L)* t)
            # Clear the screen
            screen.fill(black)

            # draw the white line at time t
            line_color = white
            line_start_x = int(width / 2)
            line_start_y = 0
            line_start = (line_start_x, line_start_y)
            L_pixel = int(height * 0.8)
            line_end_x_t = int(line_start_x + L_pixel * math.sin(theta_value))
            line_end_y_t = int(line_start_y + L_pixel * math.cos(theta_value))
            line_end = (line_end_x_t, line_end_y_t)
            line_width = int(height / 50)
            pygame.draw.line(screen, line_color, line_start, line_end, line_width)

            # draw the red ball at time t
            circle_color = red  # Red
            circle_radius = 25
            circle_center = (line_end_x_t, line_end_y_t)
            pygame.draw.circle(screen, circle_color, circle_center, circle_radius)

            # Label L = # meters
            # Define the font
            font = pygame.font.SysFont(None, 30)
            L = round(L, 2)
            label_text1 = "L = {} meters".format(L)
            label_surface = font.render(label_text1, True, white)
            label_rect = label_surface.get_rect()
            label_rect.topleft = (int((line_start_x + line_end_x) / 2 + 80), int((line_start_y + line_end_y) / 2))
            screen.blit(label_surface, label_rect)

            # Label T = # seconds
            # Define the font
            font = pygame.font.SysFont(None, 30)
            T = round(T, 2)
            label_text2 = "T = {} seconds".format(T)
            label_surface = font.render(label_text2, True, white)
            label_rect = label_surface.get_rect()
            label_rect.topleft = (int((line_start_x + line_end_x) / 2 + 80), int((line_start_y + line_end_y) / 2) + 40)
            screen.blit(label_surface, label_rect)

            # Label real-time t seconds
            # Define the font
            font = pygame.font.SysFont(None, 30)
            t = round(t, 2)
            label_text3 = "t = {} seconds".format(t)
            label_surface = font.render(label_text3, True, white)
            label_rect = label_surface.get_rect()
            label_rect.topleft = (int((line_start_x + line_end_x) / 2 + 80), int((line_start_y + line_end_y) / 2) + 80)
            screen.blit(label_surface, label_rect)

            # Convert Pygame surface to PIL Image
            image_data = pygame.image.tostring(screen, 'RGB')
            image = Image.frombytes('RGB', (width, height), image_data)

            folder_name = "pendulum images"
            # Save Image
            if count <= 9:
                image_name = "pendulum_00" + str(count) + ".jpeg"
            elif count <= 99:
                image_name = "pendulum_0" + str(count) + ".jpeg"
            else:
                image_name = "pendulum_" + str(count) + ".jpeg"

            image_filename = os.path.join(folder_name, image_name)
            pygame.image.save(screen, image_filename)

        # use all saved jpeg images to make avi video, then convert to mp4 video, and delete the images and avi video
        folder_path = "pendulum images"

        # Check if the folder path is provided
        if folder_path and os.path.exists(folder_path):
            # Load images from the folder
            images = load_images_from_folder(folder_path)

            # Check if there are images in the folder
            if images:

                # Convert images to AVI video
                convert_images_to_video(images, output_video_path_avi)

                # if mp4 exists, delete
                if output_video_path_mp4 in os.listdir():
                    remove_file(output_video_path_mp4)

                # Convert AVI to MP4 using FFmpeg
                convert_avi_to_mp4(output_video_path_avi, output_video_path_mp4)

                # Display the video using Streamlit
                st.video(output_video_path_mp4)

                # Cleanup: Remove the temporary AVI file
                # remove_file(output_video_path_avi)
                # with open(output_video_path_avi, "rb") as file:
                #     btn = st.download_button(
                #         label="Download Animation Video",
                #         data=file,
                #         file_name="animation.avi",
                #         mime="avi"
                #     )
                # st.success("The animation video is a avi file. Please download to watch.")

                for filename in os.listdir(folder_path):
                    img_path = os.path.join(folder_path, filename)
                    remove_file(img_path)
            else:
                st.warning("No valid images found in the provided folder.")

