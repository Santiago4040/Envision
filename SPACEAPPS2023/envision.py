import numpy as np
from PIL import Image
from pydub import AudioSegment 
import array

global_audio_data = array.array('d')

def export_audio(arr: np.array, name: str, type: str):
    raw_data = np.zeros(len(arr), dtype="int16")

    max_sample = 0
    for sample in arr:
        max_sample = max(max_sample, abs(sample))

    scale_factor = 1.0 / max_sample
    
    for idx in range(len(arr)):
        raw_data[idx] = arr[idx] * 32000 * scale_factor

    fft_audio = AudioSegment(
        raw_data.tobytes(), 
        frame_rate=48000,
        sample_width=2, 
        channels=1
    )

    fft_audio.export(name, type)


#https://math.stackexchange.com/questions/556341/rgb-to-hsv-color-conversion-algorithm
def rgb_to_hsv(value):
    r = value[0] / 255
    g = value[1] / 255
    b = value[2] / 255

    maxc  = max(r, g, b)
    minc = min(r, g, b)
    v = maxc
    if minc == maxc:
        return 0.0, 0.0, v
    s = (maxc-minc) / maxc
    rc = (maxc-r) / (maxc-minc)
    gc = (maxc-g) / (maxc-minc)
    bc = (maxc-b) / (maxc-minc)
    if r == maxc:
        h = 0.0+bc-gc
    elif g == maxc:
        h = 2.0+rc-bc
    else:
        h = 4.0+gc-rc
    h = (h/6.0) % 1.0
    return (h, s, v)

def convolve_image(img_path: str):
    global global_audio_data

    img_input: Image.Image = Image.open(img_path)
    img_input = img_input.convert("RGB")

    y_x_factor = 150 / img_input.size[1]
    img_input = img_input.resize((round(img_input.size[0] * y_x_factor * 4), 150))

    #Image object for exporting the reconstruction of the image
    #DEBUG_image: Image.Image = Image.new(mode="RGB", size=img_input.size)

    img_data = img_input.load()
    img_res = img_input.size
    #DEBUG_data = DEBUG_image.load()

    img_freq_slice = np.zeros(img_res[1] * 2, dtype=float)

    for x in range(img_res[0]):
        for y in range(img_res[1] - 1):
            #Just get the red channel color
            hsv = rgb_to_hsv(img_data[x, y])
            img_freq_slice[img_res[1] - y] = hsv[1]

        #Use numpy's inverse fourier transform function to get transform audio into sound
        img_spatial_slice = np.fft.ifft(img_freq_slice)

        for y in range(len(img_spatial_slice)):
            #Append the generated sound from the current row to the audio array data
            global_audio_data.append(img_spatial_slice[y].real)

    img_input.close()


def process(file: str):
    global global_audio_data
    global_audio_data = array.array('d')
    convolve_image(file)
    export_audio(global_audio_data, "static/out.wav", "wav")

#def main():
#    global global_audio_data
#
#    for idx in range(1, 900):
#        print("Image #", idx)
#        convolve_image("maybe/res", idx)
#
#    export_wav(global_audio_data, "out.wav")

#A must for a c programmer
#main()
