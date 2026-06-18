import PySimpleGUI as sg
import os.path
from PIL import Image
from processing_list import *

# Set theme
sg.theme("DarkGrey14")
sg.set_options(font=("Arial", 10))

# Kolom Area No 1: Area open folder and select image
file_list_column = [
    [
        sg.Text("Open Image Folder :"),
    ],
    [
        sg.In(size=(20, 1), enable_events=True, key="ImgFolder"),
        sg.FolderBrowse(),
    ],
    [
        sg.Text("Choose an image from list :"),
    ],
    [sg.Listbox(values=[], enable_events=True, size=(30, 20), key="ImgList")],
]

# Kolom Area No 2: Area viewer image input dan output
image_viewer_column = [
    [sg.Text("Image Input :")],
    [sg.Text(size=(40, 1), key="FilepathImgInput")],
    [sg.Image(key="ImgInputViewer")],
]

image_viewer_column2 = [
    [sg.Text("Image Processing Output:")],
    [sg.Text(size=(40, 1), key="ImgProcessingType")],
    [sg.Image(key="ImgOutputViewer")],
]

# Kolom Area No 3: Area Image info dan Tombol list of processing
img_info_frame = [
    [
        sg.Text(size=(20, 1), key="ImgSize"),
    ],
    [
        sg.Text(size=(20, 1), key="ImgColorDepth"),
    ],
]

crop_frame = [
    [sg.Text("Koordinat & Ukuran Crop (px):", font=("Arial", 9))],
    [
        sg.Text("X", size=(2, 1)),
        sg.Input("0", size=(6, 1), key="CropX"),
        sg.Text("Y", size=(2, 1)),
        sg.Input("0", size=(6, 1), key="CropY"),
    ],
    [
        sg.Text("W", size=(2, 1)),
        sg.Input("100", size=(6, 1), key="CropW"),
        sg.Text("H", size=(2, 1)),
        sg.Input("100", size=(6, 1), key="CropH"),
    ],
    [sg.Text("(gunakan ukuran piksel asli)", font=("Arial", 8))],
    [sg.Button("✂ Crop", size=(25, 1), key="ImgCrop")],
]

list_of_processing_frame = [
    [
        sg.Text("Brightness", size=(11, 1)),
        sg.Slider(
            range=(0.2, 2.0),
            default_value=1.0,
            resolution=0.2,
            orientation="h",
            enable_events=True,
            disable_number_display=True,
            size=(12, 12),
            key="SliderBrightness",
        ),
    ],
    [
        sg.Text("Contrast", size=(11, 1)),
        sg.Slider(
            range=(0.2, 2.0),
            default_value=1.0,
            resolution=0.2,
            orientation="h",
            enable_events=True,
            disable_number_display=True,
            size=(12, 12),
            key="SliderContrast",
        ),
    ],
    [
        sg.Text("Sharpening", size=(11, 1)),
        sg.Slider(
            range=(0.0, 4.0),
            default_value=1.0,
            resolution=0.2,
            orientation="h",
            enable_events=True,
            disable_number_display=True,
            size=(12, 12),
            key="SliderSharp",
        ),
    ],
    [
        sg.Text("Blur Radius", size=(11, 1)),
        sg.Slider(
            range=(0, 20),
            default_value=0,
            resolution=1,
            orientation="h",
            enable_events=True,
            disable_number_display=True,
            size=(12, 12),
            key="SliderBlur",
        ),
    ],
    [
        sg.Text("Noise", size=(11, 1)),
        sg.Slider(
            range=(0, 100),
            default_value=0,
            resolution=5,
            orientation="h",
            enable_events=True,
            disable_number_display=True,
            size=(12, 12),
            key="SliderNoise",
        ),
    ],
    [
        sg.Text("Temperature", size=(11, 1)),
        sg.Slider(
            range=(-100, 100),
            default_value=0,
            resolution=5,
            orientation="h",
            enable_events=True,
            disable_number_display=True,
            size=(12, 12),
            key="SliderTemp",
        ),
    ],
    [
        sg.Text("Thresholding", size=(11, 1)),
        sg.Slider(
            range=(0, 255),
            default_value=127,
            resolution=1,
            orientation="h",
            enable_events=True,
            disable_number_display=True,
            size=(12, 12),
            key="SliderThreshold",
        ),
    ],
    [
        sg.Button("Rotate 90°", size=(10, 1), key="ImgRotateClockwise"),
        sg.Button("Rotate -90°", size=(10, 1), key="ImgRotateCounterClockwise"),
    ],
    [
        sg.Button("Negative", size=(25, 1), key="ImgNegative"),
    ],
    [
        sg.Button("Grayscale", size=(25, 1), key="ImgGrayscale"),
    ],
    [
        sg.Button("Edge Detection", size=(25, 1), key="ImgEdgeDetect"),
    ],
    [
        sg.Button("Vintage", size=(25, 1), key="ImgVintage"),
    ],
    [
        sg.Button("Emboss", size=(25, 1), key="ImgEmboss"),
    ],
    [
        sg.Button("Erosion", size=(10, 1), key="ImgErosion"),
        sg.Button("Dilation", size=(10, 1), key="ImgDilation"),
    ],
]

save_reset_frame = [
    [sg.Button("Save", size=(25, 1), button_color=("white", "green"), key="ImgSave")],
    [sg.Button("Reset", size=(25, 1), button_color=("white", "red"), key="ImgReset")],
]

# Gabung Layout List Processing
list_processing = [
    [sg.Frame("Image Information", img_info_frame)],
    [sg.Frame("Crop", crop_frame, element_justification="center")],
    [
        sg.Frame(
            "List of Processing",
            list_of_processing_frame,
            element_justification="center",
        )
    ],
    [sg.Frame("", save_reset_frame, border_width=0)],
]

# Gabung Full layout
layout = [
    [
        sg.Column(file_list_column),
        sg.VSeparator(color="#1B1C21", pad=(5, 5)),
        sg.Column(image_viewer_column),
        sg.Column(image_viewer_column2),
        sg.VSeparator(color="#1B1C21", pad=(5, 5)),
        sg.Column(list_processing),
    ]
]

window = sg.Window("Mini Image Editor", layout)

MAX_W, MAX_H = 420, 280


def resize_for_display(img, save_path):
    w, h = img.size
    scale = min(MAX_W / w, MAX_H / h, 1.0)
    new_w, new_h = int(w * scale), int(h * scale)
    img_resized = img.resize((new_w, new_h), Image.LANCZOS)
    img_resized.save(save_path)
    return save_path


TEMP_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "temp")
os.makedirs(TEMP_DIR, exist_ok=True)

filename_out = os.path.join(TEMP_DIR, "out.png")
temp_input = os.path.join(TEMP_DIR, "temp_input.png")
rotate_deg = 0
brightness_level = 1.0
contrast_level = 1.0
blur_radius = 5
threshold_value = 127

# Run the Event Loop
while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break

    # Folder name was filled in, make a list of files in the folder
    if event == "ImgFolder":
        folder = values["ImgFolder"]
        try:
            # Get list of files in folder
            file_list = os.listdir(folder)
        except:
            file_list = []

        fnames = [
            f
            for f in file_list
            if os.path.isfile(os.path.join(folder, f))
            and f.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".bmp"))
        ]
        window["ImgList"].update(fnames)

    elif event == "ImgList":
        try:
            filename = os.path.join(values["ImgFolder"], values["ImgList"][0])
            window["FilepathImgInput"].update(filename)

            img_input = Image.open(filename)
            img_input_rgb = img_input.convert("RGB")

            resize_for_display(img_input_rgb, temp_input)
            window["ImgInputViewer"].update(filename=temp_input)
            window["ImgProcessingType"].update(filename)
            window["ImgOutputViewer"].update(filename=temp_input)

            img_width, img_height = img_input.size
            window["ImgSize"].update(f"Size: {img_width} x {img_height} px")

            mode_to_coldepth = {
                "1": 1,
                "L": 8,
                "P": 8,
                "RGB": 24,
                "RGBA": 32,
                "CMYK": 32,
                "YCbCr": 24,
                "LAB": 24,
                "HSV": 24,
                "I": 32,
                "F": 32,
            }
            coldepth = mode_to_coldepth[img_input.mode]
            window["ImgColorDepth"].update(f"Depth: {coldepth} bit")
        except Exception as e:
            print(e)

    elif event == "ImgNegative":
        try:
            window["ImgProcessingType"].update("Image Negative")
            img_output = ImgNegative(img_input, coldepth)
            resize_for_display(img_output, filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except:
            pass

    elif event == "ImgRotateClockwise":
        try:
            rotate_deg = (rotate_deg + 90) % 360
            window["ImgProcessingType"].update("Image Rotate")
            img_output = ImgRotate(img_input, coldepth, rotate_deg, "C")
            resize_for_display(img_output, filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except:
            pass

    elif event == "ImgRotateCounterClockwise":
        try:
            rotate_deg = (rotate_deg - 90) % 360
            window["ImgProcessingType"].update("Image Rotate")
            img_output = ImgRotate(img_input, coldepth, rotate_deg, "C")
            resize_for_display(img_output, filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except:
            pass

    elif event == "ImgGrayscale":
        try:
            window["ImgProcessingType"].update("Image Grayscale")
            img_output = ImgGrayscale(img_input, coldepth)
            resize_for_display(img_output, filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except:
            pass

    elif event == "SliderBrightness" or event == "SliderContrast":
        try:
            brightness_level = values["SliderBrightness"]
            contrast_level = values["SliderContrast"]
            window["ImgProcessingType"].update(
                f"Brightness: {brightness_level:.1f}x | Contrast: {contrast_level:.1f}x"
            )
            img_output = ImgBrightnessContrast(
                img_input, coldepth, brightness_level, contrast_level
            )
            resize_for_display(img_output, filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except:
            pass

    elif event == "SliderBlur":
        try:
            blur_radius = int(values["SliderBlur"])
            window["ImgProcessingType"].update(f"Gaussian Blur (radius={blur_radius})")
            img_output = ImgBlur(img_input, coldepth, blur_radius)
            resize_for_display(img_output, filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except:
            pass

    elif event == "ImgEdgeDetect":
        try:
            window["ImgProcessingType"].update("Edge Detection (Sobel)")
            img_output = ImgEdgeDetection(img_input, coldepth)
            resize_for_display(img_output, filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except:
            pass

    elif event == "SliderThreshold":
        try:
            threshold_value = int(values["SliderThreshold"])
            window["ImgProcessingType"].update(f"Thresholding (T={threshold_value})")
            img_output = ImgThresholding(img_input, coldepth, threshold_value)
            resize_for_display(img_output, filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except:
            pass

    elif event == "ImgErosion":
        try:
            window["ImgProcessingType"].update("Erosion")
            img_output = ImgErosionDilation(
                img_input, coldepth, operation="erosion", kernel_size=5, iterations=1
            )
            resize_for_display(img_output, filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except:
            pass

    elif event == "ImgDilation":
        try:
            window["ImgProcessingType"].update("Dilation")
            img_output = ImgErosionDilation(
                img_input, coldepth, operation="dilation", kernel_size=5, iterations=1
            )
            resize_for_display(img_output, filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except:
            pass

    elif event == "ImgVintage":
        try:
            window["ImgProcessingType"].update("Vintage / Sepia")
            img_output = ImgVintage(img_input, coldepth)
            resize_for_display(img_output, filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except:
            pass

    elif event == "ImgEmboss":
        try:
            window["ImgProcessingType"].update("Emboss")
            img_output = ImgEmboss(img_input, coldepth)
            resize_for_display(img_output, filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except:
            pass

    elif event == "SliderSharp":
        try:
            sharp_amount = values["SliderSharp"]
            window["ImgProcessingType"].update(f"Sharpening: {sharp_amount:.1f}x")
            img_output = ImgSharpening(img_input, coldepth, sharp_amount)
            resize_for_display(img_output, filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except:
            pass

    elif event == "SliderNoise":
        try:
            noise_intensity = int(values["SliderNoise"])
            window["ImgProcessingType"].update(
                f"Gaussian Noise (intensity={noise_intensity})"
            )
            img_output = ImgGaussianNoise(img_input, coldepth, noise_intensity)
            resize_for_display(img_output, filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except:
            pass

    elif event == "SliderTemp":
        try:
            temp_val = int(values["SliderTemp"])
            label = (
                f"Temperature: +{temp_val}"
                if temp_val >= 0
                else f"Temperature: {temp_val}"
            )
            window["ImgProcessingType"].update(label)
            img_output = ImgTemperature(img_input, coldepth, temp_val)
            resize_for_display(img_output, filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except:
            pass

    elif event == "ImgSave":
        try:
            save_path = sg.popup_get_file(
                "Simpan gambar output sebagai...",
                title="Save Image",
                save_as=True,
                default_extension=".png",
                file_types=(
                    ("PNG", "*.png"),
                    ("JPEG", "*.jpg *.jpeg"),
                    ("BMP", "*.bmp"),
                    ("All", "*.*"),
                ),
            )
            if save_path:
                img_output.save(save_path)
                sg.popup_ok(
                    f"Gambar berhasil disimpan ke:\n{save_path}",
                    title="Simpan Berhasil",
                )
        except Exception as e:
            sg.popup_error(f"Gagal menyimpan: {e}", title="Error Save")

    elif event == "ImgCrop":
        try:
            x = int(values["CropX"])
            y = int(values["CropY"])
            w = int(values["CropW"])
            h = int(values["CropH"])
            img_w, img_h = img_input.size
            window["ImgProcessingType"].update(
                f"Crop: ({x},{y}) {w}x{h} px  [asli: {img_w}x{img_h}]"
            )
            img_output = ImgCrop(img_input, coldepth, x, y, w, h)
            resize_for_display(img_output, filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except ValueError:
            sg.popup_error("Input crop harus berupa angka!", title="Error Crop")
        except Exception as e:
            sg.popup_error(f"Gagal crop: {e}", title="Error Crop")

    elif event == "ImgReset":
        try:
            rotate_deg = 0
            brightness_level = 1.0
            contrast_level = 1.0

            # Reset semua slider ke nilai default
            window["SliderBrightness"].update(1.0)
            window["SliderContrast"].update(1.0)
            window["SliderSharp"].update(1.0)
            window["SliderBlur"].update(0)
            window["SliderNoise"].update(0)
            window["SliderTemp"].update(0)
            window["SliderThreshold"].update(127)

            # Reset input crop ke nilai default
            window["CropX"].update("0")
            window["CropY"].update("0")
            window["CropW"].update("100")
            window["CropH"].update("100")

            window["ImgProcessingType"].update("Reset to Original")
            img_input_rgb = img_input.convert("RGB")
            resize_for_display(img_input_rgb, filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except:
            pass

window.close()
