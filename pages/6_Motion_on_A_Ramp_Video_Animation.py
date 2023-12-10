import streamlit.components.v1 as components
import pygame
import cv2
import os
import streamlit as st
from PIL import Image
import numpy as np
import ffmpeg


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
def convert_images_to_video(images, output_video_path, fps=20):
    height, width, _ = images[0].shape
    fourcc = cv2.VideoWriter_fourcc(*"MJPG")
    video = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

    for img in images:
        video.write(img)

    cv2.destroyAllWindows()
    video.release()


# Function to convert AVI to MP4 using FFmpeg
def convert_avi_to_mp4(input_avi_path, output_mp4_path):
    ffmpeg.input(input_avi_path).output(output_mp4_path).run()


# Function to remove a file
def remove_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)


# setup page as wide mode
st.set_page_config(layout="wide")

# Initialize Pygame
pygame.init()

# Set up display
width, height = 800, 600
screen = pygame.Surface((width, height))  # mac has issue with display.set, but seems okay with surface
pygame.display.set_caption("Motion on a Ramp")

# Set up colors
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 255)

# video output avi and mp4 name
output_video_path_avi = "output.avi"
output_video_path_mp4 = "output.mp4"
folder_name = "images"
if not os.path.exists(folder_name):
    os.mkdir(folder_name)

# setup three columns, left for input, middle right for up and down motion simulation
container = st.container()
col1, col2, col3 = st.columns([1, 2, 2])
g = 9.81  # g constant m/s^2
# square side length is 25
side = 25

#  input parameter and load a ramp diagram
with (col1):
    ramp_diagram = Image.open("ramp_diagram_dis_bmp.bmp")
    st.image(ramp_diagram, caption='Ramp Diagram')
    Kinetic_Friction_Coefficient = st.number_input('Please enter value of $\\mu_k$ (kinetic friction coefficient) : ',
                                                   0.00, 2.00, 0.15)
    Static_Friction_Coefficient = st.number_input('Please enter value of $\\mu_s$ (static friction coefficient) : ',
                                                  0.00, 3.00, 0.45)
    ramp_angle_degree = st.slider('Ramp angle θ (degree): ', 10, 89,
                                  30)  # small angle run into some accuracy, due to use round 2 or 0.01 for accurancy
    ramp_angle_radian = round(ramp_angle_degree * 3.14 / 180, 2)
    Object_initial_distance = st.number_input('Object Initial Distance D_initial (m) :', 0, 300, 0)

    a_up = - (g * np.sin(ramp_angle_radian) + g * np.cos(ramp_angle_radian) * Kinetic_Friction_Coefficient)
    # the screen is 800 * 600, but the ramp is only use 700 * 500, leaving 50 on each side
    # if tan(ramp angle) >= 5/7, the ramp has fixed height of 500 pixel
    if np.tan(ramp_angle_radian) >= 5 / 7:
        dis_from_initial_to_top = 500 / np.sin(ramp_angle_radian) - Object_initial_distance
    # if tan(ramp angle) < 5/7, the ramp has fixed base of 700 pixel
    else:
        dis_from_initial_to_top = 700 / np.cos(ramp_angle_radian) - Object_initial_distance

    # max V to avoid object move out of the screen
    v_initial_max = round(np.sqrt(-2 * a_up * (dis_from_initial_to_top - side)), 1)
    # set initial v = Vmax / 2
    half_v_initial_max = round(v_initial_max / 2, 1)
    Object_initial_up_speed = st.number_input('Object Initial Moving Up Speed V_initial (m/s) :', 0.0, v_initial_max,
                                              half_v_initial_max)

# Set up Ramp vertices
# 1 is the ramp point, bottom/lower right point
ramp_vertics_1_x = width - 50  # 750
ramp_vertics_1_y = height - 50  # 550

if ramp_angle_degree == 0:
    # 2 is the highest point, upper left point
    ramp_vertics_2_x = 50
    ramp_vertics_2_y = ramp_vertics_1_y
    # 3 is the bottom left point
    ramp_vertics_3_x = ramp_vertics_2_x
    ramp_vertics_3_y = ramp_vertics_2_y
elif ramp_angle_degree == 90:
    # 2 is the highest point
    ramp_vertics_2_x = ramp_vertics_1_x
    ramp_vertics_2_y = 50
    # 3 is the bottom left point
    ramp_vertics_3_x = ramp_vertics_2_x
    ramp_vertics_3_y = ramp_vertics_1_y
else:
    # if tan(ramp angle) >= 5/7, the ramp has fixed height of 500 pixel
    if np.tan(ramp_angle_radian) >= 5 / 7:
        # 2 is the highest point
        ramp_vertics_2_x = ramp_vertics_1_x - ((height - 100) / np.tan(ramp_angle_radian))
        ramp_vertics_2_y = 50
        # 3 is the bottom left point
        ramp_vertics_3_x = ramp_vertics_2_x
        ramp_vertics_3_y = height - 50
    # if tan(ramp angle) < 5/7, the ramp has fixed base of 700 pixel
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

# animation is made of number_of_still_images initial positions + step frames of travel up images +
# 0 or step frames of travel down images
step_up = 20
t1 = np.linspace(0, total_t_up, step_up)
dis_at_t1 = Object_initial_up_speed * t1 + 1 / 2 * a_up * t1 ** 2
if ramp_angle_degree == 0:
    square_initial_1_x = ramp_vertics_1_x
    square_initial_1_y = ramp_vertics_1_y
    Object_initial_height = 0
else:
    square_initial_1_x = ramp_vertics_1_x - Object_initial_distance * np.cos(ramp_angle_radian)
    square_initial_1_y = ramp_vertics_1_y - Object_initial_distance * np.sin(ramp_angle_radian)

# object move up calculation
with col2:
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
    moving_button = st.button('Run Simulation')
    # st.success('After click the "Run Simulation", scroll down to the bottom of the screen to see animation')
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

    # Save initial Images number_of_still_images times, so the images generated video can have enough time to show
    # initial object position well, 00.jpeg, 01.jpeg..... are all initial position image

    number_of_still_images = 12
    for i in range(number_of_still_images):
        if i <= 9:
            image_name = "motion_on_a_ramp_0" + str(i) + ".jpeg"
        else:
            image_name = "motion_on_a_ramp_" + str(i) + ".jpeg"
        image_filename = os.path.join(folder_name, image_name)
        pygame.image.save(screen, image_filename)

    # load the ramp and object initial position
    image = Image.open(image_filename)
    objectmove.image(image)

    if moving_button:
        if output_video_path_mp4:
            remove_file(output_video_path_mp4)
        # due to screen rendering, after click "run simulation", automaticlaly scroll down to the bottom of the screen
        st.session_state.chat = "Object Initial Moving Up Speed V_initial (m/s) :"
        # Define the scroll operation as a function and pass in something unique for each
        # page load that it needs to re-evaluate where "bottom" is
        js = f"""
               <script>
                   function scroll(dummy_var_to_force_repeat_execution){{
                       var textAreas = parent.document.querySelectorAll('section.main');
                       for (let index = 0; index < textAreas.length; index++) {{
                           textAreas[index].style.color = 'red'
                           textAreas[index].scrollTop = textAreas[index].scrollHeight;
                       }}
                   }}
                   scroll({len(st.session_state.chat)})
               </script>
               """
        st.components.v1.html(js)

        # move up animation
        for i in range(step_up):
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
            # if object stuck on the top of the ramp, add "Stuck" on Pygame screen
            if np.sin(ramp_angle_radian) <= np.cos(ramp_angle_radian) * Static_Friction_Coefficient:
                if i == step_up - 1:
                    # Set up font
                    font_size = 36
                    font = pygame.font.Font(None, font_size)
                    # Set up text
                    text = "Stuck!"
                    # text color is black
                    text_color = (0, 0, 0)
                    # Render text
                    text_surface = font.render(text, True, text_color)
                    # Get text rectangle
                    text_rect = text_surface.get_rect()
                    # Set the position of the text
                    text_rect.topleft = (square_vertics_4_x + 20, square_vertics_4_y - 20)
                    # Blit the text onto the screen
                    screen.blit(text_surface, text_rect)

            # Save Image     15.jpeg, 16.jpeg.....
            image_name = "motion_on_a_ramp_" + str(i + number_of_still_images) + ".jpeg"
            image_filename = os.path.join(folder_name, image_name)
            pygame.image.save(screen, image_filename)

        # move down animation
        # object will move down
        if np.sin(ramp_angle_radian) > np.cos(ramp_angle_radian) * Static_Friction_Coefficient:
            a_down = - (g * np.sin(ramp_angle_radian) - g * np.cos(ramp_angle_radian) * Kinetic_Friction_Coefficient)
            dis_from_top_to_bottom = -(square_vertics_1_x - square_initial_1_x) / np.cos(
                ramp_angle_radian) + Object_initial_distance
            time_from_top_to_bottom = np.sqrt(abs(2 * dis_from_top_to_bottom / a_down))
            step_down = int(step_up * time_from_top_to_bottom / total_t_up)
            t2 = np.linspace(0, time_from_top_to_bottom, step_down)
            dis_at_t2 = - 1 / 2 * a_down * t2 ** 2
            square_top_1_x = square_vertics_1_x
            square_top_1_y = square_vertics_1_y

            # moving down
            for i in range(step_down):
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

                # Draw the group line
                pygame.draw.line(screen, black, (0, 555), (800, 555), 10)
                # Draw the ramp
                pygame.draw.polygon(screen, triangle_color, ramp_vertices)
                # Draw the moving square object
                pygame.draw.polygon(screen, object_color, square_vertices)
                # Save Image   35.jpeg, 36.jpeg.....
                folder_name = "images"
                image_name = "motion_on_a_ramp_" + str(i + number_of_still_images + step_down) + ".jpeg"
                image_filename = os.path.join(folder_name, image_name)
                pygame.image.save(screen, image_filename)

        # use all saved jpeg images to make avi video, then convert to mp4 video, and delete the images and avi video
        folder_path = "images"
        # Check if the folder path is provided
        if folder_path and os.path.exists(folder_path):
            # Load images from the folder
            images = load_images_from_folder(folder_path)

            # Check if there are images in the folder
            if images:

                # Convert images to AVI video
                convert_images_to_video(images, output_video_path_avi)

                # Convert AVI to MP4 using FFmpeg
                # convert_avi_to_mp4(output_video_path_avi, output_video_path_mp4)

                # Display the video using Streamlit
                # st.video(output_video_path_mp4)

                # Cleanup: Remove the temporary AVI file
                # remove_file(output_video_path_avi)
                with open(output_video_path_avi, "rb") as file:
                    btn = st.download_button(
                        label="Download Animation Video",
                        data=file,
                        file_name="animation.avi",
                        mime="avi"
                    )
                for filename in os.listdir(folder_path):
                    img_path = os.path.join(folder_path, filename)
                    remove_file(img_path)
            else:
                st.warning("No valid images found in the provided folder.")

# object move up and move down calculation display in Column 3
with col3:
    st.header('Object moving up with initial speed')
    st.text('Ramp angle = ' + str(ramp_angle_degree) + ' degrees')
    st.text('V_initial = ' + str(Object_initial_up_speed) + ' m/s')
    st.text('Object initial distance = ' + str(Object_initial_distance) + ' m')
    st.text('Kinetic friction coefficient = ' + str(Kinetic_Friction_Coefficient))
    st.text('Static friction coefficient = ' + str(Static_Friction_Coefficient))
    st.text('Moving up acceleration = ' + str(round(a_up, 2)) + ' m/s²')
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
        st.text('Moving down acceleration = ' + str(round(a_down, 2)) + ' m/s²')
        st.text('Total moving down distance = ' + str(round(dis_from_top_to_bottom, 2)) + ' m')
        st.text('Total moving down time = ' + str(round(time_from_top_to_bottom, 2)) + ' seconds')
