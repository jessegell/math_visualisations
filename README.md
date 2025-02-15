# math_visualizations

This project contains visualizations of mathematical concepts.  

These are written in python using the matplotlib module.

Files contain functions which can be run in python3 with user inputs.  

The file **convergence_animation.py** creates a video demonstration of the concept of convergence of a sequence of points in the plane.  You can see an **example video on [my website](https://jessegell.github.io/teaching/)**.

- The user inputs:
    1. a sequence, written as two functions of n.
    2. a descending sequence of real numbers, which will be the radii of a nested family of discs around the origin.
- Running the function outputs a video.   The movie plots the sequence and then zooms in on the nested ball of radius epsilon.  It indicates the index of the sequence past which it lies entirely in the ball.
- Matplotlib functionalities allow the user to save the animation to a .mp4 or .gif or to .html.
- [This google colab tutorial](https://colab.research.google.com/drive/1slOKKJgM0Me-aDJejIKOvuoo_e-CuOaN) is available to take the user through the underlying mathematical concepts, and also to be used as a tutorial for analysis students.

