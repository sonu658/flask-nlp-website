from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

# Set the folder where uploaded files will be stored
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Upload Notes Route
@app.route('/upload_notes', methods=['POST'])
def upload_notes():
    if 'notes' not in request.files:
        return redirect(request.url)
    notes = request.files['notes']
    if notes.filename != '':
        notes.save(os.path.join(app.config['UPLOAD_FOLDER'], notes.filename))
    return redirect(url_for('view_uploads'))

# Upload Assignments Route
@app.route('/upload_assignment', methods=['POST'])
def upload_assignment():
    name = request.form['name']
    usn = request.form['usn']
    subject_code = request.form['subject_code']
    assignment = request.files['assignment']
    
    if 'assignment' not in request.files:
        return redirect(request.url)
    if assignment.filename != '':
        assignment.save(os.path.join(app.config['UPLOAD_FOLDER'], assignment.filename))
    return redirect(url_for('view_uploads'))

# View Uploaded Notes and Assignments
@app.route('/view_uploads')
def view_uploads():
    uploaded_files = os.listdir(UPLOAD_FOLDER)
    return render_template('view_uploads.html', uploaded_files=uploaded_files)

# Route to display individual uploads (Notes or Assignment)
@app.route('/view_file/<filename>')
def view_file(filename):
    return render_template('view_file.html', filename=filename)

# Route to delete uploaded file
@app.route('/delete_file/<filename>', methods=['GET'])
def delete_file(filename):
    try:
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('view_uploads'))
    except:
        return "Error deleting file"

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
