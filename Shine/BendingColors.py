from colour import Color

class BendingColors:
    def __init__(self):
        x = 1

    def gradient(self, frm, to, steps):
        colorList = list(Color(frm).range_to(Color(to), steps))
        colors = list()
        for c in colorList:
            aux = {'red': int(c.red * 255), 'green': int(c.green * 255), 'blue': int(c.blue * 255)}
            colors.append(aux)
        return colors
