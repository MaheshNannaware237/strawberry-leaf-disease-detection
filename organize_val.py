import os
import shutil

folder = r"C:\Users\Mahesh\Desktop\Strawberry leaf disease 2\archive (1)\val"

for filename in os.listdir(folder):
    if filename.lower().endswith((".jpg", ".jpeg", ".png")):

        class_name = ''.join([c for c in filename if not c.isdigit()]).replace(".jpg","").replace(".png","").replace(".jpeg","")

        class_path = os.path.join(folder, class_name)
        os.makedirs(class_path, exist_ok=True)

        src = os.path.join(folder, filename)
        dst = os.path.join(class_path, filename)

        if not os.path.exists(dst):
            shutil.move(src, dst)

print("✅ VAL folder organized successfully!")
