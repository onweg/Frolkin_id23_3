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
        canvas.create_rectangle(self.x, self.y, self.x + self.size / 5, self.y + self.size, fill=self.color, outline=self.color)

    def is_out_of_bounds(self, screen_width):
        return self.y > screen_width

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
            canvas.create_rectangle(self.x, self.y, self.x + self.width, self.y + self.height, fill=self.color, outline=outline_color)
        elif self.shape == "oval":
            canvas.create_oval(self.x, self.y, self.x + self.width, self.y + self.height, fill=self.color, outline=outline_color)
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
    

    def update_raindrops(self, screen_width):
        for drop in self.drops:
            drop.move()
        self.drops = [drop for drop in self.drops if not drop.is_out_of_bounds(screen_width)]

def add_cloud(entry_x, entry_y, entry_width, entry_height, shape_var, entry_spawn_rate, entry_min_speed, entry_max_speed, entry_min_size, entry_max_size, clouds):
    x = int(entry_x.get())
    y = int(entry_y.get())
    width = int(entry_width.get())
    height = int(entry_height.get())
    shape = shape_var.get()

    drop_params = {
        "spawn_rate": float(entry_spawn_rate.get()),
        "min_speed": float(entry_min_speed.get()),
        "max_speed": float(entry_max_speed.get()),
        "min_size": float(entry_min_size.get()),
        "max_size": float(entry_max_size.get())
    }

    clouds.append(Cloud(x, y, width, height, shape, drop_params))

def create_input_widgets(root, frame_left):
    label_x = tk.Label(frame_left, text="X-coordinate:")
    label_x.pack()
    entry_x = tk.Entry(frame_left)
    entry_x.insert(0, "100")
    entry_x.pack()

    label_y = tk.Label(frame_left, text="Y-coordinate:")
    label_y.pack()
    entry_y = tk.Entry(frame_left)
    entry_y.insert(0, "100")
    entry_y.pack()

    label_width = tk.Label(frame_left, text="Width:")
    label_width.pack()
    entry_width = tk.Entry(frame_left)
    entry_width.insert(0, "150")
    entry_width.pack()

    label_height = tk.Label(frame_left, text="Height:")
    label_height.pack()
    entry_height = tk.Entry(frame_left)
    entry_height.insert(0, "100")
    entry_height.pack()

    label_shape = tk.Label(frame_left, text="Shape:")
    label_shape.pack()
    shape_var = tk.StringVar()
    shape_var.set("rectangle")
    shape_options = ["rectangle", "oval", "pooh"]
    shape_menu = tk.OptionMenu(frame_left, shape_var, *shape_options)
    shape_menu.pack()

    label_spawn_rate = tk.Label(frame_left, text="Spawn Rate:")
    label_spawn_rate.pack()
    entry_spawn_rate = tk.Entry(frame_left)
    entry_spawn_rate.insert(0, "0.99")
    entry_spawn_rate.pack()

    label_min_speed = tk.Label(frame_left, text="Min Speed:")
    label_min_speed.pack()
    entry_min_speed = tk.Entry(frame_left)
    entry_min_speed.insert(0, "40")
    entry_min_speed.pack()

    label_max_speed = tk.Label(frame_left, text="Max Speed:")
    label_max_speed.pack()
    entry_max_speed = tk.Entry(frame_left)
    entry_max_speed.insert(0, "100")
    entry_max_speed.pack()

    label_min_size = tk.Label(frame_left, text="Min Size:")
    label_min_size.pack()
    entry_min_size = tk.Entry(frame_left)
    entry_min_size.insert(0, "10")
    entry_min_size.pack()

    label_max_size = tk.Label(frame_left, text="Max Size:")
    label_max_size.pack()
    entry_max_size = tk.Entry(frame_left)
    entry_max_size.insert(0, "30")
    entry_max_size.pack()

    return entry_x, entry_y, entry_width, entry_height, shape_var, entry_spawn_rate, entry_min_speed, entry_max_speed, entry_min_size, entry_max_size


def main():
    root = tk.Tk()
    root.title("Clouds")

    config = load_config("config.json")

    frame_left = tk.Frame(root)
    frame_left.pack(side="left", padx=10)

    canvas_frame = tk.Frame(root)
    canvas_frame.pack(side="right", padx=10)

    canvas = tk.Canvas(canvas_frame, width=config["screen_width"], height=config["screen_height"], bg="gray80")
    canvas.pack()
    
    clouds = []
    
    def update_scene():
        canvas.delete("all")
        for cloud in clouds:
            cloud.generate_drop()
            cloud.update_raindrops(config["screen_width"])
            cloud.draw(canvas)
        root.after(config['update_interval'], update_scene)

    entry_x, entry_y, entry_width, entry_height, shape_var, entry_spawn_rate, entry_min_speed, entry_max_speed, entry_min_size, entry_max_size = create_input_widgets(root, frame_left)

    add_cloud_button = tk.Button(frame_left, text="Create Cloud", command=lambda: add_cloud(entry_x, entry_y, entry_width, entry_height, shape_var, entry_spawn_rate, entry_min_speed, entry_max_speed, entry_min_size, entry_max_size, clouds))
    add_cloud_button.pack()

    update_scene()

    root.mainloop()

if __name__ == "__main__":
    main()
