import os
import requests

from Scrape_Winrates import Pokemon_name

# # Path to the folder with files you want to rename
# folder_path = r"C:\Users\Tanner\Documents\git\Pokemon_Unite\static\images\Pokemon"
#
# # Iterate over all the files in the folder
# for filename in os.listdir(folder_path):
#     # Check if the file name starts with "t_square_"
#     if filename.startswith("t_Square_"):
#         # Remove the "t_square_" part from the file name
#         new_filename = filename.replace("t_Square_", "")
#
#         # Get the full path of the current and new file
#         old_file = os.path.join(folder_path, filename)
#         new_file = os.path.join(folder_path, new_filename)
#
#         # Rename the file
#         os.rename(old_file, new_file)
#         print(f'Renamed: {filename} -> {new_filename}')
move_name = 'Coaching'
Pokemon_name = 'Mew'
img_url = 'https://uniteapi.dev/_next/image?url=%2FSprites%2Ft_Skill_Mew_S2A.png&w=64&q=75'
img_response = requests.get(img_url)
move_1_pic_file = 'static/images/Moves/' + Pokemon_name + ' - ' + move_name + '.png'
with open(move_1_pic_file, 'wb') as f:
    f.write(img_response.content)
