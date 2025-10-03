from PIL import Image
from pathlib import Path

input_path = Path("download.png")
output_path = Path("output.webp")

img = Image.open(input_path)
img.save(output_path, "WEBP", lossless=True, optimize=True)

print("Saved:", output_path, "Size:", output_path.stat().st_size, "bytes")
