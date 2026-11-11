from Forge.controller.canvas_controller import CanvasController
from Forge.Video import Video

font_family = "Bodoni MT"
font_color = "#051E6D"

def draw_header(layer):
    title = "Words to Live By"
    subtitle = "A poetry series for the forgetful"
    layer.set_font(family=font_family, size=54)
    layer.draw_text((80,250) , title, color=font_color)
    layer.set_font(family="Consolas", size=16)
    layer.draw_text((85,200), subtitle, color=font_color)


def draw_title(layer):
    poem_title = "And Yet"
    subtitle = "By Franklin Johnson"
    layer.set_font(family=font_family, size=54)
    layer.draw_text((80,250) , poem_title, color=font_color)
    layer.set_font(family="Consolas", size=16)
    layer.draw_text((300, 300), subtitle, color=font_color)



count_stanzas = -1
def stanzas(layer, index):
    cmd = layer.draw_image("tests\\images\\box.jpg", (150, 10), (300, 300))
    layer.draw_shape(cmd)

    global count_stanzas
    if index % 66 == 0:
        count_stanzas += 1
    
    with open("tests\\canvas\\script.txt", "r") as f:
        lines = f.readlines()
    layer.set_font(family=font_family, size=20)

    if count_stanzas + 1 >= len(lines):
        return
    if count_stanzas >= 1:
        prev_line = lines[count_stanzas - 1].strip()
        layer.draw_text((50, 366), prev_line, color="#6A80C3")
    current_line = lines[count_stanzas].strip()
    # next_line = lines[count_stanzas + 1].strip()

    layer.draw_text((50, 433), current_line, color=font_color)
    # layer.draw_text((50, 500), next_line, color="#516190")



class poem(Video):
    def __init__(self):
        super().__init__("poem_video", 600, 600, 95)
        self.background_color = "#E99797"
        self.schedule(1, lambda index, layer: draw_title(layer))
        self.schedule(2, lambda index, layer: draw_header(layer))
        self.schedule(4, lambda index, layer: stanzas(layer, index))




if __name__ == "__main__":
    p = poem()
    p.record()