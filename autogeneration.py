import sys
import subprocess
import os
import shutil
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from PIL import Image, ImageTk

def select_script():
    file_path = filedialog.askopenfilename(title="Select Python Script", filetypes=[("Python files", "*.py")])
    if file_path:
        entry_script.delete(0, tk.END)
        entry_script.insert(0, file_path)

def select_image():
    file_path = filedialog.askopenfilename(title="Select Image", filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        entry_image.delete(0, tk.END)
        entry_image.insert(0, file_path)
        try:
            load_image_preview(file_path)
        except Exception:
            pass

def load_image_preview(file_path):
    try:
        image = Image.open(file_path)
        image.thumbnail((100, 100))
        img = ImageTk.PhotoImage(image)
        image_preview_label.config(image=img)
        image_preview_label.image = img
    except Exception:
        pass

def toggle_icon_checkbox():
    if checkbox_icon.get():
        entry_image.config(state="normal")
        button_browse_image.config(state="normal")
        try:
            load_image_preview(entry_image.get())
        except Exception:
            pass
    else:
        entry_image.config(state="disabled")
        button_browse_image.config(state="disabled")
        image_preview_label.config(image='')
        image_preview_label.image = None

def generate_exe():
    script_path = entry_script.get().strip()
    icon_path = entry_image.get().strip() if checkbox_icon.get() else None
    output_name = entry_output.get().strip()
    
    if not os.path.isfile(script_path):
        messagebox.showerror("Error", f"Script file '{script_path}' does not exist.")
        return
    if checkbox_icon.get() and not os.path.isfile(icon_path):
        messagebox.showerror("Error", f"Image file '{icon_path}' does not exist.")
        return

    script_dir = os.path.dirname(os.path.abspath(script_path))
    script_name = os.path.basename(script_path)

    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--noconfirm",
        "--clean",
        "--distpath", script_dir,
        script_path
    ]

    if checkbox_console.get():
        cmd.append('--console')
    else:
        cmd.append('--noconsole')

    if checkbox_icon.get():
        cmd.extend(['--icon=' + icon_path, '--name=' + output_name])
    else:
        cmd.extend(['--name=' + output_name])

    try:
        process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)
        process.wait()

        if process.returncode != 0:
            messagebox.showerror("Error", "An error occurred while creating the exe file.")
        else:
            exe_name = os.path.join(script_dir, output_name + '.exe')
            spec_file = os.path.join(script_dir, output_name + '.spec')
            build_dir = os.path.join(script_dir, 'build')
            if os.path.exists(spec_file):
                os.remove(spec_file)
            if os.path.exists(build_dir):
                shutil.rmtree(build_dir)
            messagebox.showinfo("Done", f"Executable file created: {exe_name}")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while creating the exe file: {e}")

root = tk.Tk()
root.title("EXE File Generator with Options")

style = ttk.Style()
style.theme_use('clam')

frame_select = ttk.Frame(root, padding=10)
frame_select.pack(fill=tk.X)

label_script = ttk.Label(frame_select, text="Select Python Script:")
label_script.grid(row=0, column=0, sticky=tk.W)

entry_script = ttk.Entry(frame_select, width=50)
entry_script.grid(row=0, column=1, padx=5)

button_browse_script = ttk.Button(frame_select, text="Browse...", command=select_script)
button_browse_script.grid(row=0, column=2, padx=5)

frame_options = ttk.Labelframe(root, text="Options", padding=10)
frame_options.pack(fill="both", expand="yes", padx=10, pady=5)

checkbox_console = tk.BooleanVar()
checkbox_icon = tk.BooleanVar()

check_console = ttk.Checkbutton(frame_options, text="Console Window (Use it if you are working with a console program rather than a graphical interface)", variable=checkbox_console)
check_console.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

check_icon = ttk.Checkbutton(frame_options, text="Use Image", variable=checkbox_icon, command=toggle_icon_checkbox)
check_icon.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)

frame_image = ttk.Frame(root, padding=10)
frame_image.pack(fill=tk.X)

label_image = ttk.Label(frame_image, text="Select Image (PNG/JPG):")
label_image.grid(row=0, column=0, sticky=tk.W)

entry_image = ttk.Entry(frame_image, width=50, state="disabled")
entry_image.grid(row=0, column=1, padx=5)

button_browse_image = ttk.Button(frame_image, text="Browse...", command=select_image, state="disabled")
button_browse_image.grid(row=0, column=2, padx=5)

image_preview_label = ttk.Label(frame_image)
image_preview_label.grid(row=1, column=0, columnspan=3, pady=10)

frame_output = ttk.Frame(root, padding=10)
frame_output.pack(fill=tk.X)

label_output = ttk.Label(frame_output, text="Enter name for .exe file:")
label_output.grid(row=0, column=0, sticky=tk.W)

entry_output = ttk.Entry(frame_output, width=50)
entry_output.grid(row=0, column=1, padx=5)

button_generate = ttk.Button(root, text="Create .exe File", command=generate_exe)
button_generate.pack(pady=10)

root.mainloop()
