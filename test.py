import os
import cv2
import tkinter as tk
from tkinter import filedialog
from deepface import DeepFace
from PIL import Image, ImageTk
from fpdf import FPDF
import threading
import shutil

def select_reference_images():
    root = tk.Tk()
    root.withdraw()
    reference_image_paths = filedialog.askopenfilenames(title="Select Reference Images")
    root.destroy()
    return reference_image_paths

def select_image_folder():
    root = tk.Tk()
    root.withdraw()
    folder_path = filedialog.askdirectory(title="Select Image Folder")
    root.destroy()
    return folder_path

def print_progress(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█'):
    percent = f"{100 * (iteration / float(total)):.{decimals}f}"
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print(f'\r{prefix} |{bar}| {iteration}/{total} ({percent}%) {suffix}', end='\r')
    if iteration == total:
        print()

def create_html(output_data, images_per_row=1):
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
    <style>
    table {
      width: 100%;
      border-collapse: collapse;
      border-bottom: 1px solid #ddd;
    }
    th, td {
      padding: 8px;
      text-align: left;
      border-bottom: 1px solid #ddd;
     
    }
    th {
      background-color: #f2f2f2;
    }
    img {
      max-width: 300px;
      height: auto;
    }
    </style>
    </head>
    <body>

    <h2>Face Verification Results</h2>

    <table>
      <tr>
        <th>Image</th>
        <th>Image Name</th>
        <th>Original Dimensions</th>
        <th>Resized Dimensions</th>
        <th>Distance</th>
        <th>Match</th>
      </tr>
    """

    for i in range(0, len(output_data), images_per_row):
        html_content += "<tr>"
        for j in range(images_per_row):
            if i + j >= len(output_data):
                break
            
            data = output_data[i + j]

            # Get original image dimensions
            img = Image.open(data["image_path"])
            orig_width, orig_height = img.size

            # Add HTML table row with image and data
            html_content += f"""
            <td><img src="{data["image_path"]}"></td>
            <td>{os.path.basename(data["image_path"])}</td>
            <td>{orig_width}x{orig_height}</td>
            <td>500x{int((500 / orig_width) * orig_height)}</td>
            <td>{data['distance']:.2f}</td>
            <td>{data['match']}</td>
            """
        html_content += "</tr>"

    html_content += """
    </table>

    </body>
    </html>
    """

    with open("face_verification_output.html", "w") as html_file:
        html_file.write(html_content)




def verify_faces_and_display_results(reference_images, folder_path, scrollable_frame, output_data, match_images_folder):
    # Get list of files in the folder
    files = os.listdir(folder_path)
    total_images = len(files)
    processed_images = 0

    # Loop through each file in the folder to display results
    for file in files:
        # Path to the current image file
        image_path = os.path.join(folder_path, file)

        # Skip if it's not a file
        if not os.path.isfile(image_path):
            continue

        # Initialize distances list
        distances = []

        # Calculate distances from all reference images
        for reference_image in reference_images:
            # Perform face recognition
            result = DeepFace.verify(reference_image, image_path, enforce_detection=False)
            if result.get("distance") is not None:  # Check if distance is available
                distances.append(result["distance"])

        # Check if distances list is not empty
        if distances:
            # Calculate the minimum distance
            min_distance = min(distances)
            distance = float(min_distance)

            # Determine if the face is a match
            match = distance <= 0.6
            match_text = "Yes" if match else "No"
            
            # If it's a match, copy the image to match_images_folder
            if match:
                shutil.copy(image_path, match_images_folder)
        else:
            # If distances list is empty, set distance to infinity
            distance = float('inf')
            match_text = "N/A"

        # Add data to output
        output_data.append({
            "image_path": image_path,
            "distance": distance,
            "match": match_text
        })

        # Load the image
        img = cv2.imread(image_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        img.thumbnail((300, 300))  # Adjust preview size

        # Convert image for Tkinter
        tk_img = ImageTk.PhotoImage(img)

        # Create a frame for each image and result
        frame = tk.Frame(scrollable_frame, bd=2, relief=tk.GROOVE)
        frame.pack(fill=tk.X, padx=5, pady=5, ipadx=5, ipady=5)

        # Display the image
        img_label = tk.Label(frame, image=tk_img)
        img_label.image = tk_img
        img_label.pack(side=tk.LEFT)

        # Display the result next to the image
        result_text = f"Distance: {distance:.2f}\nMatch: {match_text}"
        result_label = tk.Label(frame, text=result_text)
        result_label.pack(side=tk.LEFT, padx=10, pady=10)

        # Update processed images count
        processed_images += 1

        # Print remaining tasks in the console with progress bar
        print_progress(processed_images, total_images, prefix='Progress:', suffix='Complete', length=50)
    
    # Create PDF
    create_html(output_data)

def verify_faces_in_folder(reference_images, folder_path):
    output_data = []  # Initialize output_data here
    
    # Create a folder to store matched images
    match_images_folder = os.path.join(os.getcwd(), "matched_images")
    if not os.path.exists(match_images_folder):
        os.makedirs(match_images_folder)

    # Initialize GUI
    root = tk.Tk()
    root.title("Face Verification Results")
    
    # Get screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    # Set window width and height
    window_width = 550
    window_height = 500
    
    # Calculate x and y position for centering window
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    
    # Set window geometry
    root.geometry(f'{window_width}x{window_height}+{x}+{y}')
    
    canvas = tk.Canvas(root)
    scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    # Start a new thread for face verification and result display
    verification_thread = threading.Thread(target=verify_faces_and_display_results, args=(reference_images, folder_path, scrollable_frame, output_data, match_images_folder))
    verification_thread.start()

    def generate_pdf(output_data):  # Modify to accept output_data as an argument
        create_pdf(output_data)
    
    # Button to generate PDF
    pdf_button = tk.Button(root, text="Generate PDF", command=lambda: generate_pdf(output_data))  # Pass output_data to generate_pdf
    pdf_button.pack()

    root.mainloop()

# Select the reference images
reference_images = select_reference_images()

# Select the folder containing images to verify
folder_path = select_image_folder()

# Perform face verification for images in the folder
verify_faces_in_folder(reference_images, folder_path)
