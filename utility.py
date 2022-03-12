import io
import os


def cleanup(result):
    try:
        return_data = io.BytesIO()
        with open(result, 'rb') as fo:
            return_data.write(fo.read())
        # (after writing, cursor will be at last byte, so move it to start)
        return_data.seek(0)
        os.remove(result)
    except Exception as e:
        return e

    return return_data

def find_png():
    diagram_file = None
    path = "./"
    valid_images = [".png"]
    for f in os.listdir(path):
        ext = os.path.splitext(f)[1]
        if ext.lower() not in valid_images:
            continue
        diagram_file = f

    if diagram_file is None:
        return None

    return diagram_file


def image_cleanup():
    img = find_png()
    if img is not None:
        cleanup(img)
