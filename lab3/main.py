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
        canvas.create_rectangle(self.x, self.y, self.x + self.size / 5, self.y + self.size, fill = self.color, outline=self.color)

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
            canvas.create_rectangle(self.x, self.y, self.x + self.width, self.y + self.height, fill = self.color, outline = outline_color)
        elif self.shape == "oval":
            canvas.create_oval(self.x, self.y, self.x + self.width, self.y + self.height, fill=self.color, outline=outline_color)
        elif self.shape == "pooh":
            canvas.create_oval(self.x, self.y, self.x + self.width, self.y + self.height, fill=self.color, outline=outline_color)
            canvas.create_oval(self.x + self.width * 0.2, self.y - self.height * 0.4, self.x + self.width * 0.5, self.y, fill=self.color, outline=outline_color)
            canvas.create_oval(self.x + self.width * 0.5, self.y - self.height * 0.4, self.x + self.width * 0.8, self.y, fill=self.color, outline=outline_color)
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
            y = self.y + self.height
            speed = random.uniform(self.drop_params["min_speed"], self.drop_params["max_speed"])
            size = random.uniform(self.drop_params["min_size"], self.drop_params["max_size"])
            color = size_to_color(size, self.drop_params["min_size"], self.drop_params["max_size"])
            self.drops.append(Drop(x, y, speed, size, color))
    

    def update_raindrops(self, screen_width):
        for drop in self.drops:
            drop.move()
        self.drops = [drop for drop in self.drops if not drop.is_out_of_bounds(screen_width)]

def add_cloud(x, y, width, height, shape, drop_params, root):
    x_tmp = int(x.get())
    y_tmp = int(y.get())
    width_tmp = int(width.get())
    height_tmp = int(height.get())
    shape_tmp = shape.get()

    spawn_rate = float(entry_spawn_rate.get())
    min_speed = float(entry_min_speed.get())
    max_speed = float(entry_max_speed.get())
    min_size = float(entry_min_size.get())
    max_size = float(entry_max_size.get())
    clouds.append(Cloud(x, y, width, height, drop_params, shape))

def create_input_widgets(root):
    entry_x = tk.Entry(root)
    entry_x.insert(0, "100")
    entry_x.pack()

    entry_y = tk.Entry(root)
    entry_y.insert(0, "100")
    entry_y.pack()

    entry_width = tk.Entry(root)
    entry_width.insert(0, "150")
    entry_width.pack()

    entry_height = tk.Entry(root)
    entry_height.insert(0, "100")
    entry_height.pack()

    shape_var = tk.StringVar()
    shape_var.set("rectangle")
    shape_options = ["rectangle", "oval", "pooh"]
    shape_menu = tk.OptionMenu(root, shape_var, *shape_options)
    shape_menu.pack()

    entry_spawn_rate = tk.Entry(root)
    entry_spawn_rate.insert(0, "0.99")
    entry_spawn_rate.pack()

    entry_min_speed = tk.Entry(root)
    entry_min_speed.insert(0, "40")
    entry_min_speed.pack()

    entry_max_speed = tk.Entry(root)
    entry_max_speed.insert(40, "100")
    entry_max_speed.pack()

    entry_min_size = tk.Entry(root)
    entry_min_size.insert(0, "10")
    entry_min_size.pack()

    entry_max_size = tk.Entry(root)
    entry_max_size.insert(10, "30")
    entry_max_size.pack()
    
    drop_params = {
        "spawn_rate" : float(entry_spawn_rate),
        "min_speed" : float(entry_min_speed),
        "max_speed" : float(entry_max_speed),
        "min_size" : float(entry_min_size),
        "max_size" : float(entry_max_size)
    }
    
    add_cloud_button = tk.Button(root, text="Create Cloud", command=lambda: add_cloud(entry_x, entry_y, entry_width, entry_height, shape_var, drop_params, root))
    add_cloud_button.pack()

    return entry_x, entry_y, entry_width, entry_height, shape_var, drop_params

        

def main():
    root = tk.Tk()
    root.title("Clouds")

    config = load_config("config.json")

    canvas = tk.Canvas(root, width=config["screen_width"], height=config["screen_height"], bg="gray80")
    canvas.pack()
    
    clouds = []
    
    default_drop_params = {
        'spawn_rate': config["spawn_rate"],
        'min_speed': config["drop_min_speed"],
        'max_speed': config["drop_max_speed"],
        'min_size': config["drop_min_size"],
        'max_size': config["drop_max_size"]
    }
    
    def update_scene():
        canvas.delete("all")
        for cloud in clouds:
            cloud.generate_drop()
            cloud.update_raindrops(config["screen_width"])
            cloud.draw(canvas)
        root.after(config['update_interval'], update_raindrops)

    
    add_cloud_button = tk.Button(root, text="Add Cloud", command=add_cloud)
    add_cloud_button.pack()
        
        

root.mainloop() #нужно запустить один раз чтоб следить за интерактивчиками


#self.drop_params = {
#    "min_speed": drop_min_speed,
#    "max_speed": drop_max_speed,
#    "min_size": drop_min_size,
#    "max_size": drop_max_size,
#    "spawn_rate": drop_density
#    }
