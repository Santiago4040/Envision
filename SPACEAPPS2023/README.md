Dependencies:
Flask
Pillow
pydub
numpy

We take an image (either from a frame of a video or an image file) and insert a 1 pixel wide row starting from the left, then fetch the individual pixel data and convert its data from RGB values to HSV values which we store 1 of these components into an array of the same length as the height of the source image.

After this we transform the array using the Inverse Fourier Transform provided by the numpy library (NumPy, n.d.), which interprets the data in the frequency domain, meaning a set of frequencies defined by the index of each element whose value controls the amplitude Figure 3, these pure tones are mixed to create audio samples in the spatial domain that will get appended into a buffer to hold the generated data.

We repeat this process for every row left in the image and we export the buffer into an audio file that can be read by any multimedia player or enhanced by an audio editor.