from xrd.models import Scherrer
import os

xrd = Scherrer()

xrd.set_input()

xrd.zoom_area(43, 45.5)

xrd.gauss()

os.remove('temp.csv')