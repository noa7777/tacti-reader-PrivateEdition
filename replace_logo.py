from PIL import Image
import os
import sys
import struct

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, "new_logo.png")
OUTPUT_PNG = os.path.join(SCRIPT_DIR, "tactireader.png")
OUTPUT_ICO = os.path.join(SCRIPT_DIR, "tactireader.ico")

ICO_SIZES = [16, 24, 32, 48, 64, 128, 256]

def png_to_ico(png_images, output_path):
    """Build a valid ICO file from multiple PNG images.
    Modern Windows supports PNG inside ICO (since Vista).
    """
    entries = []
    data_offset = 6 + 16 * len(png_images)
    
    for size, png_bytes in png_images:
        w = size if size < 256 else 0
        h = size if size < 256 else 0
        entries.append({
            'w': w,
            'h': h,
            'colors': 0,
            'reserved': 0,
            'planes': 1,
            'bpp': 32,
            'size': len(png_bytes),
            'offset': data_offset,
            'data': png_bytes,
        })
        data_offset += len(png_bytes)
    
    with open(output_path, 'wb') as f:
        f.write(struct.pack('<HHH', 0, 1, len(entries)))
        for e in entries:
            f.write(struct.pack('<BBBBHHII',
                e['w'], e['h'], e['colors'], e['reserved'],
                e['planes'], e['bpp'], e['size'], e['offset']))
        for e in entries:
            f.write(e['data'])

def main():
    if not os.path.exists(INPUT_FILE):
        print(f"ERROR: {INPUT_FILE} not found.")
        print("Please place your new logo as 'new_logo.png' in the project root.")
        sys.exit(1)

    print("Loading new_logo.png ...")
    img = Image.open(INPUT_FILE).convert("RGBA")
    print(f"Original size: {img.size}")

    print()
    print("Generating tactireader.png (256x256) ...")
    png_img = img.resize((256, 256), Image.LANCZOS)
    png_img.save(OUTPUT_PNG, "PNG")
    print(f"Saved: {OUTPUT_PNG}")

    print()
    print("Generating tactireader.ico (multi-size PNG-in-ICO) ...")
    import io
    png_images = []
    for size in ICO_SIZES:
        resized = img.resize((size, size), Image.LANCZOS)
        buf = io.BytesIO()
        resized.save(buf, "PNG")
        png_images.append((size, buf.getvalue()))
        print(f"  {size}x{size}: {len(buf.getvalue())} bytes")
    
    png_to_ico(png_images, OUTPUT_ICO)
    
    file_size = os.path.getsize(OUTPUT_ICO)
    print(f"Saved: {OUTPUT_ICO} ({file_size} bytes)")
    
    with open(OUTPUT_ICO, 'rb') as f:
        data = f.read(6)
        count = struct.unpack('<H', data[4:6])[0]
    print(f"ICO contains {count} icon sizes")

    print()
    print("Done! Logo replaced successfully.")
    print("Next: rebuild the project with build_portable.bat to apply the new icon.")

if __name__ == "__main__":
    main()
