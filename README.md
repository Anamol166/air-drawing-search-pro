# Air Drawing Search Pro ✋🎨
Draw in the air with your hand and search Google instantly! This project lets you draw letters, numbers, and shapes by moving your hand in front of a camera. The AI recognizes what you drew and can search it on Google.

## What Does This Do?
- **Draw with your finger** in the air (no pen needed!)
- **AI recognizes** letters (A-Z), numbers (0-9), and drawings
- **Auto-corrects** spelling mistakes
- **Search Google** with what you drew
- **Draw shapes** like circles, rectangles, and lines
- **Choose colors** from the color palette

## Demo
Watch your hand become a magic drawing tool! Just point your index finger and draw in the air.

## What You Need

### Hardware
- A **webcam** or laptop camera
- A computer (Windows, Mac, or Linux)

### Software
- Python 3.7 or higher
- The libraries listed below

## Installation

### Step 1: Install Python
Download Python from [python.org](https://www.python.org/downloads/)

### Step 2: Download This Project
```bash
git clone https://github.com/anamol166/air-drawing-search-pro.git
cd air-drawing-search-pro
```

### Step 3: Install Required Libraries
```bash
pip install opencv-python
pip install numpy
pip install tensorflow
pip install mediapipe
pip install pyspellchecker
```

### Step 4: Add Your AI Models
You need these model files in the same folder:
- `bModel.h5` - For recognizing letters (A-Z)
- `bestmodel.h5` - For recognizing numbers (0-9)
- `drawing.h5` - For recognizing drawings
- `class.txt` - List of drawing categories

**Note:** You need to train these models or get them separately (not included in this repo).

## How to Run

```bash
python main.py
```

Make sure your webcam is connected!

## How to Use

### Basic Drawing
1. **Point your index finger** = Draw/Write
2. **Hold up 3 fingers** (index, middle, ring) = Select color
3. **Hold up 2 fingers** (index, middle) = Draw shapes (preview mode)

### Keyboard Shortcuts
- **R** = Recognize what you drew
- **C** = Clear the canvas
- **A** = Switch to Alphabet mode (letters A-Z)
- **N** = Switch to Number mode (0-9)
- **D** = Switch to Drawing mode
- **S** = Change shape (Line → Rectangle → Circle)
- **F** = Toggle fullscreen
- **ENTER** = Search on Google
- **Q** = Quit the app

### Color Palette
Available colors at the top:
- Red
- Green
- Blue
- Yellow
- Pink
- Black
- Eraser (to erase)

## Features Explained

### 1. Hand Tracking
Uses Google's MediaPipe to track your hand movements in real-time.

### 2. AI Recognition
- **Alphabet Mode**: Recognizes letters and auto-corrects spelling
- **Number Mode**: Recognizes digits 0-9
- **Drawing Mode**: Recognizes shapes and objects

### 3. Shape Drawing
Draw perfect shapes:
- Hold 2 fingers up
- Move to set the shape size
- Release to draw on canvas

### 4. Google Search
- Draw or write something
- Press **R** to recognize
- Press **ENTER** to search on Google

## Project Structure

```
air-drawing-search-pro/
│
├── main.py           # Main application file
├── model.py          # AI recognition engine
├── hand.py           # Hand tracking module
├── README.md         # This file
│
├── bModel.h5         # Alphabet recognition model
├── bestmodel.h5      # Number recognition model
├── drawing.h5        # Drawing recognition model
└── class.txt         # Drawing class labels
```

## How It Works

1. **Camera captures** video of your hand
2. **MediaPipe tracks** 21 hand landmarks
3. **Finger detection** determines what you're doing
4. **OpenCV draws** on a virtual canvas
5. **TensorFlow AI** recognizes your drawing
6. **Spell checker** corrects mistakes
7. **Web browser** searches Google

## Troubleshooting

### Camera not working?
- Change `cv2.VideoCapture(1)` to `cv2.VideoCapture(0)` in main.py

### Models not loading?
- Make sure all `.h5` files are in the same folder as main.py

### Hand not detected?
- Make sure you have good lighting
- Keep your hand clearly visible to the camera

### Recognition not accurate?
- Draw bigger and clearer
- Use the correct mode (A/N/D)
- Try drawing slower

## Requirements File

All Python libraries needed:
```
opencv-python>=4.5.0
numpy>=1.19.0
tensorflow>=2.8.0
mediapipe>=0.8.0
pyspellchecker>=0.6.0
```

## Future Improvements

- [ ] Add more drawing categories
- [ ] Save drawings as images
- [ ] Add voice commands
- [ ] Mobile app version

## Credits

Built with:
- [OpenCV](https://opencv.org/) - Computer vision
- [MediaPipe](https://mediapipe.dev/) - Hand tracking
- [TensorFlow](https://www.tensorflow.org/) - AI models
- [PySpellChecker](https://pypi.org/project/pyspellchecker/) - Spell correction

## License

MIT License - Feel free to use and modify!

## Contributing

Want to improve this project?
1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request

## Contact

Have questions? Open an issue on GitHub!

---

**Made with  by Anamol166**

Happy Air Drawing! 🎨✨
