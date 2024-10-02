import tkinter as tk
import random
import json

def load_config(file_name):
    with open(file_name, 'r') as file:
        return json.load(file)

root = tk.Tk()
root.title("Rain")

config = load_config("config.json")

canvas = tk.Canvas(root, width=config["screen_width"], height=config["screen_height"], bg="gray80")
canvas.pack()


drops = []

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

    def is_out_of_bounds(self):
        return self.y > config["screen_width"]

def gen_drop():
    def size_to_color(size, min_size, max_size):
        normalized_size = (size - min_size) / (max_size - min_size)
        green = int((1 - normalized_size) * 255)
        blue = 255
        return f"#00{green:02x}{blue:02x}"

    x = random.uniform(0, config["screen_width"])
    y = -config["max_size"]
    speed = random.uniform(config['min_speed'], config['max_speed'])
    size = random.uniform(config["min_size"], config["max_size"])
    color = size_to_color(size, config["min_size"], config["max_size"])
    return Drop(x, y, speed, size, color)


def update_raindrops():
    global drops

    canvas.delete("all")

    if random.random() < config['spawn_rate']:
        drops.append(gen_drop())

    for drop in drops:
        drop.move()
        drop.draw(canvas)

    drops = [drop for drop in drops if not drop.is_out_of_bounds()]

    root.after(config['update_interval'], update_raindrops)

update_raindrops()

root.mainloop()
