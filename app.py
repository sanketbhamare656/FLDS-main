from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import cv2
import os
import shutil
import dlib
from imutils import face_utils

"""FastAPI app initialization"""
app = FastAPI()

# Templates and static files
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

"""Path to the predictor file"""
shape_predictor_path = "shape_predictor_68_face_landmarks.dat"

"""Initialize dlib's face detector and predictor"""
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(shape_predictor_path)

def process_image(image_path, output_filename):
    """Utility function to process image and return output"""
    image = cv2.imread(image_path)
    image = cv2.resize(image, (500, 500))  # Resize to make it manageable
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    rects = detector(gray, 1)

    for (i, rect) in enumerate(rects):
        """Detect faces and draw landmarks"""
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)
        (x, y, w, h) = face_utils.rect_to_bb(rect)
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(image, f"Face #{i + 1}", (x - 10, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        for (x, y) in shape:
            cv2.circle(image, (x, y), 1, (0, 0, 255), -1)

    output_folder = "static/output"
    """Ensure the output directory exists and save the image"""
    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, output_filename)
    cv2.imwrite(output_path, image)
    """Return the path to the processed image"""
    return output_path

"""Route for displaying the HTML form to upload an image"""
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):  # Make sure `request` is passed here
    return templates.TemplateResponse("index.html", {"request": request})

"""About route"""
@app.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})

"""Route to handle file upload and processing"""
@app.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...)):
    """Save the uploaded file"""
    upload_folder = "static/uploads"
    os.makedirs(upload_folder, exist_ok=True)
    file_location = os.path.join(upload_folder, file.filename)

    """Save the uploaded image to disk"""
    with open(file_location, "wb") as f:
        shutil.copyfileobj(file.file, f)

    """Generate a unique output filename for the processed image"""
    output_filename = f"landmarks_{file.filename}"

    """Process the image and save the result"""
    output_image_path = process_image(file_location, output_filename)

    """Return the URL of the processed image for display"""
    return {
        "filename": file.filename,
        "output_image": f"/static/output/{output_filename}"
    }
