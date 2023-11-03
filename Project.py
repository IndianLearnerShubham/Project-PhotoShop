import tkinter as tk
from tkinter import filedialog, Menu
from PIL import Image, ImageTk, ImageEnhance, ImageFilter

class PhotoshopApp:
    def __init__(self, root):
        self.root = root
        self.root.attributes('-alpha', True)
        self.root.title("CutEx Photoshop")

        self.zoom_factor = 1.0
        self.max_zoom_factor = 3.0
        self.min_zoom_factor = 0.1
        self.start_x = None
        self.start_y = None
        self.end_x = None
        self.end_y = None
        self.contrast_value = 1.0
        self.brightness_value = 1.0

        self.canvas_frame = tk.Frame(self.root)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        self.canvas = tk.Canvas(self.canvas_frame, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(side=tk.RIGHT, padx=10)

        self.scrollbar_x = tk.Scrollbar(self.canvas_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.configure(xscrollcommand=self.scrollbar_x.set)
        
        self.scrollbar_y = tk.Scrollbar(self.root, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar_y.pack(side=tk.LEFT, fill=tk.Y)
        self.canvas.configure(yscrollcommand=self.scrollbar_y.set)

        self.crop_button = tk.Button(self.button_frame, text="Manual Crop", command=self.manual_crop)
        self.crop_button.pack(fill=tk.X)

        self.open_button = tk.Button(self.button_frame, text="Open Image", command=self.open_image)
        self.open_button.pack(fill=tk.X)

        self.zoom_in_button = tk.Button(self.button_frame, text="Zoom In", command=self.zoom_in)
        self.zoom_in_button.pack(fill=tk.X)

        self.zoom_out_button = tk.Button(self.button_frame, text="Zoom Out", command=self.zoom_out)
        self.zoom_out_button.pack(fill=tk.X)
        
        self.blur_button = tk.Button(self.button_frame, text="Blur", command=self.apply_blur)
        self.blur_button.pack(fill=tk.X)
        
        self.sharpen_button = tk.Button(self.button_frame, text="Sharpen", command=self.apply_sharpen)
        self.sharpen_button.pack(fill=tk.X)
        
        self.edge_enhance_button = tk.Button(self.button_frame, text="Edge enhance", command=self.apply_edge_enhance)
        self.edge_enhance_button.pack(fill=tk.X)
        
        self.reset_button = tk.Button(self.button_frame, text="Reset", command=self.reset_filters)
        self.reset_button.pack(fill=tk.X)

        self.contrast_slider = tk.Scale(self.button_frame, from_=0.1, to=2.0, resolution=0.1, orient=tk.HORIZONTAL, label="Contrast", command=self.adjust_contrast)
        self.contrast_slider.set(self.contrast_value)
        self.contrast_slider.pack(fill=tk.X)

        self.brightness_slider = tk.Scale(self.button_frame, from_=0.1, to=2.0, resolution=0.1, orient=tk.HORIZONTAL, label="Brightness", command=self.adjust_brightness)
        self.brightness_slider.set(self.brightness_value)
        self.brightness_slider.pack(fill=tk.X)

        self.save_button = tk.Button(self.button_frame, text="Save Image", command=self.save_image)
        self.save_button.pack(fill=tk.X)

        self.image = None
        self.image_tk = None
        self.modified_image = None
        self.original_image = None

        self.canvas.bind("<Configure>", self.on_canvas_resize)

    def open_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.jpeg *.png *.gif")])
        if file_path:
            self.image = Image.open(file_path)
            self.original_image = self.image.copy()
            self.modified_image = self.image.copy()
            self.update_image()

    def update_image(self):
        if self.modified_image:
            zoomed_width = int(self.modified_image.width * self.zoom_factor)
            zoomed_height = int(self.modified_image.height * self.zoom_factor)
            self.zoomed_image = self.modified_image.resize((zoomed_width, zoomed_height), Image.ANTIALIAS)
            self.image_tk = ImageTk.PhotoImage(self.zoomed_image)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image_tk)
            self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))

    def on_canvas_resize(self, event):
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))

    def manual_crop(self):
        self.canvas.bind("<ButtonPress-1>", self.start_cropping)
        self.canvas.bind("<B1-Motion>", self.update_crop)
        self.canvas.bind("<ButtonRelease-1>", self.end_cropping)

    def start_cropping(self, event):
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)

    def update_crop(self, event):
        self.end_x = self.canvas.canvasx(event.x)
        self.end_y = self.canvas.canvasy(event.y)
        self.canvas.delete("crop_rect")
        self.canvas.create_rectangle(self.start_x, self.start_y, self.end_x, self.end_y, outline="red", tags="crop_rect")

    def end_cropping(self, event):
        self.canvas.unbind("<ButtonPress-1>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.perform_crop()

    def perform_crop(self):
        if self.start_x is not None and self.start_y is not None and self.end_x is not None and self.end_y is not None:
            x1 = min(self.start_x, self.end_x) / self.zoom_factor
            y1 = min(self.start_y, self.end_y) / self.zoom_factor
            x2 = max(self.start_x, self.end_x) / self.zoom_factor
            y2 = max(self.start_y, self.end_y) / self.zoom_factor
            cropped_image = self.modified_image.crop((x1, y1, x2, y2))
            self.modified_image = cropped_image
            self.update_image()

    def adjust_contrast(self, value):
        self.contrast_value = float(value)
        original_image = self.original_image.copy()  # Create a copy of the original image
        contrast_enhancer = ImageEnhance.Contrast(original_image)
        self.modified_image = contrast_enhancer.enhance(self.contrast_value)
        self.update_image()

    def apply_blur(self):
        self.modified_image = self.modified_image.filter(ImageFilter.BLUR)
        self.update_image()

    def apply_sharpen(self):
        self.modified_image = self.modified_image.filter(ImageFilter.SHARPEN)
        self.update_image()

    def apply_edge_enhance(self):
        self.modified_image = self.modified_image.filter(ImageFilter.EDGE_ENHANCE)
        self.update_image()

    def reset_filters(self):
        self.modified_image = self.original_image.copy()
        self.contrast_slider.set(1.0)
        self.brightness_slider.set(1.0)
        self.update_image()
    
    def adjust_brightness(self, value):
        self.brightness_value = float(value)
        original_image = self.original_image.copy()  # Create a copy of the original image
        brightness_enhancer = ImageEnhance.Brightness(original_image)
        self.modified_image = brightness_enhancer.enhance(self.brightness_value)
        self.update_image()

    def apply_blur(self):
        self.modified_image = self.modified_image.filter(ImageFilter.BLUR)
        self.update_image()

    def apply_sharpen(self):
        self.modified_image = self.modified_image.filter(ImageFilter.SHARPEN)
        self.update_image()

    def apply_edge_enhance(self):
        self.modified_image = self.modified_image.filter(ImageFilter.EDGE_ENHANCE)
        self.update_image()

    def reset_filters(self):
        self.modified_image = self.original_image.copy()
        self.contrast_slider.set(1.0)
        self.brightness_slider.set(1.0)
        self.update_image()

    def zoom_in(self):
        if self.zoom_factor < self.max_zoom_factor:
            self.zoom_factor *= 1.2
            self.update_image()

    def zoom_out(self):
        if self.zoom_factor > self.min_zoom_factor:
            self.zoom_factor /= 1.2
            self.update_image()

    def save_image(self):
        if self.modified_image:
            file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                     filetypes=[("PNG Files", "*.png")])
            if file_path:
                self.modified_image.save(file_path)

def main():
    root = tk.Tk()
    app = PhotoshopApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

