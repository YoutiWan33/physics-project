import streamlit as st
import matplotlib.pyplot as plt
import math
import numpy as np

st.set_page_config(page_title= "CrossProduct", page_icon='tada:', layout="wide")

st.header('Cross Product')
st.markdown(
    """
    As you can guess, the cross product is written as a cross between two vectors: **a** × **b**. \n
    The geometric definition is \n
    **a** × **b** = (a)(b)sin(θ)û \n
    Note that θ is the angle between vectors A and B. Non-bolded a and b are the magnitudes of their respective vectors. \n
    The analytic definition is \n
    """)
st.latex(r'\textbf{a}'r'\times'r'\textbf{b}'r'''= (a_yb_z - a_zb_y)x̂ - (a_xb_z - a_zb_x)ŷ + (a_xb_y - a_yb_x)ẑ ''')
st.markdown(
    """
    These definitions return a vector quantity because the cross product has magnitude and direction. 
    ### The simulation below calculates the cross product and graphs the two input vectors. Play around!
    """)

# three columns - A, B, Output (output with graph)
A_column, B_column, Output_column = st.columns([2, 2, 6])

# A Vector
with A_column:
    # input
    st.latex(r'''\vec{A}''' + '   Input:')
    Ax = A_column.number_input('Please enter X component of Vector A: ', -1000000000, 1000000000, 6)
    Ay = A_column.number_input('Please enter Y component of Vector A: ', -1000000000, 1000000000, 4)
    Az = A_column.number_input('Please enter Z component of Vector A: ', -1000000000, 1000000000, 3)
    # graph
    figA = plt.figure(1)
    ax = figA.add_subplot(projection='3d')
    ax.quiver(0, 0, 0, Ax, Ay, Az, color='red')
    ax.set_xlim(min(0, (Ax - 1)), max(0, (Ax + 1)))
    ax.set_ylim(min(0, (Ay - 1)), max(0, (Ay + 1)))
    ax.set_zlim(min(0, (Az - 1)), max(0, (Az + 1)))
    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_zlabel('Z axis')
    ax.set_title('Vector A')
    #st.write(figA)

# B Vector
with B_column:
    # input
    st.latex(r'''\vec{B}''' + '   Input:')
    Bx = B_column.number_input('Please enter X component of Vector B: ', -1000000000, 1000000000, 5)
    By = B_column.number_input('Please enter Y component of Vector B: ', -1000000000, 1000000000, 6)
    Bz = B_column.number_input('Please enter Z component of Vector B: ', -1000000000, 1000000000, 4)
    # graph
    figB = plt.figure(2)
    ax = figB.add_subplot(projection='3d')
    ax.quiver(0, 0, 0, Bx, By, Bz, color='red')
    ax.set_xlim(min(0, (Bx - 1)), max(0, (Bx + 1)))
    ax.set_ylim(min(0, (By - 1)), max(0, (By + 1)))
    ax.set_zlim(min(0, (Bz - 1)), max(0, (Bz + 1)))
    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_zlabel('Z axis')
    ax.set_title('Vector B')
    #st.write(figB)

# output column
with (Output_column):
    # dot_product = abs(a_mag)*abs(b_mag)*math.cos(theta)
    dot_product = Ax*Bx + Ay*By + Az*Bz
    # solve for theta (radians)
    a_mag = math.sqrt(Ax*Ax+Ay*Ay+Az*Az)
    b_mag = math.sqrt(Bx*Bx+By*By+Bz*Bz)
    if a_mag != 0 and b_mag != 0:
        acos_theta = round(dot_product / (abs(a_mag) * abs(b_mag)),4)

        theta = math.acos(acos_theta)
        mag = abs(a_mag) * abs(b_mag) * math.sin(theta)

        st.header("Angle between Vector A and Vector B is " + str(round(theta * 180 / np.pi, 2)) + " degrees")

    else:
        st.header("Invalid because magnitude of Vector A or B is 0")

    # cross product
    d1mag = Ay*Bz-Az*By
    d2mag = Az*Bx-Ax*Bz
    d3mag = Ax*By-Ay*Bx
    # magnitude |a||b|sin(θ)

    # graph
    figC = plt.figure(3)
    ax = figC.add_subplot(projection='3d')
    ax.quiver(0, 0, 0, Ax, Ay, Az, color='red')
    ax.quiver(0, 0, 0, Bx, By, Bz, color='blue')
    ax.quiver(0, 0, 0, d1mag, d2mag, d3mag, color='purple')
    ax.set_xlim(min(0, (Ax - 1),(Bx - 1),(d1mag - 1)), max(0, (Ax + 1),(Bx + 1),(d1mag + 1)))
    ax.set_ylim(min(0, (Ay - 1),(By - 1),(d2mag - 1)), max(0, (Ay + 1),(By + 1),(d2mag + 1)))
    ax.set_zlim(min(0, (Az - 1),(Bz - 1),(d3mag - 1)), max(0, (Az + 1),(Bz + 1),(d3mag + 1)))
    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_zlabel('Z axis')
    ax.set_title('Vector A, B, and A X B')
    ax.text(Ax, Ay, Az, "A", color='red')
    ax.text(Bx, By, Bz, "B", color='blue')
    ax.text(d1mag, d2mag, d3mag, "AXB", color='purple')
    st.write(figC)


# Manage font, organization, etc
A_column.markdown(
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

B_column.markdown(
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