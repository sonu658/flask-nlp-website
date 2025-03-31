from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

# Folder configuration
UPLOAD_FOLDER = 'uploads/'
COMMENT_FOLDER = 'comments/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['COMMENT_FOLDER'] = COMMENT_FOLDER

# Ensure upload folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(COMMENT_FOLDER, exist_ok=True)

# In-memory storage (could be replaced with a database)
submissions = []

# Home route
@app.route('/')
def index():
    return render_template('index.html', submissions=submissions)

# Upload Notes route
@app.route('/upload_notes', methods=['POST'])
def upload_notes():
    if 'notes' not in request.files:
        return redirect(request.url)
    file = request.files['notes']
    if file:
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)
        submissions.append(file.filename)
    return redirect(url_for('index'))

# Upload Assignment route
@app.route('/upload_assignment', methods=['POST'])
def upload_assignment():
    name = request.form['name']
    usn = request.form['usn']
    subject_code = request.form['subject_code']
    if 'assignment' not in request.files:
        return redirect(request.url)
    file = request.files['assignment']
    if file:
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)
        submissions.append(f"{name}_{usn}_{subject_code}_{file.filename}")
    return redirect(url_for('index'))

# View Submissions route
@app.route('/view_submissions', methods=['POST'])
def view_submissions():
    name = request.form['name']
    usn = request.form['usn']
    user_submissions = [s for s in submissions if s.startswith(f"{name}_{usn}")]
    return render_template('index.html', submissions=user_submissions)

# Submit Comment route
@app.route('/submit_comment', methods=['POST'])
def submit_comment():
    comment = request.form['comment']
    with open(os.path.join(app.config['COMMENT_FOLDER'], 'comments.txt'), 'a') as f:
        f.write(f"{comment}\n")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
