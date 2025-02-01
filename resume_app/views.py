from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Resume
from .forms import ResumeForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
import PyPDF2, docx
import re
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer


from django.core.paginator import Paginator

# Create your views here.
@login_required(login_url='/login/')
def home(request):
    return render(request, 'home.html')

def login_page(request):
    if request.method == "POST":
        user_name = request.POST.get('username')
        password = request.POST.get('password')
        
        if User.objects.filter(username=user_name).exists():
            user = authenticate(username=user_name, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                messages.error(request,"Invalid Password")
                return redirect('/login/')
        else:
            messages.error(request,"User does not exist")
            return redirect('/login/')
        
    return render(request, 'login.html')

def register_page(request):
    
    if request.method == "POST":
        user_name = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password1')

        if User.objects.filter(username=user_name).exists():
            messages.error(request,"Username is already taken")
            return redirect('/register/')

        user = User.objects.create_user(username=user_name,email=email)
        user.set_password(password)
        user.save()
        messages.success(request,"Your accout is successfully added....")
        return redirect('/')        
    return render(request, 'register.html')


def logout_page(request):
    logout(request)
    return redirect('/login/')

@login_required(login_url='/login/')
def upload_resume(request):
    if request.method == "POST":
        form = ResumeForm(request.POST, request.FILES)
        if form.is_valid():
            resume = form.save(commit=False)
            resume.user = request.user
            text = extract_text(request.FILES["file"])
            resume.extracted_text = text
            resume.score = calculate_resume_score(text)  # Assign AI score
            resume.save()
            messages.success(request,"Your resume has been uploaded successfully....")
            return redirect('resume_list')
        else:
            messages.error(request,"Invalid Form")
            return redirect('/upload/')
    else:
        form = ResumeForm()
    return render(request,'upload.html',{'form':form})




nlp = spacy.load("en_core_web_sm")

# Predefined job keywords (Modify based on job role)
# JOB_KEYWORDS = ["python", "machine learning", "data analysis", "django", "AI", "SQL"]

JOB_KEYWORDS = [
    "java", "python", "c++", "c#", "software development", "algorithms", "api", "git", "version control", "scrum", "microservices",  # Software Engineer
    "python", "machine learning", "statistics", "tensorflow", "keras", "deep learning", "data analysis", "pandas", "sql", "big data", "model deployment",  # Data Scientist
    "html", "css", "javascript", "react", "vue.js", "ui/ux", "ajax", "responsive design", "bootstrap", "sass",  # Web Developer Frontend
    "node.js", "django", "flask", "java", "sql", "api", "microservices", "aws", "docker", "kubernetes",  # Web Developer Backend
    "ui design", "ux research", "wireframes", "prototypes", "figma", "sketch", "adobe xd", "user stories", "responsive design", "interaction design",  # UX/UI Designer
    "unity", "unreal engine", "c++", "c#", "game design", "game mechanics", "3d modeling", "ai", "multiplayer", "game testing",  # Game Developer
    "aws", "azure", "google cloud", "cloud architecture", "microservices", "containers", "kubernetes", "cloud security", "serverless", "terraform",  # Cloud Architect
    "roadmap", "scrum", "agile", "mvp", "market research", "stakeholder management", "product lifecycle", "jira", "confluence", "data-driven decisions",  # Product Manager
    # Add more roles as needed...
]



def extract_text(file):
    """Extracts text from a PDF or DOCX file."""
    if file.name.endswith(".pdf"):
        reader = PyPDF2.PdfReader(file)
        text = " ".join([page.extract_text() for page in reader.pages if page.extract_text()])
    elif file.name.endswith(".docx"):
        doc = docx.Document(file)
        text = " ".join([para.text for para in doc.paragraphs])
    else:
        return ""

    return preprocess_text(text)

def preprocess_text(text):
    """Cleans and processes resume text using NLP."""
    text = re.sub(r"\s+", " ", text)  # Remove extra spaces
    text = text.lower()  # Convert to lowercase
    doc = nlp(text)  
    tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
    return " ".join(tokens)

def calculate_resume_score(text):
    """Matches resume text with job keywords using TF-IDF vectorization."""
    vectorizer = TfidfVectorizer()
    corpus = [" ".join(JOB_KEYWORDS), text]  # Compare job keywords with resume text
    tfidf_matrix = vectorizer.fit_transform(corpus)
    similarity = (tfidf_matrix * tfidf_matrix.T).A[0][1]  # Cosine similarity
    # print(similarity)
    return round(similarity * 100, 2)  # Convert to percentage






@login_required
def resume_list(request):
    resumes = Resume.objects.filter(user=request.user).order_by('-uploaded_at')  # Show latest first

    # Pagination: Show 5 resumes per page
    paginator = Paginator(resumes, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'resume_list.html', {'page_obj': page_obj})


def delete(request,id_resume):
    resume = get_object_or_404(Resume,id=id_resume,user=request.user)
    resume.delete()
    return redirect('resume_list')


def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def services(request):
    return render(request,'services.html')



