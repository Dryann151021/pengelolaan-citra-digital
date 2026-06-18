import PySimpleGUI as sg
import os.path
from PIL import Image
from processing_list import *

# Color Palette
BG_DARK = "#0F0F13"
BG_PANEL = "#1A1A24"
BG_CARD = "#22222F"
ACCENT_BLUE = "#4F8EF7"
ACCENT_GREEN = "#3DD68C"
ACCENT_RED = "#F75F5F"
TEXT_PRIMARY = "#E8E8F0"
TEXT_MUTED = "#7070A0"
BORDER = "#2E2E42"

# Custom Theme
sg.theme_add_new(
    "PhotoEditor",
    {
        "BACKGROUND": BG_DARK,
        "TEXT": TEXT_PRIMARY,
        "INPUT": BG_CARD,
        "TEXT_INPUT": TEXT_PRIMARY,
        "SCROLL": BORDER,
        "BUTTON": (TEXT_PRIMARY, BG_CARD),
        "PROGRESS": (ACCENT_BLUE, BORDER),
        "BORDER": 0,
        "SLIDER_DEPTH": 0,
        "PROGRESS_DEPTH": 0,
    },
)
sg.theme("PhotoEditor")
sg.set_options(font=("Helvetica", 10))


# Helper
def slider_row(label, key, val_key, rng, default, res):
    """Slider row: label | slider | live value"""
    return [
        sg.Text(
            label,
            size=(11, 1),
            font=("Helvetica", 9),
            text_color=TEXT_PRIMARY,
            background_color=BG_PANEL,
            pad=((8, 2), (3, 3)),
        ),
        sg.Slider(
            range=rng,
            default_value=default,
            resolution=res,
            orientation="h",
            enable_events=True,
            disable_number_display=True,
            size=(12, 14),
            key=key,
            background_color=BG_PANEL,
            pad=((0, 2), (3, 3)),
        ),
        sg.Text(
            f"{default}",
            size=(5, 1),
            key=val_key,
            font=("Helvetica", 9, "bold"),
            text_color=ACCENT_BLUE,
            background_color=BG_PANEL,
            justification="right",
            pad=((0, 8), (3, 3)),
        ),
    ]


def filter_btn(label, key, pad=((8, 4), (3, 3))):
    return sg.Button(
        label,
        key=key,
        size=(11, 1),
        button_color=(TEXT_PRIMARY, BG_CARD),
        border_width=0,
        pad=pad,
    )


def section_label(text):
    return sg.Text(
        text,
        font=("Helvetica", 8, "bold"),
        text_color=TEXT_MUTED,
        background_color=BG_PANEL,
        pad=((8, 8), (10, 5)),
    )


# Left Panel
left_sidebar = [
    [section_label("📁  FILES")],
    [
        sg.In(
            size=(17, 1),
            key="ImgFolder",
            enable_events=True,
            background_color=BG_CARD,
            text_color=TEXT_PRIMARY,
            pad=((8, 0), (0, 4)),
        ),
        sg.FolderBrowse(button_color=(TEXT_PRIMARY, ACCENT_BLUE), pad=((2, 8), (0, 4))),
    ],
    [
        sg.Listbox(
            values=[],
            enable_events=True,
            size=(24, 13),
            key="ImgList",
            background_color=BG_CARD,
            text_color=TEXT_PRIMARY,
            highlight_background_color=ACCENT_BLUE,
            highlight_text_color="#FFFFFF",
            pad=((8, 8), (0, 8)),
            no_scrollbar=False,
        )
    ],
    [sg.HorizontalSeparator(color=BORDER, pad=((8, 8), (4, 4)))],
    [section_label("📊  INFO")],
    [
        sg.Text(
            "—",
            size=(22, 1),
            key="ImgSize",
            font=("Helvetica", 9),
            text_color=TEXT_PRIMARY,
            background_color=BG_PANEL,
            pad=((8, 8), (2, 2)),
        )
    ],
    [
        sg.Text(
            "—",
            size=(22, 1),
            key="ImgColorDepth",
            font=("Helvetica", 9),
            text_color=TEXT_PRIMARY,
            background_color=BG_PANEL,
            pad=((8, 8), (2, 8)),
        )
    ],
]

# Center Panel
before_col = sg.Column(
    [
        [
            sg.Text(
                "BEFORE",
                font=("Helvetica", 8, "bold"),
                text_color=TEXT_MUTED,
                background_color=BG_DARK,
                justification="center",
                expand_x=True,
            )
        ],
        [
            sg.Image(
                key="ImgInputViewer", background_color=BG_DARK, pad=((8, 8), (4, 4))
            )
        ],
    ],
    background_color=BG_DARK,
    element_justification="center",
    expand_x=True,
    expand_y=True,
)

after_col = sg.Column(
    [
        [
            sg.Text(
                "AFTER",
                font=("Helvetica", 8, "bold"),
                text_color=ACCENT_BLUE,
                background_color=BG_DARK,
                justification="center",
                expand_x=True,
            )
        ],
        [
            sg.Image(
                key="ImgOutputViewer", background_color=BG_DARK, pad=((8, 8), (4, 4))
            )
        ],
    ],
    background_color=BG_DARK,
    element_justification="center",
    expand_x=True,
    expand_y=True,
)

canvas_area = [
    [before_col, sg.VSeparator(color=BORDER, pad=((10, 10), (0, 0))), after_col],
    [
        sg.Push(background_color=BG_DARK),
        sg.Text(
            "",
            size=(60, 1),
            key="ImgProcessingType",
            font=("Helvetica", 9, "bold"),
            text_color=ACCENT_BLUE,
            background_color=BG_DARK,
            justification="center",
        ),
        sg.Push(background_color=BG_DARK),
    ],
    [
        sg.Push(background_color=BG_DARK),
        sg.Text(
            "",
            size=(70, 1),
            key="FilepathImgInput",
            font=("Helvetica", 8),
            text_color=TEXT_MUTED,
            background_color=BG_DARK,
            justification="center",
        ),
        sg.Push(background_color=BG_DARK),
    ],
]

#  Right Panel
right_panel = [
    [section_label("ADJUSTMENTS")],
    slider_row("Brightness", "SliderBrightness", "ValBrightness", (0.2, 2.0), 1.0, 0.2),
    slider_row("Contrast", "SliderContrast", "ValContrast", (0.2, 2.0), 1.0, 0.2),
    slider_row("Sharpening", "SliderSharp", "ValSharp", (0.0, 4.0), 1.0, 0.2),
    slider_row("Blur Radius", "SliderBlur", "ValBlur", (0, 20), 0, 1),
    slider_row("Noise", "SliderNoise", "ValNoise", (0, 100), 0, 5),
    slider_row("Temperature", "SliderTemp", "ValTemp", (-100, 100), 0, 5),
    slider_row("Threshold", "SliderThreshold", "ValThreshold", (0, 255), 127, 1),
    [sg.HorizontalSeparator(color=BORDER, pad=((8, 8), (8, 4)))],
    [section_label("FILTERS")],
    [
        filter_btn("Grayscale", "ImgGrayscale"),
        filter_btn("Negative", "ImgNegative", pad=((4, 8), (3, 3))),
    ],
    [
        filter_btn("Edge Detect", "ImgEdgeDetect"),
        filter_btn("Vintage", "ImgVintage", pad=((4, 8), (3, 3))),
    ],
    [
        filter_btn("Emboss", "ImgEmboss"),
        filter_btn("Posterize", "ImgPosterize", pad=((4, 8), (3, 3))),
    ],
    [
        filter_btn("Dilation", "ImgDilation"),
        filter_btn("Erosion", "ImgErosion", pad=((4, 8), (3, 3))),
    ],
    [sg.HorizontalSeparator(color=BORDER, pad=((8, 8), (4, 4)))],
    [section_label("✂  CROP  (px)")],
    [
        sg.Text(
            "X",
            size=(2, 1),
            background_color=BG_PANEL,
            text_color=TEXT_MUTED,
            pad=((8, 0), (2, 2)),
        ),
        sg.Input(
            "0",
            size=(5, 1),
            key="CropX",
            background_color=BG_CARD,
            text_color=TEXT_PRIMARY,
        ),
        sg.Text(
            "Y",
            size=(2, 1),
            background_color=BG_PANEL,
            text_color=TEXT_MUTED,
            pad=((4, 0), (2, 2)),
        ),
        sg.Input(
            "0",
            size=(5, 1),
            key="CropY",
            background_color=BG_CARD,
            text_color=TEXT_PRIMARY,
        ),
    ],
    [
        sg.Text(
            "W",
            size=(2, 1),
            background_color=BG_PANEL,
            text_color=TEXT_MUTED,
            pad=((8, 0), (2, 2)),
        ),
        sg.Input(
            "100",
            size=(5, 1),
            key="CropW",
            background_color=BG_CARD,
            text_color=TEXT_PRIMARY,
        ),
        sg.Text(
            "H",
            size=(2, 1),
            background_color=BG_PANEL,
            text_color=TEXT_MUTED,
            pad=((4, 0), (2, 2)),
        ),
        sg.Input(
            "100",
            size=(5, 1),
            key="CropH",
            background_color=BG_CARD,
            text_color=TEXT_PRIMARY,
        ),
    ],
    [
        sg.Button(
            "✂  Crop Image",
            key="ImgCrop",
            size=(20, 1),
            button_color=(TEXT_PRIMARY, BG_CARD),
            border_width=0,
            pad=((8, 8), (8, 10)),
        )
    ],
    [sg.HorizontalSeparator(color=BORDER, pad=((8, 8), (8, 4)))],
    [section_label("ROTATE")],
    [
        filter_btn("↻  +90°", "ImgRotateClockwise"),
        filter_btn("↺  −90°", "ImgRotateCounterClockwise", pad=((4, 8), (3, 6))),
    ],
    [sg.HorizontalSeparator(color=BORDER, pad=((8, 8), (6, 4)))],
    [section_label("3D ROTATE")],
    slider_row("Tilt (X)", "Slider3DX", "Val3DX", (-60, 60), 0, 1),
    slider_row("Pan  (Y)", "Slider3DY", "Val3DY", (-60, 60), 0, 1),
]

# Top Toolbar
toolbar = [
    sg.Text(
        "🖼  MetamorPhoto",
        font=("Helvetica", 13, "bold"),
        text_color=ACCENT_BLUE,
        background_color=BG_DARK,
        pad=((16, 8), (10, 10)),
    ),
    sg.Push(background_color=BG_DARK),
    sg.Button(
        "  💾  Save  ",
        key="ImgSave",
        button_color=(BG_DARK, ACCENT_GREEN),
        font=("Helvetica", 10, "bold"),
        border_width=0,
        pad=((4, 4), (8, 8)),
    ),
    sg.Button(
        "  ↺  Reset  ",
        key="ImgReset",
        button_color=(BG_DARK, ACCENT_RED),
        font=("Helvetica", 10, "bold"),
        border_width=0,
        pad=((4, 16), (8, 8)),
    ),
]

# full layout
layout = [
    toolbar,
    [sg.HorizontalSeparator(color=BORDER)],
    [
        sg.Column(
            left_sidebar,
            background_color=BG_PANEL,
            vertical_alignment="top",
            size=(215, 350),
        ),
        sg.VSeparator(color=BORDER),
        sg.Column(
            canvas_area,
            background_color=BG_DARK,
            element_justification="center",
            vertical_alignment="top",
            expand_x=True,
            expand_y=True,
        ),
        sg.VSeparator(color=BORDER),
        sg.Column(
            right_panel,
            background_color=BG_PANEL,
            vertical_alignment="top",
            size=(250, 650),
        ),
    ],
]

window = sg.Window(
    "MetamorPhoto",
    layout,
    background_color=BG_DARK,
    margins=(0, 0),
    finalize=True,
    resizable=True,
)
window.bind("<Configure>", "WindowResized")

# Constants & State
_SIDEBAR_W = 520
_TOOLBAR_H = 90
MAX_W, MAX_H = 400, 300
last_win_size = (0, 0)

TEMP_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "temp")
os.makedirs(TEMP_DIR, exist_ok=True)

filename_out = os.path.join(TEMP_DIR, "out.png")
temp_input = os.path.join(TEMP_DIR, "temp_input.png")

rotate_deg = 0
brightness_level = 1.0
contrast_level = 1.0
blur_radius = 0
threshold_value = 127

img_input = None
coldepth = 24
img_output = None


def update_canvas_size():
    """Hitung ulang MAX_W/MAX_H dari ukuran window saat ini."""
    global MAX_W, MAX_H
    win_w, win_h = window.size
    # Canvas tersisa setelah kedua sidebar, bagi dua untuk before/after
    avail_w = max(160, (win_w - _SIDEBAR_W) // 2 - 20)
    avail_h = max(120, win_h - _TOOLBAR_H - 60)
    MAX_W, MAX_H = avail_w, avail_h


def resize_for_display(img, save_path):
    w, h = img.size
    scale = min(MAX_W / w, MAX_H / h, 1.0)
    new_w, new_h = int(w * scale), int(h * scale)
    img.resize((new_w, new_h), Image.LANCZOS).save(save_path)
    return save_path


# Event Loop
while True:
    event, values = window.read()

    if event in (sg.WIN_CLOSED, "Exit"):
        break

    # Window resized
    if event == "WindowResized":
        curr_size = window.size
        if curr_size != last_win_size:
            last_win_size = curr_size
            try:
                update_canvas_size()
                if img_input is not None:
                    resize_for_display(img_input.convert("RGB"), temp_input)
                    window["ImgInputViewer"].update(filename=temp_input)
                if img_output is not None:
                    out_img = (
                        img_output.convert("RGB")
                        if img_output.mode not in ("RGB", "L")
                        else img_output
                    )
                    resize_for_display(out_img, filename_out)
                    window["ImgOutputViewer"].update(filename=filename_out)
                else:
                    if img_input is not None:
                        window["ImgOutputViewer"].update(filename=temp_input)
            except Exception:
                pass

    # Open folder
    elif event == "ImgFolder":
        folder = values["ImgFolder"]
        try:
            file_list = os.listdir(folder)
        except Exception:
            file_list = []
        fnames = [
            f
            for f in file_list
            if os.path.isfile(os.path.join(folder, f))
            and f.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".bmp"))
        ]
        window["ImgList"].update(fnames)

    # Select image
    elif event == "ImgList":
        try:
            filename = os.path.join(values["ImgFolder"], values["ImgList"][0])
            window["FilepathImgInput"].update(filename)

            img_input = Image.open(filename)
            img_input_rgb = img_input.convert("RGB")

            # Reset output state and sliders when loading a new image
            img_output = None
            rotate_deg = 0
            brightness_level = 1.0
            contrast_level = 1.0

            window["SliderBrightness"].update(1.0)
            window["SliderContrast"].update(1.0)
            window["SliderSharp"].update(1.0)
            window["SliderBlur"].update(0)
            window["SliderNoise"].update(0)
            window["SliderTemp"].update(0)
            window["SliderThreshold"].update(127)
            window["Slider3DX"].update(0)
            window["Slider3DY"].update(0)

            window["ValBrightness"].update("1.0")
            window["ValContrast"].update("1.0")
            window["ValSharp"].update("1.0")
            window["ValBlur"].update("0")
            window["ValNoise"].update("0")
            window["ValTemp"].update("0")
            window["ValThreshold"].update("127")
            window["Val3DX"].update("0°")
            window["Val3DY"].update("0°")

            window["CropX"].update("0")
            window["CropY"].update("0")
            window["CropW"].update("100")
            window["CropH"].update("100")

            resize_for_display(img_input_rgb, temp_input)
            window["ImgInputViewer"].update(filename=temp_input)
            window["ImgProcessingType"].update("Original")
            window["ImgOutputViewer"].update(filename=temp_input)

            img_width, img_height = img_input.size
            window["ImgSize"].update(f"Size: {img_width} × {img_height} px")

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
            coldepth = mode_to_coldepth.get(img_input.mode, 24)
            window["ImgColorDepth"].update(f"Depth: {coldepth}-bit")
        except Exception as e:
            print(e)

    # Negative
    elif event == "ImgNegative":
        try:
            window["ImgProcessingType"].update("Negative")
            img_output = ImgNegative(img_input, coldepth)
            resize_for_display(img_output, filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except Exception:
            pass

    # Rotate Clockwise
    elif event == "ImgRotateClockwise":
        try:
            rotate_deg = (rotate_deg + 90) % 360
            window["ImgProcessingType"].update(f"Rotate +{rotate_deg}°")
            img_output = ImgRotate(img_input, coldepth, rotate_deg, "C")
            resize_for_display(img_output, filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except Exception:
            pass

    # Rotate Counter Clockwise
    elif event == "ImgRotateCounterClockwise":
        try:
            rotate_deg = (rotate_deg - 90) % 360
            window["ImgProcessingType"].update(f"Rotate −{(360 - rotate_deg) % 360}°")
            img_output = ImgRotate(img_input, coldepth, rotate_deg, "C")
            resize_for_display(img_output, filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except Exception:
            pass

    # Grayscale
    elif event == "ImgGrayscale":
        try:
            window["ImgProcessingType"].update("Grayscale")
            img_output = ImgGrayscale(img_input, coldepth)
            resize_for_display(img_output, filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except Exception:
            pass

    # Brightness / Contrast
    elif event in ("SliderBrightness", "SliderContrast"):
        try:
            brightness_level = values["SliderBrightness"]
            contrast_level = values["SliderContrast"]
            window["ValBrightness"].update(f"{brightness_level:.1f}")
            window["ValContrast"].update(f"{contrast_level:.1f}")
            window["ImgProcessingType"].update(
                f"Brightness {brightness_level:.1f}x  ·  Contrast {contrast_level:.1f}x"
            )
            img_output = ImgBrightnessContrast(
                img_input, coldepth, brightness_level, contrast_level
            )
            resize_for_display(img_output, filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except Exception:
            pass

    # Blur
    elif event == "SliderBlur":
        try:
            blur_radius = int(values["SliderBlur"])
            window["ValBlur"].update(str(blur_radius))
            window["ImgProcessingType"].update(f"Gaussian Blur  r = {blur_radius}")
            img_output = ImgBlur(img_input, coldepth, blur_radius)
            resize_for_display(img_output, filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except Exception:
            pass

    # Edge Detection
    elif event == "ImgEdgeDetect":
        try:
            window["ImgProcessingType"].update("Edge Detection (Sobel)")
            img_output = ImgEdgeDetection(img_input, coldepth)
            resize_for_display(img_output, filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except Exception:
            pass

    # Threshold
    elif event == "SliderThreshold":
        try:
            threshold_value = int(values["SliderThreshold"])
            window["ValThreshold"].update(str(threshold_value))
            window["ImgProcessingType"].update(f"Threshold  T = {threshold_value}")
            img_output = ImgThresholding(img_input, coldepth, threshold_value)
            resize_for_display(img_output, filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except Exception:
            pass

    # Erosion
    elif event == "ImgErosion":
        try:
            window["ImgProcessingType"].update("Erosion")
            img_output = ImgErosionDilation(
                img_input, coldepth, operation="erosion", kernel_size=5, iterations=1
            )
            resize_for_display(img_output, filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except Exception:
            pass

    # Dilation
    elif event == "ImgDilation":
        try:
            window["ImgProcessingType"].update("Dilation")
            img_output = ImgErosionDilation(
                img_input, coldepth, operation="dilation", kernel_size=5, iterations=1
            )
            resize_for_display(img_output, filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except Exception:
            pass

    # Posterize
    elif event == "ImgPosterize":
        try:
            window["ImgProcessingType"].update("Posterize")
            img_output = ImgPosterize(img_input, coldepth, levels=4)
            resize_for_display(img_output, filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except Exception:
            pass

    # Vintage
    elif event == "ImgVintage":
        try:
            window["ImgProcessingType"].update("Vintage / Sepia")
            img_output = ImgVintage(img_input, coldepth)
            resize_for_display(img_output, filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except Exception:
            pass

    # Emboss
    elif event == "ImgEmboss":
        try:
            window["ImgProcessingType"].update("Emboss")
            img_output = ImgEmboss(img_input, coldepth)
            resize_for_display(img_output, filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except Exception:
            pass

    # ── Sharpening ───────────────────────────────────
    elif event == "SliderSharp":
        try:
            sharp_amount = values["SliderSharp"]
            window["ValSharp"].update(f"{sharp_amount:.1f}")
            window["ImgProcessingType"].update(f"Sharpening  {sharp_amount:.1f}x")
            img_output = ImgSharpening(img_input, coldepth, sharp_amount)
            resize_for_display(img_output, filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except Exception:
            pass

    # Noise
    elif event == "SliderNoise":
        try:
            noise_intensity = int(values["SliderNoise"])
            window["ValNoise"].update(str(noise_intensity))
            window["ImgProcessingType"].update(f"Gaussian Noise  σ = {noise_intensity}")
            img_output = ImgGaussianNoise(img_input, coldepth, noise_intensity)
            resize_for_display(img_output, filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except Exception:
            pass

    # Temperature
    elif event == "SliderTemp":
        try:
            temp_val = int(values["SliderTemp"])
            label = f"+{temp_val}" if temp_val >= 0 else str(temp_val)
            window["ValTemp"].update(label)
            window["ImgProcessingType"].update(f"Temperature  {label}")
            img_output = ImgTemperature(img_input, coldepth, temp_val)
            resize_for_display(img_output, filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except Exception:
            pass

    # 3D Rotate
    elif event in ("Slider3DX", "Slider3DY"):
        try:
            ax = int(values["Slider3DX"])
            ay = int(values["Slider3DY"])
            window["Val3DX"].update(f"{ax:+d}°")
            window["Val3DY"].update(f"{ay:+d}°")
            window["ImgProcessingType"].update(
                f"3D Rotate  Tilt {ax:+d}°  Pan {ay:+d}°"
            )
            img_output = ImgRotate3D(img_input, coldepth, angle_x=ax, angle_y=ay)
            resize_for_display(img_output, filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except Exception:
            pass

    # Save
    elif event == "ImgSave":
        try:
            image_to_save = img_output if img_output is not None else img_input
            if image_to_save is None:
                sg.popup_error(
                    "Tidak ada gambar yang dimuat untuk disimpan!",
                    title="Error",
                    background_color=BG_CARD,
                    text_color=ACCENT_RED,
                )
                continue

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
                background_color=BG_CARD,
                text_color=TEXT_PRIMARY,
            )
            if save_path:
                image_to_save.save(save_path)
                sg.popup_ok(
                    f"Gambar berhasil disimpan:\n{save_path}",
                    title="Saved!",
                    background_color=BG_CARD,
                    text_color=TEXT_PRIMARY,
                )
        except Exception as e:
            sg.popup_error(
                f"Gagal menyimpan: {e}",
                title="Error",
                background_color=BG_CARD,
                text_color=ACCENT_RED,
            )

    # Crop
    elif event == "ImgCrop":
        try:
            x = int(values["CropX"])
            y = int(values["CropY"])
            w = int(values["CropW"])
            h = int(values["CropH"])
            img_w, img_h = img_input.size
            window["ImgProcessingType"].update(
                f"Crop  ({x}, {y})  {w} × {h} px  [original: {img_w} × {img_h}]"
            )
            img_output = ImgCrop(img_input, coldepth, x, y, w, h)
            resize_for_display(img_output, filename_out)
            window["ImgOutputViewer"].update(filename=filename_out)
        except ValueError:
            sg.popup_error(
                "Input crop harus berupa angka!",
                title="Error",
                background_color=BG_CARD,
                text_color=ACCENT_RED,
            )
        except Exception as e:
            sg.popup_error(
                f"Gagal crop: {e}",
                title="Error",
                background_color=BG_CARD,
                text_color=ACCENT_RED,
            )

    # Reset
    elif event == "ImgReset":
        try:
            rotate_deg = 0
            brightness_level = 1.0
            contrast_level = 1.0

            # Reset sliders
            window["SliderBrightness"].update(1.0)
            window["SliderContrast"].update(1.0)
            window["SliderSharp"].update(1.0)
            window["SliderBlur"].update(0)
            window["SliderNoise"].update(0)
            window["SliderTemp"].update(0)
            window["SliderThreshold"].update(127)
            window["Slider3DX"].update(0)
            window["Slider3DY"].update(0)

            # Reset live value displays
            window["ValBrightness"].update("1.0")
            window["ValContrast"].update("1.0")
            window["ValSharp"].update("1.0")
            window["ValBlur"].update("0")
            window["ValNoise"].update("0")
            window["ValTemp"].update("0")
            window["ValThreshold"].update("127")
            window["Val3DX"].update("0°")
            window["Val3DY"].update("0°")

            # Reset crop inputs
            window["CropX"].update("0")
            window["CropY"].update("0")
            window["CropW"].update("100")
            window["CropH"].update("100")

            window["ImgProcessingType"].update("Reset to Original")
            if img_input is not None:
                img_input_rgb = img_input.convert("RGB")
                resize_for_display(img_input_rgb, filename_out)
                window["ImgOutputViewer"].update(filename=filename_out)
        except Exception:
            pass

window.close()
