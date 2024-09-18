import tkinter as tk
import math

window_size = 600
root = tk.Tk()
canvas = tk.Canvas(root, width=window_size, height=window_size)
canvas.pack()

center_x = window_size // 2
center_y = window_size // 2
radius = 200
point_radius = 10

background_circle = canvas.create_oval(center_x - radius, center_y - radius,
                                       center_x + radius, center_y + radius, fill='blue')
moving_point = canvas.create_oval(center_x + radius - point_radius, center_y - point_radius,
                                  center_x + radius + point_radius, center_y + point_radius, fill='green')

current_angle = 0
rotation_speed = 0.005
def update_position():
    global current_angle
    new_x = center_x + radius * math.cos(current_angle)
    new_y = center_y + radius * math.sin(current_angle)

    canvas.coords(moving_point, new_x - point_radius, new_y - point_radius,
                  new_x + point_radius, new_y + point_radius)

    current_angle -= rotation_speed

    root.after(10, update_position)

update_position()

root.mainloop()

