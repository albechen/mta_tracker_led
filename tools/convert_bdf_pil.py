# %%
from PIL import BdfFontFile
import glob
import os

# %%
input_dir = "assets/fonts/bdf"
output_dir = "assets/fonts/pil"

font_file_paths = glob.glob(os.path.join(input_dir, "*.bdf"))

# %%
for font_file_path in font_file_paths:
    try:
        with open(font_file_path, "rb") as fp:
            p = BdfFontFile.BdfFontFile(fp)

            # build output base path (no extension)
            base_name = os.path.splitext(os.path.basename(font_file_path))[0]
            output_base = os.path.join(output_dir, base_name)

            # despite what the syntax suggests, .save(font_file_path) won't
            # overwrite your .bdf files, it just creates new .pil and .pdm
            p.save(output_base)

    except (SyntaxError, IOError) as err:
        print(f"File at '{font_file_path}' could not be processed.")
        print("Error:", err)
# %%
