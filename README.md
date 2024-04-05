# 🎭 Face Verification System

## 🌟 Overview
This project is a Face Verification System implemented in Python using various libraries including OpenCV, tkinter, DeepFace, PIL (Python Imaging Library), and fpdf. The system allows users to select reference images and a folder containing images to be verified. It then calculates the distance between the faces in the reference images and the faces in the selected folder using DeepFace, and determines whether there is a match based on a predefined threshold. 

## ✨ Features
- **Select Reference Images**: Users can select multiple reference images to be used for face verification.
- **Select Image Folder**: Users can select a folder containing images to be verified against the reference images.
- **Face Verification**: The system uses DeepFace to calculate the distance between the faces in the reference images and the faces in the selected folder.
- **Display Results**: The system displays the verification results along with the processed images in a graphical user interface using tkinter.
- **Generate HTML Report**: Users can generate an HTML report summarizing the verification results.

## 🛠️ Installation
1. Clone the repository: `git clone https://github.com/your_username/FaceMatch.git`
2. Navigate to the project directory: `cd FaceMatch`
3. Install the required dependencies: `pip install -r requirements.txt`

## 🚀 Usage
1. Run the `face_verification.py` script.
2. Select reference images when prompted.
3. Select the folder containing images to be verified.
4. The system will perform face verification and display the results in a graphical user interface.
5. Optionally, click the "Generate HTML" button to generate an HTML report summarizing the verification results.

## 📝 Notes
- Ensure that Python and necessary dependencies are installed before running the script.
- The system uses DeepFace for face recognition, make sure it is installed and configured properly.
- Depending on the number of images and the computational resources, the verification process may take some time.

## 🙏 Credits
- This project utilizes various open-source libraries and frameworks, including OpenCV, tkinter, DeepFace, PIL, and fpdf.

## 📄 License
This project is licensed under the [MIT License](LICENSE).
