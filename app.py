from flask import Flask, request, render_template, jsonify
from flask_mail import Mail, Message
import subprocess
import tempfile
import os
import zipfile
import threading
import uuid

app = Flask(__name__)

# Flask-Mail Configuration using fastmail's smtp server.
app.config["MAIL_SERVER"] = "smtp.fastmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"] = "viralgeneclock1@fastmail.com"
app.config["MAIL_PASSWORD"] = "8wyxcy6vu6n6egyb" 
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_DEFAULT_SENDER"] = "viralgeneclock1@fastmail.com"

mail = Mail(app)

# Dictionary to store the status and output of each task.
tasks_status = {}

# Function to zip directories -- zipped output emailed.
def zip_directories(directories, zip_filename):
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for directory in directories:
            for root, dirs, files in os.walk(directory):
                for file in files:
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, os.path.relpath(file_path, os.path.join(directory, '..')))

def run_command(fasta_sequence, reference_genome, email_address, task_id):
    with tempfile.NamedTemporaryFile(delete=False, mode='w+', suffix='.fasta') as tmpfile:
        tmpfile.write(fasta_sequence)
        fasta_file_path = tmpfile.name

    tasks_status[task_id] = {'status': 'running', 'output': ''}

    # Running the main.py -- runs the entire command line mechanism.
    command = ['python3', 'main.py', fasta_file_path, reference_genome]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    # Capturing output in real-time.
    while True:
        line = process.stdout.readline()
        if not line and process.poll() is not None:
            break
        tasks_status[task_id]['output'] += line
        print(line, end='')  # Also prints to command line

    # Once command completes, email is sent.
    try:
        zip_filename = 'outputs.zip'
        zip_directories(['fullSequence-output', 'geneAnalysis-output', 'avg_mutation_rate_final'], zip_filename)

        with app.app_context():  # Subject and recipient for sending email.
            msg = Message("ViralGeneClock Outputs", recipients=[email_address])
            msg.body = "Your ViralGeneClock analysis is complete! Please find the results attached with this email."
            with open(zip_filename, "rb") as fp:
                msg.attach(zip_filename, "application/zip", fp.read())
            mail.send(msg)

        tasks_status[task_id]['status'] = 'emailed'
        os.remove(zip_filename)
    except Exception as e: # exception not working here; email sent either way. Javascript in running.html used to notify user of input failure.
        tasks_status[task_id]['status'] = 'failed'
        tasks_status[task_id]['output'] = str(e)
    finally:
        os.unlink(fasta_file_path)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/references')
def references():
    return render_template('references.html')

@app.route('/run', methods=['POST'])
def run_script():
    fasta_sequence = request.form['fasta_sequence']
    reference_genome = request.form['reference_genome']
    email_address = request.form['email']
    task_id = str(uuid.uuid4())
    tasks_status[task_id] = {'status': 'initialized', 'output': ''}
    
    thread = threading.Thread(target=run_command, args=(fasta_sequence, reference_genome, email_address, task_id))
    thread.start()
    
    return render_template('running.html', task_id=task_id)

@app.route('/status/<task_id>')
def task_status(task_id):
    return jsonify(tasks_status.get(task_id, {'status': 'unknown', 'output': ''}))

if __name__ == '__main__':
    app.run(debug=True)

