from PIL import Image

img_path = 'assets/mnist_sample.png'
try:
    img = Image.open(img_path)
    print(f"Loaded image: mode={img.mode}, size={img.size}")
    if img.mode != 'L':
        img = img.convert('L')
        img.save(img_path)
        print("Converted and saved as grayscale PNG.")
    else:
        print("Image is already grayscale.")
except Exception as e:
    print(f"Failed to open image: {e}") 