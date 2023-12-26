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


# Function to draw a candle made of rectangular and ellipse
def draw_candle(surface, x_pos, mag):
    # draw a rectangular with width = 30 , height = 90
    # Set up rectangle parameters
    rect_width = 30 * abs(mag)
    rect_height = 90 * abs(mag)
    if mag == 0:
        rect_width = 30
        rect_height = 90
        rect_x, rect_y, rect_width, rect_height = x_pos - rect_width / 2, height / 2 - rect_height, rect_width, rect_height
        pygame.draw.rect(screen, black, (rect_x, rect_y, rect_width, rect_height))
        # draw flame as a 20 * 40 rect ellipse
        pygame.draw.ellipse(screen, orange, (x_pos - rect_width / 2, rect_y - rect_width * 2, rect_width,
                                             rect_width * 2))
    elif mag > 0:   # real image
        rect_x, rect_y, rect_width, rect_height = x_pos - rect_width / 2, height / 2, rect_width, rect_height
        pygame.draw.rect(screen, gray, (rect_x, rect_y, rect_width, rect_height))
        # draw flame as a 20 * 40 rect ellipse
        pygame.draw.ellipse(screen, light_orange,
                            (x_pos - rect_width / 2, rect_y + rect_height, rect_width, rect_width * 2))
    else:   # mag < 0 for virtual image
        rect_x, rect_y, rect_width, rect_height = x_pos - rect_width / 2, height / 2 - rect_height, rect_width, rect_height
        pygame.draw.rect(screen, gray, (rect_x, rect_y, rect_width, rect_height))
        # draw flame as a 20 * 40 rect ellipse
        pygame.draw.ellipse(screen, light_orange, (x_pos - rect_width / 2, rect_y - rect_width * 2, rect_width,
                                             rect_width * 2))

# setup page as wide mode
st.set_page_config(layout="wide")

# setup three columns, left for light reflection simulation, right for light passing lens simulation
container = st.container()
col1, col2, col3 = st.columns([2, 1, 4])

with col1:
    st.title("The Thin Lens Equation")

    # Thin Lens Equation in LaTeX
    thin_lens_equation = r"\frac{1}{f} = \frac{1}{d_o} + \frac{1}{d_i}"

    # Display the Thin Lens Equation
    st.latex(thin_lens_equation)
    st.markdown(r"$f$: **Thin lens focal length**, $f$ is positive for convex lens, $f$ is negative for concave lens")
    st.markdown(r"$d_o$: **Distance from object to lens**, $d_o$ is always positive")
    st.markdown(r"$d_i$: **Distance from image to lens**, $d_i$ is positive for real image (opposite side of the object), $d_i$ is negative for virtual image (same side of object)")

    # st.latex(r"f:\ Thin\ lens\ focal\ length,\ f\ is\ positive\ for\ convex\ lens,\ negative\ for\ concave\ lens.")
    # st.latex(r"{d_o}:\ Distance\ from\ object\ to\ lens,\ {d_o}\ is\ always\ positive.")
    # st.latex(r"{d_i}:\ Distance\ from\ image\ to\ lens,\ {d_i}\ is\ positive\ for\ real\ image\
    #  (opposite\ side\ of\ the\ object),")
    # st.latex(r"\ \ \ \ \ \ \ \ {d_i}\ is\ negative\ for\ virtual\ image\ (where\ the\ image\ is\ on\ the\
    #   same\ side\ of\ object).")

with col3:
    focal_length = st.number_input(r'Please enter value of $f$ (thin lens focal length) : ', 0, 1000, 130)
    d_o = st.selectbox('Choose Distance from Object to Lens:', ('0.6f', 'f', '1.25f', '1.5f', '1.75f', '2f', '3f',
                                                                   '4f', '5f'))

    st.subheader(f"The Convex Thin Lens has focal length of {focal_length}")
    st.subheader("Distance from Object to Lens is " + d_o)

    if d_o == "0.6f":
        object_to_lens = 0.6 * focal_length
        d_i = 1 / (1 / focal_length - 1 / object_to_lens)
        image_to_lens_f = round(-d_i / focal_length, 2)    # add "-" in the front to get a positive number
        image_to_lens_f_str = str(image_to_lens_f)
        m_value = round(-d_i / object_to_lens, 2)
        st.subheader("Distance from Image to Lens is " + image_to_lens_f_str + "f")
        st.subheader("Image Height to Object Height Ratio (M-value) is " + str(m_value))
        st.subheader("Image forms at the same side of object")

    elif d_o == 'f':
        object_to_lens = focal_length
        st.subheader("Image forms at infinity")
    else:
        if d_o == "1.25f":
            object_to_lens = 1.25 * focal_length
        elif d_o == "1.5f":
            object_to_lens = 1.5 * focal_length
        elif d_o == "1.75f":
            object_to_lens = 1.75 * focal_length
        elif d_o == "2f":
            object_to_lens = 2 * focal_length

        elif d_o == "3f":
            object_to_lens = 3 * focal_length

        elif d_o == "4f":
            object_to_lens = 4 * focal_length

        elif d_o == "5f":
            object_to_lens = 5 * focal_length

        d_i = 1 / (1 / focal_length - 1 / object_to_lens)
        image_to_lens_f = round(d_i / focal_length, 2)
        image_to_lens_f_str = str(image_to_lens_f)
        m_value = round(-d_i / object_to_lens, 2)
        st.subheader("Distance from Image to Lens is " + image_to_lens_f_str + "f")
        st.subheader("Image Height to Object Height Ratio is " + str(m_value))
        st.subheader("Image forms on opposite side of object")

    # Initialize Pygame
    pygame.init()

    # Set up display
    width, height = 1600, 1200
    screen = pygame.Surface((width, height))  # mac has issue with display.set, but seems okay with surface
    pygame.display.set_caption("Thin Convex Lens")

    # Set up colors
    black = (0, 0, 0)
    white = (255, 255, 255)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    red = (255, 0, 0)
    yellow = (255, 255, 0)
    orange = (255, 165, 0)
    gray = (128, 128, 128)
    light_orange = (255, 200, 100)

    screen.fill(white)
    objectmove = st.empty()

    # # Set up font
    font_size = 70
    font = pygame.font.Font(None, font_size)

    # Set up text, label f, 2f, 3f, 4f, 5f
    for i in range(5):
        if i == 0:
            text = "f"
        else:
            text = str(i + 1) + "f"
        text_color = black
        # Render text
        text_surface = font.render(text, True, text_color)
        # Get text rectangle
        text_rect = text_surface.get_rect()  # Set the position of the text
        text_rect.topleft = (width / 2 - (i + 1) * focal_length, height / 2 + 30)
        # Draw the center line
        draw_dashed_line(screen, black, (width / 2 - (i + 1) * focal_length, height / 2 - 50),
                         (width / 2 - (i + 1) * focal_length, height / 2 + 50), 4)
        # Blit the text onto the screen
        screen.blit(text_surface, text_rect)
        text_rect.bottomleft = (width / 2 + (i + 1) * focal_length, height / 2 - 30)
        draw_dashed_line(screen, black, (width / 2 + (i + 1) * focal_length, height / 2 - 50),
                         (width / 2 + (i + 1) * focal_length, height / 2 + 50), 4)
        screen.blit(text_surface, text_rect)

    # Draw convex lens
    lens_thickness = 35
    lens_height = 600

    # Draw the center line
    draw_dashed_line(screen, black, (0, height / 2), (width, height / 2), 6)

    # Draw a dashed line at normal
    start_point1 = (width / 2, height / 2 - lens_height)
    end_point1 = (width / 2, height / 2 + lens_height)
    draw_dashed_line(screen, black, start_point1, end_point1)

    # Draw convex lens - a long ellipse
    pygame.draw.ellipse(screen, black, (width / 2 - lens_thickness / 2, height / 2 - lens_height / 2,
                                        lens_thickness, lens_height), 10)

    # Draw Object candle
    draw_candle(screen, width / 2 - object_to_lens, 0)

    # Draw image candle
    if d_o != "f":
        draw_candle(screen, width / 2 + d_i, d_i / object_to_lens)

    # Draw light propagation rays

    # from object flame to lens, parallel to the horizontal line
    # Object candle height = 90 + 60 = 150
    object_height = 150
    object_flame_x = width / 2 - object_to_lens
    object_flame_y = height / 2 - object_height
    start_point1 = (object_flame_x, object_flame_y)
    end_point1 = (width / 2 - object_to_lens / 2, object_flame_y)
    draw_arrow_line(screen, black, start_point1, end_point1, 30)
    start_point2 = end_point1
    end_point2 = (width / 2, object_flame_y)
    pygame.draw.line(screen, black, start_point2, end_point2, 4)
    # from lens to image, focus to the focal length
    start_point3 = end_point2
    end_point3 = (width / 2 + focal_length, height / 2)
    draw_arrow_line(screen, black, start_point3,end_point3, 30)
    start_point4 = end_point3
    end_point4 = (width / 2 + 5 * focal_length, height / 2 + 4 * object_height )
    pygame.draw.line(screen, black, start_point4, end_point4, 4)

    # from object flame top to lens center
    # Object candle height = 90 + 60 = 150
    object_height = 150
    object_flame_x = width / 2 - object_to_lens
    object_flame_y = height / 2 - object_height
    start_point1 = (object_flame_x, object_flame_y)
    end_point1 = (width / 2 - object_to_lens / 2, height / 2 - object_height / 2)
    draw_arrow_line(screen, black, start_point1, end_point1, 30)
    start_point2 = end_point1
    end_point2 = (width / 2, height / 2)
    pygame.draw.line(screen, black, start_point2, end_point2, 4)
    start_point3 = end_point2
    if object_to_lens == focal_length:
        end_point3 = (width / 2 + focal_length, height / 2 + object_height )
    else:
        end_point3 = (width / 2 + focal_length, height / 2 + object_height / object_to_lens * focal_length)
    draw_arrow_line(screen, black, start_point3, end_point3, 30)
    start_point4 = end_point3
    end_point4 = (width / 2 + 5 * focal_length, 5 * focal_length / object_to_lens * object_height + height / 2)
    pygame.draw.line(screen, black, start_point4, end_point4, 4)

    # add dash line for virtual image
    if d_o == "0.6f":
        start_point1 = (width / 2 - object_to_lens, height / 2 - object_height)
        end_point1 = (width / 2 + d_i, height / 2 + object_height * d_i / object_to_lens)
        draw_dashed_line(screen, black, start_point1, end_point1, 4)
        start_point2 = (width / 2, height / 2 - object_height)
        end_point2 = end_point1
        draw_dashed_line(screen, black, start_point2, end_point2, 4)

    image_name = "Thin Convex Lens.jpeg"
    pygame.image.save(screen, image_name)
    image = Image.open(image_name)
    objectmove.image(image)