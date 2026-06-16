from PIL import Image, ImageOps, ImageEnhance, ImageFilter
import cv2
import numpy as np


def ImgNegative(img_input, coldepth):
    # solusi 1
    # img_output = ImageOps.invert(img_input)

    # solusi 2
    if coldepth != 24:
        img_input = img_input.convert('RGB')

    img_output = Image.new('RGB', (img_input.size[0], img_input.size[1]))
    pixels = img_output.load()
    for i in range(img_output.size[0]):
        for j in range(img_output.size[1]):
            r, g, b = img_input.getpixel((i, j))
            pixels[i, j] = (255 - r, 255 - g, 255 - b)

    if coldepth == 1:
        img_output = img_output.convert("1")
    elif coldepth == 8:
        img_output = img_output.convert("L")
    else:
        img_output = img_output.convert("RGB")

    return img_output


def ImgRotate(img_input, coldepth, deg, direction):
    # solusi 1
    img_output = img_input.rotate(-deg if direction == "C" else deg, expand=True)
    
    if coldepth == 1:
        img_output = img_output.convert("1")
    elif coldepth == 8:
        img_output = img_output.convert("L")
    else:
        img_output = img_output.convert("RGB")
    
    return img_output

    # # solusi 2
    # if coldepth != 24:
    #     img_input = img_input.convert('RGB')

    # img_output = Image.new('RGB', (img_input.size[1], img_input.size[0]))
    # pixels = img_output.load()
    # for i in range(img_output.size[0]):
    #     for j in range(img_output.size[1]):
    #         if direction == "C":
    #             r, g, b = img_input.getpixel((j, img_output.size[0] - i - 1))
    #         else:
    #             r, g, b = img_input.getpixel((img_input.size[1] - j - 1, i))
    #         pixels[i, j] = (r, g, b)

    # if coldepth == 1:
    #     img_output = img_output.convert("1")
    # elif coldepth == 8:
    #     img_output = img_output.convert("L")
    # else:
    #     img_output = img_output.convert("RGB")

    # return img_output


def ImgGrayscale(img_input, coldepth):
    """Convert image to grayscale"""
    img_output = img_input.convert('L')
    return img_output


def ImgBrightnessContrast(img_input, coldepth, brightness=1.0, contrast=1.0):
    """Adjust brightness and contrast
    brightness: 0.0 to 2.0 (1.0 = normal, >1 brighter, <1 darker)
    contrast: 0.0 to 2.0 (1.0 = normal, >1 more contrast, <1 less contrast)
    """
    if coldepth != 24:
        img_input = img_input.convert('RGB')
    
    # Adjust brightness
    enhancer = ImageEnhance.Brightness(img_input)
    img_output = enhancer.enhance(brightness)
    
    # Adjust contrast
    enhancer = ImageEnhance.Contrast(img_output)
    img_output = enhancer.enhance(contrast)
    
    if coldepth == 1:
        img_output = img_output.convert("1")
    elif coldepth == 8:
        img_output = img_output.convert("L")
    else:
        img_output = img_output.convert("RGB")
    
    return img_output


def ImgBlur(img_input, coldepth, radius=5):
    """Apply Gaussian blur filter
    radius: blur radius (1-20)
    """
    if coldepth != 24:
        img_input = img_input.convert('RGB')
    
    img_output = img_input.filter(ImageFilter.GaussianBlur(radius=radius))
    
    if coldepth == 1:
        img_output = img_output.convert("1")
    elif coldepth == 8:
        img_output = img_output.convert("L")
    else:
        img_output = img_output.convert("RGB")
    
    return img_output


def ImgEdgeDetection(img_input, coldepth):
    """Detect edges using Sobel operator"""
    # Convert PIL to OpenCV
    if coldepth != 24:
        img_input = img_input.convert('RGB')
    
    img_cv = cv2.cvtColor(np.array(img_input), cv2.COLOR_RGB2BGR)
    img_gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
    
    # Apply Sobel edge detection
    sobel_x = cv2.Sobel(img_gray, cv2.CV_64F, 1, 0, ksize=3)
    sobel_y = cv2.Sobel(img_gray, cv2.CV_64F, 0, 1, ksize=3)
    
    # Magnitude
    sobel_magnitude = np.sqrt(sobel_x**2 + sobel_y**2)
    sobel_magnitude = np.clip(sobel_magnitude, 0, 255).astype(np.uint8)
    
    # Convert back to PIL
    img_output = Image.fromarray(sobel_magnitude, mode='L')
    
    if coldepth == 24:
        img_output = img_output.convert('RGB')
    elif coldepth == 1:
        img_output = img_output.convert("1")
    
    return img_output


def ImgThresholding(img_input, coldepth, threshold_value=127):
    """Convert image to binary (black and white) using threshold
    threshold_value: 0-255
    """
    # Convert to grayscale first
    if img_input.mode != 'L':
        img_gray = img_input.convert('L')
    else:
        img_gray = img_input
    
    # Apply threshold
    img_output = img_gray.point(lambda x: 255 if x > threshold_value else 0, '1')
    
    if coldepth == 24:
        img_output = img_output.convert('RGB')
    elif coldepth == 8:
        img_output = img_output.convert('L')
    
    return img_output


def ImgErosionDilation(img_input, coldepth, operation='erosion', kernel_size=5, iterations=1):
    """Apply morphological operations (erosion/dilation)
    operation: 'erosion' or 'dilation'
    kernel_size: size of structuring element (3, 5, 7, etc.)
    iterations: number of times to apply operation
    """
    # Convert PIL to OpenCV
    if img_input.mode != 'L':
        img_input = img_input.convert('L')
    
    img_cv = np.array(img_input)
    
    # Create structuring element
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_size, kernel_size))
    
    # Apply operation
    if operation.lower() == 'erosion':
        result = cv2.erode(img_cv, kernel, iterations=iterations)
    else:  # dilation
        result = cv2.dilate(img_cv, kernel, iterations=iterations)
    
    # Convert back to PIL
    img_output = Image.fromarray(result, mode='L')
    
    if coldepth == 24:
        img_output = img_output.convert('RGB')
    elif coldepth == 1:
        img_output = img_output.convert("1")
    
    return img_output


def ImgCrop(img_input, coldepth, x, y, w, h):
    """Crop gambar berdasarkan koordinat (x, y) dan ukuran (w, h).
    Koordinat menggunakan piksel asli gambar.
    """
    img_w, img_h = img_input.size

    # Clamp agar tidak keluar batas gambar
    x = max(0, min(int(x), img_w - 1))
    y = max(0, min(int(y), img_h - 1))
    w = max(1, min(int(w), img_w - x))
    h = max(1, min(int(h), img_h - y))

    # PIL crop: (left, top, right, bottom)
    img_output = img_input.crop((x, y, x + w, y + h))

    if coldepth == 1:
        img_output = img_output.convert("1")
    elif coldepth == 8:
        img_output = img_output.convert("L")
    else:
        img_output = img_output.convert("RGB")

    return img_output


def ImgSharpening(img_input, coldepth, amount=2.0):
    """Pertajam detail gambar menggunakan ImageEnhance.Sharpness.
    amount: 0.0 = blur penuh, 1.0 = asli, >1.0 = lebih tajam (maks ~3.0)
    """
    img_rgb = img_input.convert('RGB')
    enhancer = ImageEnhance.Sharpness(img_rgb)
    img_output = enhancer.enhance(amount)

    if coldepth == 1:
        img_output = img_output.convert("1")
    elif coldepth == 8:
        img_output = img_output.convert("L")
    else:
        img_output = img_output.convert("RGB")
    return img_output


def ImgVintage(img_input, coldepth):
    """Efek vintage/sepia: menggeser channel warna untuk nuansa coklat hangat."""
    img_rgb = img_input.convert('RGB')
    r_ch, g_ch, b_ch = img_rgb.split()

    r_arr = np.array(r_ch, dtype=np.float32)
    g_arr = np.array(g_ch, dtype=np.float32)
    b_arr = np.array(b_ch, dtype=np.float32)

    new_r = np.clip(r_arr * 0.393 + g_arr * 0.769 + b_arr * 0.189, 0, 255).astype(np.uint8)
    new_g = np.clip(r_arr * 0.349 + g_arr * 0.686 + b_arr * 0.168, 0, 255).astype(np.uint8)
    new_b = np.clip(r_arr * 0.272 + g_arr * 0.534 + b_arr * 0.131, 0, 255).astype(np.uint8)

    img_output = Image.merge('RGB', (
        Image.fromarray(new_r),
        Image.fromarray(new_g),
        Image.fromarray(new_b),
    ))

    if coldepth == 1:
        img_output = img_output.convert("1")
    elif coldepth == 8:
        img_output = img_output.convert("L")
    return img_output


def ImgEmboss(img_input, coldepth):
    """Efek emboss / timbul menggunakan ImageFilter.EMBOSS."""
    img_rgb = img_input.convert('RGB')
    img_output = img_rgb.filter(ImageFilter.EMBOSS)

    if coldepth == 1:
        img_output = img_output.convert("1")
    elif coldepth == 8:
        img_output = img_output.convert("L")
    else:
        img_output = img_output.convert("RGB")
    return img_output


def ImgGaussianNoise(img_input, coldepth, intensity=25):
    """Tambahkan Gaussian noise acak ke gambar.
    intensity: standar deviasi noise (0–100)
    """
    img_rgb = img_input.convert('RGB')
    img_arr = np.array(img_rgb, dtype=np.float32)
    noise = np.random.normal(0, intensity, img_arr.shape)
    img_noisy = np.clip(img_arr + noise, 0, 255).astype(np.uint8)
    img_output = Image.fromarray(img_noisy, mode='RGB')

    if coldepth == 1:
        img_output = img_output.convert("1")
    elif coldepth == 8:
        img_output = img_output.convert("L")
    return img_output


def ImgTemperature(img_input, coldepth, temp=0):
    """Sesuaikan temperature warna gambar.
    temp > 0 = lebih hangat (tambah merah/kurangi biru)
    temp < 0 = lebih dingin (tambah biru/kurangi merah)
    rentang: -100 hingga +100
    """
    img_rgb = img_input.convert('RGB')
    r_ch, g_ch, b_ch = img_rgb.split()

    r_arr = np.array(r_ch, dtype=np.float32)
    g_arr = np.array(g_ch, dtype=np.float32)
    b_arr = np.array(b_ch, dtype=np.float32)

    shift = temp * 1.2  # konversi skala slider ke intensitas piksel
    new_r = np.clip(r_arr + shift, 0, 255).astype(np.uint8)
    new_b = np.clip(b_arr - shift, 0, 255).astype(np.uint8)

    img_output = Image.merge('RGB', (
        Image.fromarray(new_r),
        Image.fromarray(g_arr.astype(np.uint8)),
        Image.fromarray(new_b),
    ))

    if coldepth == 1:
        img_output = img_output.convert("1")
    elif coldepth == 8:
        img_output = img_output.convert("L")
    return img_output