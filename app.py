import os
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from sentence_transformers import SentenceTransformer, util
import fitz  # PyMuPDF

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create the uploads directory if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Initialize the model
model = SentenceTransformer('all-MiniLM-L6-v2')


# Function to check allowed file types
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Function to sanitize filenames
def sanitize_filename(filename):
    return secure_filename(filename)


# Function to read text from a PDF file
def read_resume_content(resume_path):
    text = ""
    try:
        with fitz.open(resume_path) as pdf:
            for page in pdf:
                text += page.get_text()
    except Exception as e:
        print(f"Error reading file {resume_path}: {e}")
    return text


# Function to calculate similarity score
def calculate_similarity(resume_path, job_description):
    resume_content = read_resume_content(resume_path)
    if not resume_content.strip():
        print(f"No content found in resume: {resume_path}")
        return 0  # Return 0 if no content is found

    # Encode the resume and job description
    resume_embedding = model.encode(resume_content, convert_to_tensor=True)
    job_desc_embedding = model.encode(job_description, convert_to_tensor=True)

    # Compute the cosine similarity
    similarity_score = util.pytorch_cos_sim(resume_embedding, job_desc_embedding).item()

    return similarity_score


# Route for the main page
@app.route('/')
def index():
    return render_template('index.html')


# Route for comparing resumes
@app.route('/compare', methods=['POST'])
def compare():
    try:
        # Ensure 'resumes[]' is in the request and multiple files are processed
        if 'resumes[]' not in request.files:
            return jsonify({"error": "No files part"})

        # Get the list of uploaded files
        files = request.files.getlist('resumes[]')

        if not files:
            return jsonify({"error": "No files selected"})

        # Get job description and number of resumes to shortlist from the form
        job_desc = request.form.get('jobDesc', '')
        num_shortlist = int(request.form.get('numShortlist', 0))
        scores = []

        # Loop through all the uploaded files
        for file in files:
            if file and allowed_file(file.filename):
                # Sanitize the filename to remove any special characters or spaces
                filename = sanitize_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

                try:
                    # Save the file
                    file.save(file_path)

                    # Check if the file exists and is accessible
                    if os.path.exists(file_path):
                        # Calculate similarity score for each resume
                        score = calculate_similarity(file_path, job_desc)
                        # Append the filename and score to the scores list
                        scores.append({"filename": filename, "score": score})
                        print(f"Processed file: {filename} with score: {score}")
                    else:
                        print(f"File not found after saving: {file_path}")
                except Exception as e:
                    print(f"Error saving file {filename}: {e}")

            else:
                return jsonify({"error": f"Invalid file type: {file.filename}. Only PDF files are allowed."})

        # Sort the resumes by their scores in descending order
        scores = sorted(scores, key=lambda x: x['score'], reverse=True)

        # Limit the number of results based on user input
        if num_shortlist > 0:
            scores = scores[:num_shortlist]

        # Log sorted scores
        print(f"Sorted Scores: {scores}")

        # Return the ranked list of scores
        return jsonify({"scores": scores})

    except Exception as e:
        # Catch and log unexpected errors
        print(f"An error occurred: {e}")
        return jsonify({"error": "An unexpected error occurred. Please try again later."})


if __name__ == '__main__':
    app.run(debug=True)
