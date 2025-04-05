# from flask import Flask, request, jsonify, send_from_directory
# from werkzeug.utils import secure_filename
# import numpy as np
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity
# import PyPDF2
# import io
# from PIL import Image
# import pytesseract
# import os

# # Create the Flask app
# app = Flask(_name_, static_folder=r'C:\\Users\\user\\OneDrive\\Desktop\\PROJECT\\static')

# # Define sample job descriptions with required skills
# job_descriptions = {
#     'data_scientist': "Must have experience with Python, machine learning, and data analysis.",
#     'software_engineer': "Proficiency in Java, algorithms, and software design is required.",
#     'administrative_assistant': "Experience with Excel, PowerPoint, CRM, problem-solving, and team leadership."
# }

# # Define required skills for each job
# required_skills = {
#     'data_scientist': ['python', 'machine learning', 'data analysis'],
#     'software_engineer': ['java', 'algorithms', 'software design'],
#     'administrative_assistant': ['excel', 'powerpoint', 'crm', 'problem-solving', 'team leadership']
# }

# # Initialize vectorizer and transform job descriptions
# vectorizer = TfidfVectorizer()
# job_description_vectors = vectorizer.fit_transform(job_descriptions.values())

# # Function to extract text from PDF
# def extract_text_from_pdf(pdf_file):
#     try:
#         pdf_reader = PyPDF2.PdfFileReader(io.BytesIO(pdf_file))
#         text = ""
#         for page in pdf_reader.pages:
#             text += page.extract_text() or ""
#         return text
#     except Exception as e:
#         print(f"Error extracting text from PDF: {e}")
#         return ""

# # Function to extract text from JPG
# def extract_text_from_jpg(jpg_file):
#     try:
#         image = Image.open(io.BytesIO(jpg_file))
#         text = pytesseract.image_to_string(image)
#         return text
#     except Exception as e:
#         print(f"Error extracting text from JPG: {e}")
#         return ""

# # Function to extract skills from resume text
# def extract_skills(resume_text, job_title):
#     skills = required_skills.get(job_title.lower(), [])
#     resume_text_lower = resume_text.lower()
#     score = sum(1 for skill in skills if skill in resume_text_lower)
#     return score, len(skills)

# @app.route('/')
# def index():
#     return send_from_directory(app.static_folder, 'index.html')

# @app.route('/add_resume')
# def add_resume():
#     return send_from_directory(app.static_folder, 'add_resume.html')
# @app.route('/help_and_support')
# def help_and_support():
#     return send_from_directory(app.static_folder, 'help_and_support.html')

# @app.route('/upload', methods=['POST'])
# def upload():
#     try:
#         if 'resume' not in request.files or 'job' not in request.form:
#             return jsonify({"error": "No file part or job title missing"}), 400

#         file = request.files['resume']
#         job_title = request.form['job'].strip().lower()

#         if file.filename == '':
#             return jsonify({"error": "No selected file"}), 400

#         file_extension = file.filename.rsplit('.', 1)[1].lower()
        
#         if file and file_extension in ['pdf', 'jpg', 'jpeg']:
#             if file_extension in ['pdf']:
#                 resume_text = extract_text_from_pdf(file.read())
#             elif file_extension in ['jpg', 'jpeg']:
#                 resume_text = extract_text_from_jpg(file.read())
            
#             if not resume_text:
#                 return jsonify({"error": "Unable to extract text from file"}), 500
            
#             # Extract skills and calculate score
#             skills_count, total_skills = extract_skills(resume_text, job_title)
#             ats_score = (skills_count / total_skills) * 100 if total_skills > 0 else 0

#             return jsonify({"score": ats_score}), 200

#         return jsonify({"error": "Invalid file format"}), 400
#     except Exception as e:
#         print(f"Error during upload: {e}")
#         return jsonify({"error": "An error occurred while uploading the file"}), 500

# # Run the app
# if _name_ == '_main_':
#     app.run(debug=True)
from flask import Flask, request, jsonify, send_from_directory
from flask import Flask, render_template
from werkzeug.utils import secure_filename
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import PyPDF2
import io
from PIL import Image
import pytesseract
from docx import Document
import os

# Create the Flask app
app = Flask(__name__, static_folder=r'C:\\Users\\user\\OneDrive\\Desktop\\project2\\coding\\static')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limit file size to 16MB

# Define required skills with synonyms for each job
required_skills = {
    'data_scientist': [
        {'python': ['programming', 'scripting']}, 
        {'machine learning': ['ml', 'predictive modeling']}, 
        {'data analysis': ['data analytics', 'insights']}, 
        {'statistics': ['statistical analysis', 'quantitative analysis']}, 
        {'data visualization': ['data viz', 'charting', 'graphing']}, 
        {'pandas': ['data manipulation', 'dataframes']}, 
        {'scikit-learn': ['sklearn', 'ML toolkit']}, 
        {'sql': ['structured query language', 'databases']}, 
        {'big data': ['data engineering', 'large datasets']}, 
        {'deep learning': ['dl', 'neural networks']}
    ],
    'software_engineer': [
        {'java': ['backend programming', 'jvm languages']}, 
        {'python': ['scripting', 'automation']}, 
        {'software design': ['software architecture', 'design patterns']}, 
        {'sql': ['databases', 'data storage']}, 
        {'cloud computing': ['cloud services', 'cloud solutions']}, 
        {'javascript': ['js', 'frontend programming']}, 
        {'data structures': ['data organization', 'memory management']}, 
        {'algorithms': ['computational logic', 'problem-solving']}, 
        {'api development': ['api design', 'integration']}, 
        {'version control': ['git', 'source control']}
    ],
    'administrative_assistant': [
        {'excel': ['spreadsheets', 'data organization']}, 
        {'powerpoint': ['presentation software', 'slides']}, 
        {'crm': ['customer relationship management', 'client database']}, 
        {'data entry': ['data recording', 'data accuracy']}, 
        {'calendar management': ['scheduling', 'appointments']}, 
        {'communication': ['interpersonal skills', 'professional communication']}, 
        {'organization': ['coordination', 'task management']}, 
        {'problem-solving': ['troubleshooting', 'issue resolution']}, 
        {'customer service': ['client support', 'customer relations']}, 
        {'team support': ['collaboration', 'team coordination']}
    ],
    'project_manager': [
        {'strategic planning': ['long-term planning', 'goal setting']}, 
        {'project lifecycle management': ['project execution', 'project tracking']}, 
        {'budgeting': ['financial planning', 'cost control']}, 
        {'resource allocation': ['resource planning', 'resource optimization']}, 
        {'risk management': ['risk assessment', 'risk mitigation']}, 
        {'communication': ['interpersonal skills', 'stakeholder engagement']}, 
        {'agile methodologies': ['scrum', 'kanban']}, 
        {'team leadership': ['guiding teams', 'meeting objectives']}, 
        {'problem-solving': ['troubleshooting', 'conflict resolution']}, 
        {'conflict resolution': ['mediation', 'negotiation']}
    ],
    'web_developer': [
        {'html': ['markup language', 'web content structure']}, 
        {'css': ['styling', 'visual design']}, 
        {'javascript': ['js', 'dynamic content']}, 
        {'react.js': ['react', 'component-based design']}, 
        {'node.js': ['node', 'backend javascript']}, 
        {'git': ['version control', 'source management']}, 
        {'api integration': ['api connections', 'third-party integration']}, 
        {'responsive design': ['mobile optimization', 'cross-device compatibility']}, 
        {'typescript': ['type-safe javascript', 'typed programming']}, 
        {'web performance': ['site speed', 'optimization']}
    ],
    'aws_cloud_engineer': [
        {'aws': ['amazon web services', 'cloud infrastructure']}, 
        {'microsoft azure': ['azure', 'cloud platform']}, 
        {'linux': ['unix', 'system administration']}, 
        {'docker': ['containerization', 'virtualization']}, 
        {'kubernetes': ['k8s', 'container orchestration']}, 
        {'terraform': ['iac', 'infrastructure as code']}, 
        {'jenkins': ['ci/cd', 'automation']}, 
        {'networking': ['network configuration', 'cloud networks']}, 
        {'cloud security': ['cloud protection', 'data security']}, 
        {'ansible': ['automation', 'configuration management']}
    ]
}
# Skill development resources
skill_resources = {
    'python': {'website': 'https://www.w3schools.com/python/', 'youtube': 'https://www.youtube.com/watch?v=_uQrJ0TkZlc'},
    'machine learning': {'website': 'https://www.coursera.org/learn/machine-learning', 'youtube': 'https://www.youtube.com/watch?v=Gv9_4yMHFhI'},
    'data analysis': {'website': 'https://www.kaggle.com/learn/data-analysis', 'youtube': 'https://www.youtube.com/watch?v=5TjiHaP5BXA'},
    'sql': {'website': 'https://www.w3schools.com/sql/', 'youtube': 'https://www.youtube.com/watch?v=HXV3zeQKqGY'},
    'javascript': {'website': 'https://developer.mozilla.org/en-US/docs/Web/JavaScript', 'youtube': 'https://www.youtube.com/watch?v=W6NZfCO5SIk'},
    'react.js': {'website': 'https://react.dev/', 'youtube': 'https://www.youtube.com/watch?v=SqcY0GlETPk'},
    'aws': {'website': 'https://aws.amazon.com/training/', 'youtube': 'https://www.youtube.com/watch?v=ulprqHHWlng'},
    'java': {'website': 'https://www.w3schools.com/java/', 'youtube': 'https://www.youtube.com/watch?v=grEKMHpH7j0'},
    'software design': {'website': 'https://www.coursera.org/courses?query=software%20design', 'youtube': 'https://www.youtube.com/watch?v=QCBvh31AeEY'},
    'cloud computing': {'website': 'https://www.cloudacademy.com/', 'youtube': 'https://www.youtube.com/watch?v=32rxsPYH9pA'},
    'data structures': {'website': 'https://www.geeksforgeeks.org/data-structures/', 'youtube': 'https://www.youtube.com/watch?v=RBSGKlAvoiM'},
    'algorithms': {'website': 'https://www.geeksforgeeks.org/fundamentals-of-algorithms/', 'youtube': 'https://www.youtube.com/watch?v=8hly31xKZpI'},
    'api development': {'website': 'https://www.codecademy.com/learn/paths/build-python-web-apps-with-django', 'youtube': 'https://www.youtube.com/watch?v=G8X6Y2Wm0Hk'},
    'version control': {'website': 'https://www.git-scm.com/book/en/v2', 'youtube': 'https://www.youtube.com/watch?v=SWYqp7iY_Tc'},
    'excel': {'website': 'https://support.microsoft.com/en-us/excel', 'youtube': 'https://www.youtube.com/watch?v=EXmck_fZmL0'},
    'powerpoint': {'website': 'https://support.microsoft.com/en-us/powerpoint', 'youtube': 'https://www.youtube.com/watch?v=8Nhxt6UHFJw'},
    'crm': {'website': 'https://www.salesforce.com/products/crm-overview/', 'youtube': 'https://www.youtube.com/watch?v=rZrXhfOYED8'},
    'calendar management': {'website': 'https://www.cio.com/article/331160/11-tips-for-managing-your-calendar-like-a-pro.html', 'youtube': 'https://www.youtube.com/watch?v=wYXb5RwrGzI'},
    'communication': {'website': 'https://www.skillsyouneed.com/ips/communication-skills.html', 'youtube': 'https://www.youtube.com/watch?v=HAnw168huqA'},
    'organization': {'website': 'https://www.mindtools.com/pages/main/newMN_HTE.htm', 'youtube': 'https://www.youtube.com/watch?v=J7lUtNQUnhI'},
    'problem-solving': {'website': 'https://www.mindtools.com/pages/main/newMN_TCS.htm', 'youtube': 'https://www.youtube.com/watch?v=CVTgWHi9Yg0'},
    'customer service': {'website': 'https://www.salesforce.com/products/service-cloud/what-is-customer-service/', 'youtube': 'https://www.youtube.com/watch?v=6zD7zkA8L24'},
    'team support': {'website': 'https://www.mindtools.com/pages/main/newMN_TG.htm', 'youtube': 'https://www.youtube.com/watch?v=MG8l4h93Wh0'},
    'strategic planning': {'website': 'https://www.mindtools.com/pages/main/newMN_TCS.htm', 'youtube': 'https://www.youtube.com/watch?v=_u_Mxq6iShI'},
    'project lifecycle management': {'website': 'https://www.projectmanager.com/project-life-cycle', 'youtube': 'https://www.youtube.com/watch?v=RzHnbPRr8Jw'},
    'budgeting': {'website': 'https://www.investopedia.com/terms/b/budgeting.asp', 'youtube': 'https://www.youtube.com/watch?v=mNQ0rA7XYb8'},
    'resource allocation': {'website': 'https://www.projectmanager.com/project-resource-allocation', 'youtube': 'https://www.youtube.com/watch?v=QXgT98lFWXc'},
    'risk management': {'website': 'https://www.mindtools.com/pages/main/newMN_RM.htm', 'youtube': 'https://www.youtube.com/watch?v=7EvJXZ-p7H4'},
    'agile methodologies': {'website': 'https://www.atlassian.com/agile', 'youtube': 'https://www.youtube.com/watch?v=3l3T7gvcqAw'},
    'team leadership': {'website': 'https://www.mindtools.com/pages/main/newMN_TL.htm', 'youtube': 'https://www.youtube.com/watch?v=1uEr88YwJjw'},
    'conflict resolution': {'website': 'https://www.cio.com/article/286896/career-advice-how-to-handle-conflict-in-the-workplace.html', 'youtube': 'https://www.youtube.com/watch?v=2FqG0-j6a9E'},
    'html': {'website': 'https://www.w3schools.com/html/', 'youtube': 'https://www.youtube.com/watch?v=UB1O30fR-EE'},
    'css': {'website': 'https://www.w3schools.com/css/', 'youtube': 'https://www.youtube.com/watch?v=1Rs2ND1ryYc'},
    'node.js': {'website': 'https://nodejs.org/en/', 'youtube': 'https://www.youtube.com/watch?v=U8XF6AFGqlc'},
    'git': {'website': 'https://git-scm.com/', 'youtube': 'https://www.youtube.com/watch?v=SWYqp7iY_Tc'},
    'api integration': {'website': 'https://www.codecademy.com/learn/paths/build-python-web-apps-with-django', 'youtube': 'https://www.youtube.com/watch?v=G8X6Y2Wm0Hk'},
    'responsive design': {'website': 'https://www.w3schools.com/css/css_rwd_intro.asp', 'youtube': 'https://www.youtube.com/watch?v=srvUrASNj0s'},
    'typescript': {'website': 'https://www.typescriptlang.org/', 'youtube': 'https://www.youtube.com/watch?v=BwuLxPH8IDs'},
    'web performance': {'website': 'https://www.keycdn.com/blog/web-performance', 'youtube': 'https://www.youtube.com/watch?v=Ufl3cHQp7q8'},
    'docker': {'website': 'https://www.docker.com/what-docker', 'youtube': 'https://www.youtube.com/watch?v=3c-iBXg6q68'},
    'kubernetes': {'website': 'https://kubernetes.io/', 'youtube': 'https://www.youtube.com/watch?v=PH-2FfFD2PU'},
    'terraform': {'website': 'https://www.terraform.io/', 'youtube': 'https://www.youtube.com/watch?v=7xngdSCh1Xk'},
    'jenkins': {'website': 'https://www.jenkins.io/', 'youtube': 'https://www.youtube.com/watch?v=FxngTnP69tI'},
    'networking': {'website': 'https://www.geeksforgeeks.org/computer-network-tutorials/', 'youtube': 'https://www.youtube.com/watch?v=Uqobvllq0lk'},
    'cloud security': {'website': 'https://www.cio.com/article/334809/cloud-computing-what-is-cloud-security.html', 'youtube': 'https://www.youtube.com/watch?v=ydz9jwr0NG0'},
    'ansible': {'website': 'https://www.ansible.com/resources', 'youtube': 'https://www.youtube.com/watch?v=wpYX7tO8U7Y'}
}



# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    try:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_file))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() or ""
        return text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return ""

# Function to extract text from JPG
def extract_text_from_jpg(jpg_file):
    try:
        image = Image.open(io.BytesIO(jpg_file))
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        print(f"Error extracting text from JPG: {e}")
        return ""

# Function to extract text from Word documents
def extract_text_from_docx(docx_file):
    try:
        doc = Document(io.BytesIO(docx_file))
        text = []
        for paragraph in doc.paragraphs:
            text.append(paragraph.text)
        return '\n'.join(text)
    except Exception as e:
        print(f"Error extracting text from DOCX: {e}")
        return ""

# Function to extract skills from resume text with synonyms and resources
def extract_skills(resume_text, job_title):
    resume_text_lower = ' '.join(resume_text.lower().split())
    skills = required_skills.get(job_title.lower(), [])
    
    matched_skills = []
    unmatched_skills = []
    skill_learning_resources = {}

    for skill_dict in skills:
        for skill, synonyms in skill_dict.items():
            if any(term in resume_text_lower for term in [skill] + synonyms):
                matched_skills.append(skill)
                break
        else:
            unmatched_skills.append(skill)
            if skill in skill_resources:
                skill_learning_resources[skill] = skill_resources[skill]
    
    return len(matched_skills), len(skills), matched_skills, unmatched_skills, skill_learning_resources


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_resume')
def add_resume():
    return render_template('add_resume.html')

@app.route('/Services')
def services():
    return render_template('services.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
   return render_template('contact.html')

@app.route('/privacy')
def privacy_policy():
    return render_template('privacy.html')
@app.route('/student')
def student():
    return render_template('students.html')
@app.route('/parent')
def parent():
    return render_template('parents.html')

@app.route('/upload', methods=['POST'])
def upload():
    try:
        if 'resume' not in request.files or 'job' not in request.form:
            return jsonify({"error": "No file part or job title missing"}), 400

        file = request.files['resume']
        job_title = request.form['job'].strip().lower()

        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        file_extension = file.filename.rsplit('.', 1)[1].lower()
        
        if file and file_extension in ['pdf', 'jpg', 'jpeg', 'docx']:
            if file_extension == 'pdf':
                resume_text = extract_text_from_pdf(file.read())
            elif file_extension in ['jpg', 'jpeg']:
                resume_text = extract_text_from_jpg(file.read())
            elif file_extension == 'docx':
                resume_text = extract_text_from_docx(file.read())

            if not resume_text:
                return jsonify({"error": "Unable to extract text from file"}), 500
            
            skills_count, total_skills, matched_skills, unmatched_skills, skill_learning_resources = extract_skills(resume_text, job_title)
            ats_score = (skills_count / total_skills) * 100 if total_skills > 0 else 0
            
            return jsonify({
                "score": ats_score,
                "matched_skills": matched_skills,
                "unmatched_skills": unmatched_skills,
                "learning_resources": skill_learning_resources
            }), 200
        
        return jsonify({"error": "Invalid file format"}), 400
    except Exception as e:
        print(f"Error during upload: {e}")
        return jsonify({"error": "An error occurred while uploading the file"}), 500

if __name__ == '__main__':
    app.run(debug=True)
