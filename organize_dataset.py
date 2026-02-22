import os
import shutil

# ---- CHANGE THIS ONLY IF YOUR PATH IS DIFFERENT ----
folder = r"C:\Users\Mahesh\Desktop\Strawberry leaf disease 2\archive (1)\train"
# ----------------------------------------------------

# Create class folders and move images there
for filename in os.listdir(folder):
    if filename.lower().endswith((".jpg", ".jpeg", ".png")):
        
        # Extract class name (remove digits and file extension)
        class_name = ''.join([c for c in filename if not c.isdigit()]).replace(".jpg","").replace(".png","").replace(".jpeg","")

        class_path = os.path.join(folder, class_name)

        # Create class folder if not exists
        os.makedirs(class_path, exist_ok=True)

        # Move file into class folder
        src = os.path.join(folder, filename)
        dst = os.path.join(class_path, filename)

        # Prevent overwriting if already moved
        if not os.path.exists(dst):
            shutil.move(src, dst)

print("✅ Dataset organized successfully!")
print("➡ Check inside your train folder now.")
