from PIL import ImageGrab
box_area = (578.0, 239.0, 1170.0, 553.0)
img = ImageGrab.grab(box_area)
img.show()