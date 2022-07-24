from ast import Pass, Return
from email.policy import default
from cProfile import label
from operator import ne
from tkinter import *
from tkinter import filedialog, messagebox
from turtle import left, right
from PIL import ImageTk, Image, ImageEnhance
from black import cancel
from click import command
import cv2
from matplotlib import image
import numpy as np



window = Tk()
window.title('Image Editor')

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
window.geometry(f'{screen_width}x{screen_height}')

#font tupple
Font_tuple = ("Helvetica Neue 95 Black", 15)
Font_tuple1 = ("Helvetica Neue 95 Black", 10)

frame_1 = Frame(window, width=screen_width, height=(screen_height/7), bg='#FCE6C9')
frame_1.pack()


frame_2 = Frame(window, width=(screen_width/4), height=(6*screen_height/7), bg='#514143')
frame_2.pack(side='left')


frame_3 = Frame(window, width=(3*screen_width/4), height=(6*screen_height/7), bg='#6A5A5D')
frame_3.pack(side='right')

'''
    -----------------------
    |  Callback Funtions  |
    -----------------------
'''

global original_image, output_image, img_width, img_height

#image viewer.
def display_image(img):
    global img_width, img_height
    img_width, img_height = img.size
    ratio = img_height / img_width

    new_width = img_width
    new_height = img_height

    img_frame_h = (5*screen_height)/8
    img_frame_w = (13*screen_width)/28

    if(img_height > img_frame_h or img_width > img_frame_w):
        if ratio < 1:
            new_width = int(img_frame_w)
            new_height = int(new_width * ratio)
        else:
            new_height = int(img_frame_h)
            new_width = int(new_height * (img_width / img_height))

    image_to_display = img.resize((new_width,new_height),Image.ANTIALIAS)
    image_to_display = ImageTk.PhotoImage(image_to_display)
    display.configure(image=image_to_display)
    display.photo_ref = image_to_display
    display.place(anchor='center')

#import image
def select_image():
    global original_image
    file_name = filedialog.askopenfilename()
    original_image = Image.open(file_name)
    display_image(original_image)

#save image
def save_image():
    save_file = filedialog.asksaveasfilename(defaultextension=".jpeg")
    output_image.save(save_file)

def exit():
    warning=messagebox.askokcancel(title='Exit Page', message="Do you want to Exit!", icon='warning', default='cancel')
    if(warning == 1):
        window.destroy()
    

#brightness
def image_brightness(brightness_pos):
    global output_image
    brightness_pos = float(brightness_pos)
    enhancer = ImageEnhance.Brightness( original_image )
    output_image = enhancer.enhance(brightness_pos)
    display_image(output_image)

#contrast
def image_contrast(contrast_pos):
    global output_image
    contrast_pos = float(contrast_pos)
    enhancer = ImageEnhance.Contrast(original_image)
    output_image = enhancer.enhance(contrast_pos)
    display_image(output_image)

#blur
def image_sharpness(sharpness_pos):
    global output_image
    sharpness_pos = (float(sharpness_pos))
    enhancer = ImageEnhance.Sharpness(original_image)
    output_image = enhancer.enhance(sharpness_pos)
    display_image(output_image)

#saturation
def image_saturation(color_pos):
    global output_image
    color_pos = float(color_pos)
    enhancer = ImageEnhance.Color(original_image)
    output_image = enhancer.enhance(color_pos)
    display_image(output_image)

#rotate image
def image_rotation():
    global original_image, output_image
    output_image = original_image.rotate(-90,expand=True)
    original_image = output_image
    display_image(original_image)

#crop image
def crop_image(left, top, right, bottom):
    global output_image
    img = original_image
    output_image = img.crop((left, top, right, bottom))
    display_image(output_image)

##text on image
#def text_image():
#    global output_image


#vertical flip image
def vertical_flip():
    global original_image, output_image
    output_image = original_image.transpose(Image.FLIP_LEFT_RIGHT)
    original_image = output_image
    display_image(original_image)

#horizontal flip image
def horizontal_flip():
    global original_image, output_image
    output_image = original_image.transpose(Image.FLIP_TOP_BOTTOM)
    original_image = output_image
    display_image(original_image)

#cancel option
def cancel_efect():
    global output_image
    output_image = original_image
    display_image(output_image)

#making output image an orignal image.
def save_outputImage():
    global original_image
    original_image = output_image



'''
    ---------------------
    |      Filters      |
    ---------------------
'''

#Sketch filter
def sketch_image():
    global output_image
    img_gray = cv2.cvtColor(np.asarray(original_image), cv2.COLOR_RGB2GRAY)  #importing image in array form and gray scale
    img_blur = cv2.GaussianBlur(img_gray, (43, 67), 0, 0)               #applyig gaussian blur
    img_blend = cv2.divide(img_gray, img_blur, scale=256)           #dividing gray image by blur image
    output_image = Image.fromarray(img_blend)                   #now changing from array to an image
    display_image(output_image)

#cartoon filter.
def cartoon_image():
    global output_image
    img = cv2.stylization(np.asarray(original_image), sigma_s=15, sigma_r=0.55) 
    output_image = Image.fromarray(img)
    display_image(output_image)

def gamma_function(channel, gamma):
        invGamma = 1 / gamma
        table = np.array([((i / 255.0) ** invGamma) * 255
                          for i in np.arange(0, 256)]).astype("uint8")  #creating lookup table
        channel = cv2.LUT(channel, table)
        return channel

#warm filter
def warm_image():
    global output_image
    img = np.asarray(original_image)
    img[:, :, 0] = gamma_function(img[:, :, 0], 1.20)  #up scaling red channel 
    img[:, :, 2] = gamma_function(img[:, :, 2], 0.75)  #down scaling blue channel
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hsv[:, :, 1] = gamma_function(hsv[:, :, 1], 1.2)  #up scaling saturation channel
    img = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    output_image = Image.fromarray(img)
    display_image(output_image)
    
#invert(negative) image filter
def invert_image():
    global output_image
    img = cv2.bitwise_not(np.asarray(original_image))      #invert the image
    output_image = Image.fromarray(img)
    display_image(output_image)


'''
    -----------------------------------
    | Buttons, Sliders, Bullet Points |   
    -----------------------------------
'''
#filter buttons
def filter_opions():
    #to remove the buttons from the frame
    apply_command = lambda:[save_outputImage(),
                            sketch_button.place_forget(),
                            cartoon_button.place_forget(),
                            warm_button.place_forget(),
                            invert_button.place_forget(),
                            none_button.place_forget(),
                            cancel_button.place_forget(),
                            apply_button.place_forget()]

    cancel_command = lambda:[cancel_efect(),
                            sketch_button.place_forget(),
                            cartoon_button.place_forget(),
                            warm_button.place_forget(),
                            invert_button.place_forget(),
                            none_button.place_forget(),
                            cancel_button.place_forget(),
                            apply_button.place_forget()]

    sketch_button = Radiobutton(frame_2,
                                text = "   Sketch   ",
                                bg="red",
                                font=Font_tuple1,
                                indicatoron=0,
                                padx=10,
                                pady=5,
                                value=1,
                                command=sketch_image)
    sketch_button.place(anchor='center', relx=0.25, rely=0.58)

    cartoon_button = Radiobutton(frame_2,
                                text = "  Cartoon  ",
                                bg="yellow",
                                font=Font_tuple1,
                                indicatoron=0,
                                padx=10,
                                pady=5,
                                value=2,
                                command=cartoon_image)
    cartoon_button.place(anchor='center', relx=0.75, rely=0.58)

    warm_button = Radiobutton(frame_2,
                                text = "Warm Filter",
                                bg="green",
                                font=Font_tuple1,
                                indicatoron=0,
                                padx=10,
                                pady=5,
                                value=3,
                                command=warm_image)
    warm_button.place(anchor='center', relx=0.25, rely=0.65)

    invert_button = Radiobutton(frame_2,
                                text = "  Negative  ",
                                bg="blue",
                                font=Font_tuple1,
                                indicatoron=0,
                                padx=10,
                                pady=5,
                                value=4,
                                command=invert_image)
    invert_button.place(anchor='center', relx=0.75, rely=0.65)

    none_button = Radiobutton(frame_2,
                                text = "    None    ",
                                font=Font_tuple1,
                                indicatoron=0,	
                                activebackground="orange",
                                padx=10,
                                pady=5,
                                value=5,
                                command=cancel_efect)
    none_button.place(anchor='center', relx=0.505, rely=0.72)
    none_button.select()

    cancel_button = Radiobutton(frame_2,
                                text = "   Cancel   ",
                                font=Font_tuple1,
                                indicatoron=0,	
                                activebackground="red",
                                padx=10,
                                pady=5,
                                value=5,
                                command=cancel_command)
    cancel_button.place(anchor='center', relx=0.25, rely=0.72)
    cancel_button.select()

    apply_button = Radiobutton(frame_2,
                                text = "   Apply   ",
                                font=Font_tuple1,
                                indicatoron=0,	
                                activebackground="green",
                                padx=10,
                                pady=5,
                                value=5,
                                command=apply_command)
    apply_button.place(anchor='center', relx=0.75, rely=0.72)

#imahe croping tools
def image_crop_tools():

    #to remove the buttons from the frame
    apply_command = lambda:[save_outputImage(),
                            top_slider.place_forget(),
                            bottom_slider.place_forget(),
                            left_slider.place_forget(),
                            right_slider.place_forget(),
                            cancel_button.place_forget(),
                            apply_button.place_forget()]

    cancel_command = lambda:[cancel_efect(),
                            top_slider.place_forget(),
                            bottom_slider.place_forget(),
                            left_slider.place_forget(),
                            right_slider.place_forget(),
                            cancel_button.place_forget(),
                            apply_button.place_forget()]

    #works for left side of the image
    top_slider = Scale(frame_3, from_=0, 
                to=img_width,
                length=int((13*screen_width)/28),
                sliderlength=15,
                troughcolor="#A06550",
                orient=HORIZONTAL, 
                bg='#6A5A5D',
                foreground="#C38560",
                command= lambda x: crop_image(top_slider.get(),
                                                left_slider.get(), 
                                                bottom_slider.get(), 
                                                right_slider.get()))
    top_slider.place(anchor='center', relx=0.5, rely=0.07)

    #works for right side of the image
    bottom_slider = Scale(frame_3, from_=0, 
                to=img_width,
                length=int((13*screen_width)/28),
                sliderlength=15,
                troughcolor="#A06550",
                orient=HORIZONTAL, 
                bg='#6A5A5D',
                foreground="#C38560",
                command= lambda x: crop_image(top_slider.get(),
                                                left_slider.get(), 
                                                bottom_slider.get(), 
                                                right_slider.get()))
    bottom_slider.set(img_width)
    bottom_slider.place(anchor='center', relx=0.5, rely=0.93)
    
    #works for top side of the image
    left_slider = Scale(frame_3, from_=0, 
                to=img_height,
                length=int((5*screen_height)/9),
                sliderlength=15,
                troughcolor="#A06550",
                bg='#6A5A5D',
                foreground="#C38560",
                command= lambda x: crop_image(top_slider.get(),
                                                left_slider.get(), 
                                                bottom_slider.get(), 
                                                right_slider.get()))
    left_slider.place(anchor='center', relx=0.1, rely=0.5)

    #works for bottom side of the image
    right_slider = Scale(frame_3, from_=0, 
                to=img_height, 
                length=int((5*screen_height)/9),
                sliderlength=15,
                troughcolor="#A06550",
                bg='#6A5A5D',
                foreground="#C38560",
                command= lambda x: crop_image(top_slider.get(),
                                                left_slider.get(), 
                                                bottom_slider.get(), 
                                                right_slider.get()))
    right_slider.set(img_height)
    right_slider.place(anchor='center', relx=0.9, rely=0.5)

    #apply button 
    cancel_button = Button(frame_3, font=Font_tuple, 
                            text='  Cancel  ', 
                            bg="#FCE6C9",
                            padx=10,
                            pady=5, 
                            compound=TOP,
                            command=cancel_command)
    cancel_button.place(anchor='center', relx=0.1, rely=0.94)

    #apply button 
    apply_button = Button(frame_3, font=Font_tuple, 
                            text='  Apply  ', 
                            bg="#FCE6C9",
                            padx=10,
                            pady=5, 
                            compound=TOP,
                            command=apply_command)
    apply_button.place(anchor='center', relx=0.9, rely=0.94)

    


#open button.
open_img = PhotoImage(file="Icons/open_image.png") 
open_button = Button(frame_1, font=Font_tuple, 
                        text='Select Image', 
                        bg="#FCE6C9",
                        padx=10,
                        pady=5,
                        image=open_img,
                        width=300,
                        compound=TOP,
                        command=select_image)
open_button.place(anchor='center', relx=0.125, rely=0.5)

#Filter button.
filter_img = PhotoImage(file="Icons/filter.png") 
filter_button = Button(frame_1, font=Font_tuple, 
                        text='  Filter  ', 
                        bg="#FCE6C9",
                        padx=10,
                        pady=5, 
                        image=filter_img,
                        compound=TOP,
                        command=filter_opions)
filter_button.place(anchor='center', relx=0.3, rely=0.5)

#Rotate button.
rotate_img = PhotoImage(file="Icons/rotate.png") 
rotate_button = Button(frame_1, font=Font_tuple, 
                        text=' Rotate ', 
                        bg="#FCE6C9",
                        padx=10,
                        pady=5, 
                        image=rotate_img,
                        compound=TOP,
                        command=image_rotation)
rotate_button.place(anchor='center', relx=0.4, rely=0.5)

#Crop button.
crop_img = PhotoImage(file="Icons/crop.png") 
crop_button = Button(frame_1, font=Font_tuple, 
                        text='  Crop  ', 
                        bg="#FCE6C9",
                        padx=10,
                        pady=5,
                        image=crop_img,
                        compound=TOP,
                        command= image_crop_tools)
crop_button.place(anchor='center', relx=0.5, rely=0.5)
#
#       ------------------------------------------------------------
#       |                                                          |
#       |       Work In Future on text writing on image            |
#       |                                                          |
#       ------------------------------------------------------------
#
'''
#Text button.
text_img = PhotoImage(file="Icons/Text.png") 
text_button = Button(frame_1, font=Font_tuple, 
                        text='  Text  ', 
                        bg="#FCE6C9",
                        padx=10,
                        pady=5,
                        image=text_img,
                        compound=TOP)
text_button.place(anchor='center', relx=0.6, rely=0.5)

#Vertical_flip_button.place(anchor='center', relx=0.7, rely=0.5)
#Horizontal_flip_button.place(anchor='center', relx=0.8, rely=0.5)
#exit_button.place(anchor='center', relx=0.9, rely=0.5)
'''

#Vertical flip button.
Vertical_flip_img = PhotoImage(file="Icons/vertical_flip.png") 
Vertical_flip_button = Button(frame_1, font=Font_tuple, 
                        text='   Flip   ', 
                        bg="#FCE6C9",
                        padx=10,
                        pady=5, 
                        image=Vertical_flip_img,
                        compound=TOP,
                        command=vertical_flip)
Vertical_flip_button.place(anchor='center', relx=0.6, rely=0.5)

#Horizontal flip button.
Horizontal_flip_img = PhotoImage(file="Icons/horizontal_flip.png") 
Horizontal_flip_button = Button(frame_1, font=Font_tuple, 
                        text='   Flip   ', 
                        bg="#FCE6C9",
                        padx=10,
                        pady=5, 
                        image=Horizontal_flip_img,
                        compound=TOP,
                        command=horizontal_flip)
Horizontal_flip_button.place(anchor='center', relx=0.7, rely=0.5)

#Exit button.
exit_img = PhotoImage(file="Icons/close.png") 
exit_button = Button(frame_1, font=Font_tuple, 
                        text='   Exit   ', 
                        bg="#FCE6C9",
                        padx=10,
                        pady=5,
                        image=exit_img,
                        compound=TOP,
                        command=exit)
exit_button.place(anchor='center', relx=0.8, rely=0.5)

#save button.
save_img = PhotoImage(file="Icons/save.png")
save_button = Button(frame_2, font=Font_tuple, 
                        text='Save Image', 
                        bg="#FCE6C9",
                        padx=10,
                        pady=5,
                        image=save_img,
                        width=300,
                        compound=TOP,
                        command=save_image)
save_button.place(anchor='center', relx=0.5, rely=0.9)

#brightness slider
brightness_slider = Scale(frame_2, from_=0, 
            to=3, 
            resolution=0.01,
            font=Font_tuple,
            length=310,
            sliderlength=15,
            troughcolor="#A06550",
            orient=HORIZONTAL,
            label="Brightness", 
            bg="#514143",
            foreground="#C38560",
            command=image_brightness)
brightness_slider.set(1)
brightness_slider.place(anchor='center', relx=0.5, rely=0.1)

#Contrast slider.
contrast_slider = Scale(frame_2, from_=0, 
            to=3, 
            resolution=0.01,
            font=Font_tuple,
            length=310,
            sliderlength=15,
            troughcolor="#A06550",
            orient=HORIZONTAL,
            label="Contrast", 
            bg="#514143",
            foreground="#C38560",
            command=image_contrast)
contrast_slider.set(1)
contrast_slider.place(anchor='center', relx=0.5, rely=0.22)

#Sharpness slider.
sharpness_slider = Scale(frame_2, from_=-2.8, 
            to=8.5, 
            resolution=0.1,
            font=Font_tuple,
            length=310,
            sliderlength=15,
            troughcolor="#A06550",
            orient=HORIZONTAL,
            label="Sharpness", 
            bg="#514143",
            foreground="#C38560",
            command=image_sharpness)
sharpness_slider.set(1)
sharpness_slider.place(anchor='center', relx=0.5, rely=0.34)

#Saturation slider.
saturation_slider = Scale(frame_2, from_=0, 
            to=3, 
            resolution=0.01,
            font=Font_tuple,
            length=310,
            sliderlength=15,
            troughcolor="#A06550",
            orient=HORIZONTAL,
            label="Saturation", 
            bg="#514143",
            foreground="#C38560",
            command=image_saturation)
saturation_slider.set(1)
saturation_slider.place(anchor='center', relx=0.5, rely=0.46)


display = Label(frame_3,bg="#6A5A5D")
display.place(anchor='center', relx=0.5, rely=0.5)

window.mainloop()