import os
from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename
import PyPDF2
import re
import pandas as pd




import base64
from io import BytesIO

from Rejection_Email_Send import rejection_mail
from Selection_Email_Send import selection_mail
from job_descript import job_descript

path = os.getcwd()
UPLOAD_FOLDER = os.path.join(path, 'uploads')
ALLOWED_EXTENSIONS = {'pdf'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.add_url_rule(
    "/uploads/<name>", endpoint="download_file", build_only=True
)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000
app.config['SECRET_KEY'] = 'super secret key'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('screening', name=filename)+"#Sparta")
    return render_template("index.html")

@app.route('/screening/<name>', methods=['GET', 'POST'])
def screening(name):
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            pdfFileObj = open('uploads/{}'.format(filename), 'rb')
            pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
            num_pages = pdfReader.numPages
            count = 0
            text = ""
            x=""
            while count < num_pages:
                pageObj = pdfReader.getPage(count)
                count += 1
                text += pageObj.extractText()


            def cleanResume(resumeText):




                resumeText = re.sub('http\S+\s*', ' ', resumeText)  # remove URLs
                resumeText = re.sub('RT|cc', ' ', resumeText)  # remove RT and cc
                resumeText = re.sub('#\S+', '', resumeText)  # remove hashtags
                resumeText = re.sub('[%s]' % re.escape("""!"#$%&'()*+,-/:;<=>?[\]^_`{|}~"""), ' ',
                                    resumeText)  # remove punctuations
                resumeText = re.sub(r'[^\x00-\x7f]', r' ', resumeText)
                resumeText = re.sub('\s+', ' ', resumeText)  # remove extra whitespace
                return resumeText.lower()

            text = cleanResume(text)

            # Extracting email using regular expression
            email = re.findall(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}', text)
            x=''




            job_desc_count = 0

            data = 0
            bidang=job_descript()
            for word_project in bidang['Job Description']:
                job_desc_count += 1

            job_describtion = []

            data_list = []

            job_desc = 0  # matching
            # Create an empty list where the scores will be stored
            scores = []

            # Obtain the scores for each area
            for area in bidang.keys():
                if area == 'Job Description':
                    for word_project in bidang['Job Description']:
                        if word_project in text:
                            job_desc += 1
                            job_describtion.append(word_project)
                    scores.append(job_desc)


            k = (job_desc / job_desc_count) * 100
            if (k > 80):
                data = f'Candidate is selected for next round as\n {k} '
                for i in email:
                    x += i
                selection_mail(x)
                print(x)
            else:
                data = f'Candidate is not selected for next round as\n {k} '
                for i in email:
                    x += i

                rejection_mail(x)
                print(x)





            data_all_list = {'Job Description': job_describtion, 'Data Science': data_list}
            # data_all_list_df = pd.DataFrame.from_dict(data_all_list, orient='index', dtype=object).transpose()


            summary = \
            pd.DataFrame(scores, index=bidang.keys(), columns=['score']).sort_values(by='score', ascending=False).loc[
                lambda df: df['score'] > 0]




            return render_template('index.html', data=data)


    else:
        pdfFileObj = open('uploads/{}'.format(name), 'rb')
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
        num_pages = pdfReader.numPages
        count = 0
        text = ""
        while count < num_pages:
            pageObj = pdfReader.getPage(count)
            count += 1
            text += pageObj.extractText()

        def cleanResume(resumeText):
            resumeText = re.sub('http\S+\s*', ' ', resumeText)  # remove URLs
            resumeText = re.sub('RT|cc', ' ', resumeText)  # remove RT and cc
            resumeText = re.sub('#\S+', '', resumeText)  # remove hashtags

            resumeText = re.sub('[%s]' % re.escape("""!"#$%&'()*+,-/:;<=>?[\]^_`{|}~"""), ' ',
                                resumeText)  # remove punctuations
            resumeText = re.sub(r'[^\x00-\x7f]', r' ', resumeText)
            resumeText = re.sub('\s+', ' ', resumeText)  # remove extra whitespace
            return resumeText.lower()


        text = cleanResume(text)

        email = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)

        # Printing the extracted email





        bidang=job_descript()
        job_desc_count = 0

        data = 0
        for word_project in bidang['Job Description']:
                job_desc_count += 1




        job_describtion = []

        data_list = []

        job_desc=0
        # Create an empty list where the scores will be stored
        scores = []

        # Obtain the scores for each area
        for area in bidang.keys():
            if area == 'Job Description':
                for word_project in bidang['Job Description']:
                    if word_project in text:
                        job_desc += 1
                        job_describtion.append(word_project)
                scores.append(job_desc)


        x=''
        k= (job_desc/job_desc_count)*100
        k = (job_desc / job_desc_count) * 100
        if (k > 80):
            data = f'Candidate is selected for next round as\n {k} '
            for i in email:
                x += i
            selection_mail(x)
            print(x)
        else:
            data = f'Candidate is not selected for next round as\n {k} '
            for i in email:
                x += i
            print(x)
            rejection_mail(x)






        data_all_list = {'Job Description': job_describtion}
        #data_all_list_df = pd.DataFrame.from_dict(data_all_list, orient='index', dtype=object).transpose()

        summary = pd.DataFrame(scores, index=bidang.keys(), columns=['score']).sort_values(by='score', ascending=False).loc[
            lambda df: df['score'] > 0]









        return render_template('index.html', data=data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
