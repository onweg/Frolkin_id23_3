import tkinter as tk
import random
import json

def load_config(file_name):
    with open(file_name, 'r') as file:
        return json.load(file)

class Drop:
    def __init__(self, x, y, speed, size, color):
        self.x = x
        self.y = y
        self.speed = speed
        self.size = size
        self.color = color

    def move(self):
        self.y += self.speed

    def draw(self, canvas):
        canvas.create_rectangle(
            self.x, self.y, self.x + self.size / 5, self.y + self.size,
            fill=self.color, outline=self.color)

    def is_out_of_bounds(self, screen_height):
        return self.y > screen_height


class Cloud:
    def __init__(self, x, y, width, height, shape, drop_params):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.shape = shape
        self.drop_params = drop_params
        self.drops = []
        self.color = "gray"
        self.selected = False

    def draw(self, canvas):
        outline_color = "blue" if self.selected else "black"
        if self.shape == "rectangle":
            canvas.create_rectangle(self.x, self.y, self.x + self.width,
                                    self.y + self.height, fill=self.color, outline=outline_color)
        elif self.shape == "oval":
            canvas.create_oval(self.x, self.y, self.x + self.width,
                               self.y + self.height, fill=self.color, outline=outline_color)
        elif self.shape == "pooh":
            ball_width = self.width * 0.6
            ball_height = self.height * 0.6
            
            canvas.create_oval(self.x - ball_width * 0.5, self.y + self.height * 0.2,
                               self.x + ball_width * 0.5, self.y + self.height * 0.3 + ball_height,
                               fill=self.color, outline=outline_color)
                               
            canvas.create_oval(self.x + self.width - ball_width * 0.5, self.y + self.height * 0.2,
                               self.x + self.width + ball_width * 0.5, self.y + self.height * 0.3 + ball_height,
                               fill=self.color, outline=outline_color)
            canvas.create_oval(self.x, self.y, self.x + self.width, self.y + self.height, fill=self.color, outline=outline_color)
            
        for drop in self.drops:
            drop.draw(canvas)

    def generate_drop(self):
        def size_to_color(size, min_size, max_size):
            normalized_size = (size - min_size) / (max_size - min_size)
            green = int((1 - normalized_size) * 255)
            blue = 255
            return f"#00{green:02x}{blue:02x}"

        if random.random() < self.drop_params["spawn_rate"]:
            x = random.uniform(self.x, self.x + self.width)
            y = self.y + self.height * 0.6
            speed = random.uniform(self.drop_params["min_speed"], self.drop_params["max_speed"])
            size = random.uniform(self.drop_params["min_size"], self.drop_params["max_size"])
            color = size_to_color(size, self.drop_params["min_size"], self.drop_params["max_size"])
            self.drops.append(Drop(x, y, speed, size, color))

    def update_raindrops(self, screen_height):
        for drop in self.drops:
            drop.move()
        self.drops = [drop for drop in self.drops if not drop.is_out_of_bounds(screen_height)]

    def is_clicked(self, x, y):
        return self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height

    def move(self, dx, dy):
        self.x += dx
        self.y += dy


def main():
    root = tk.Tk()
    root.title("Interactive Clouds")

    config = load_config("config.json")
    canvas = tk.Canvas(root, width=config["screen_width"], height=config["screen_height"], bg="gray80")
    canvas.pack(side="right", expand=True, fill="both")

    frame_left = tk.Frame(root)
    frame_left.pack(side="left", padx=10, pady=10)

    clouds = []
    selected_cloud = None
    drag_start = None

    # Инициализируем shape_var до вызова trace
    shape_var = tk.StringVar()
    shape_var.set("rectangle")  # начальное значение

    def update_scene():
        canvas.delete("all")
        for cloud in clouds:
            cloud.generate_drop()
            cloud.update_raindrops(config["screen_height"])
            cloud.draw(canvas)
        root.after(config["update_interval"], update_scene)

    def on_canvas_click(event):
        nonlocal selected_cloud
        for cloud in clouds:
            if cloud.is_clicked(event.x, event.y):
                if selected_cloud:
                    selected_cloud.selected = False
                selected_cloud = cloud
                selected_cloud.selected = True
                update_controls()
                return
        if selected_cloud:
            selected_cloud.selected = False
            selected_cloud = None
            update_controls()

    def update_controls():
        if selected_cloud:
            width_slider.set(selected_cloud.width)
            height_slider.set(selected_cloud.height)
            density_slider.set(selected_cloud.drop_params["spawn_rate"] * 100)
            min_speed_slider.set(selected_cloud.drop_params["min_speed"])
            max_speed_slider.set(selected_cloud.drop_params["max_speed"])
            min_size_slider.set(selected_cloud.drop_params["min_size"])
            max_size_slider.set(selected_cloud.drop_params["max_size"])
            shape_var.set(selected_cloud.shape.capitalize())

        else:
            width_slider.set(0)
            height_slider.set(0)
            density_slider.set(0)
            min_speed_slider.set(0)
            max_speed_slider.set(0)
            min_size_slider.set(0)
            max_size_slider.set(0)

    # Привязка изменения формы
    def on_shape_change(*args):
        if selected_cloud:
            selected_cloud.shape = shape_var.get().lower()
            update_controls()

    shape_var.trace("w", on_shape_change)  # Теперь можно привязать trace

    def add_cloud_handler():
        cloud = Cloud(100, 100, 150, 100, "rectangle", {
            "spawn_rate": 0.1,
            "min_speed": 2,
            "max_speed": 4,
            "min_size": 10,
            "max_size": 20
        })
        clouds.append(cloud)

    def remove_cloud_handler():
        if selected_cloud in clouds:
            clouds.remove(selected_cloud)
            update_controls()

    def on_slider_change(event=None):
        if selected_cloud:
            selected_cloud.width = width_slider.get()
            selected_cloud.height = height_slider.get()

    def on_rain_params_change(event=None):
        if selected_cloud:
            selected_cloud.drop_params["spawn_rate"] = density_slider.get() / 100
            selected_cloud.drop_params["min_speed"] = min_speed_slider.get()
            selected_cloud.drop_params["max_speed"] = max_speed_slider.get()
            selected_cloud.drop_params["min_size"] = min_size_slider.get()
            selected_cloud.drop_params["max_size"] = max_size_slider.get()

    def on_mouse_press(event):
        nonlocal drag_start
        drag_start = (event.x, event.y)

    def on_mouse_release(event):
        nonlocal drag_start
        if selected_cloud and drag_start:
            dx = event.x - drag_start[0]
            dy = event.y - drag_start[1]
            selected_cloud.move(dx, dy)
        drag_start = None

    canvas.bind("<Button-1>", on_canvas_click)
    canvas.bind("<B1-Motion>", on_mouse_release)

    # UI Elements
    add_button = tk.Button(frame_left, text="Add Cloud", command=add_cloud_handler)
    add_button.pack(pady=5)

    remove_button = tk.Button(frame_left, text="Remove Cloud", command=remove_cloud_handler)
    remove_button.pack(pady=5)

    # Cloud Size
    width_label = tk.Label(frame_left, text="Width")
    width_label.pack()
    width_slider = tk.Scale(frame_left, from_=50, to=300, orient="horizontal", command=on_slider_change)
    width_slider.pack()

    height_label = tk.Label(frame_left, text="Height")
    height_label.pack()
    height_slider = tk.Scale(frame_left, from_=50, to=300, orient="horizontal", command=on_slider_change)
    height_slider.pack()

    label_shape = tk.Label(frame_left, text="Shape:")
    label_shape.pack()

    # Привязка значения формы
    shape_options = ["rectangle", "oval", "pooh"]
    shape_menu = tk.OptionMenu(frame_left, shape_var, *shape_options)
    shape_menu.pack()

    # Rain Parameters
    density_label = tk.Label(frame_left, text="Density (%)")
    density_label.pack()
    density_slider = tk.Scale(frame_left, from_=1, to=100, orient="horizontal", command=on_rain_params_change)
    density_slider.pack()

    min_speed_label = tk.Label(frame_left, text="Min Speed")
    min_speed_label.pack()
    min_speed_slider = tk.Scale(frame_left, from_=1, to=20, orient="horizontal", command=on_rain_params_change)
    min_speed_slider.pack()

    max_speed_label = tk.Label(frame_left, text="Max Speed")
    max_speed_label.pack()
    max_speed_slider = tk.Scale(frame_left, from_=1, to=20, orient="horizontal", command=on_rain_params_change)
    max_speed_slider.pack()

    min_size_label = tk.Label(frame_left, text="Min Size")
    min_size_label.pack()
    min_size_slider = tk.Scale(frame_left, from_=1, to=50, orient="horizontal", command=on_rain_params_change)
    min_size_slider.pack()

    max_size_label = tk.Label(frame_left, text="Max Size")
    max_size_label.pack()
    max_size_slider = tk.Scale(frame_left, from_=1, to=50, orient="horizontal", command=on_rain_params_change)
    max_size_slider.pack()

    update_scene()
    root.mainloop()



if __name__ == "__main__":
    main()
