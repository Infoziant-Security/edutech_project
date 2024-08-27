from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import connection
from django.db import connections
from django.contrib.auth.decorators import login_required
from django.utils.dateparse import parse_date
from django.http import HttpResponseBadRequest
import datetime
import re
from django.http import HttpResponse

# Function to execute raw SQL queries
def execute_raw_sql(query, params=None):
    with connection.cursor() as cursor:
        cursor.execute(query, params)
        return cursor.fetchall()

def home_page(request):
    return render(request, "index.html")

def signin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
         
        user = authenticate(username=username, password=password)
         
        if user is None:
            messages.error(request, "Invalid Password")
            return render(request, "login.html")
        
        query = "SELECT user_type FROM auth_user WHERE username = %s"
        user_type = execute_raw_sql(query, [username])
        
        if user_type:
            user_type = user_type[0][0]
            login(request, user)
            if user_type == 'Candidate':
                request.session['username'] = username
                return redirect('/jobseekerhome/')
            elif user_type == 'Employer':
                return redirect('/employerhome/')
        else:
            messages.error(request, "User type not found")
            return render(request, "login.html")
            
    return render(request, "login.html")

def register(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user_type = request.POST.get('user_type')

        if user_type not in ['Candidate', 'Employer']:
            messages.error(request, "Invalid user type")
            return redirect("/register/")
        
        if User.objects.filter(username=email).exists():
            messages.error(request, "User name taken")
            return redirect("/register/")
         
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password
        )
        user.save()
        
        query = "UPDATE auth_user SET user_type = %s WHERE username = %s"
        execute_raw_sql(query, [user_type, email])

        # Insert default profile data for new users
        insert_query = """
            INSERT INTO candidate_informations (
                user_id, full_name, job_title, phone, email, website,
                current_salary, expected_salary, experience, age,
                education_level, languages, categories, allow_search, description
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = [
            user.id, None, None, None, email, None, None, None, None, None,
            None, None, None, False, None
        ]
        execute_raw_sql(insert_query, params)

        return redirect('/signin/')
    return render(request, "register.html")

def jobseekerhome(request):
    return render(request, "candidate-dashboard.html")

@login_required
def candidate_profile(request):
    if request.method == 'POST':
        user_id = request.user.id
        full_name = request.POST.get('name')
        job_title = request.POST.get('job_title')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        website = request.POST.get('website')
        current_salary = request.POST.get('current_salary', '')
        expected_salary = request.POST.get('expected_salary', '')
        experience = request.POST.get('experience', '')
        age = request.POST.get('age', '')
        education_level = request.POST.get('education_level', '')
        languages = request.POST.get('languages', '')
        categories = ', '.join(request.POST.getlist('categories'))
        allow_search = request.POST.get('allow_search') == 'Yes'
        description = request.POST.get('description', '')

        # Use the email to update existing profile or create a new one
        query = """
            INSERT INTO candidate_informations (
                user_id, full_name, job_title, phone, email, website, 
                current_salary, expected_salary, experience, age, 
                education_level, languages, categories, allow_search, description
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                full_name = VALUES(full_name),
                job_title = VALUES(job_title),
                phone = VALUES(phone),
                website = VALUES(website),
                current_salary = VALUES(current_salary),
                expected_salary = VALUES(expected_salary),
                experience = VALUES(experience),
                age = VALUES(age),
                education_level = VALUES(education_level),
                languages = VALUES(languages),
                categories = VALUES(categories),
                allow_search = VALUES(allow_search),
                description = VALUES(description)
        """
        params = [
            user_id, full_name, job_title, phone, email, website,
            current_salary, expected_salary, experience, age,
            education_level, languages, categories, allow_search, description
        ]
        execute_raw_sql(query, params)

        messages.success(request, "Profile information saved successfully.")
        return redirect('/jobseekerhome/')
    
    # Fetch the saved data from the database (if needed)
    query = "SELECT languages FROM candidate_informations WHERE user_id = %s"
    saved_languages = execute_raw_sql(query, [request.user.id])
    languages = saved_languages[0][0] if saved_languages else ''

    return render(request, "candidate-dashboard-profile.html")

def create_job_opening(request):
    if request.method == "POST":
        # Extract data from POST request
        job_title = request.POST.get('job_title')
        job_description = request.POST.get('job_description')
        email_address = request.POST.get('email_address')
        username = request.POST.get('username')
        specialisms = ','.join(request.POST.getlist('specialisms'))
        job_type = request.POST.get('job_type')

        # Handle the offered salary and remove non-numeric characters except the decimal point
        offered_salary_str = request.POST.get('offered_salary')
        offered_salary = re.sub(r'[^\d.]', '', offered_salary_str) if offered_salary_str else None

        career_level = request.POST.get('career_level')
        experience = request.POST.get('experience')
        gender = request.POST.get('gender')
        industry = request.POST.get('industry')
        qualification = request.POST.get('qualification')

        # Handle the date as text in DD.MM.YYYY format
        application_deadline_date_str = request.POST.get('application_deadline_date')
        if not application_deadline_date_str:
            return HttpResponseBadRequest("Error: Application deadline date is required.")
        
        try:
            day, month, year = map(int, application_deadline_date_str.split('.'))
            application_deadline_date = datetime.date(year, month, day)
        except ValueError:
            return HttpResponseBadRequest("Error: Invalid date format. Use DD.MM.YYYY.")
        
        country = request.POST.get('country')
        city = request.POST.get('city')
        complete_address = request.POST.get('complete_address')
        find_on_map = request.POST.get('find_on_map')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

        # Insert data into the job_openings table
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO job_openings (
                    job_title, job_description, email_address, username, specialisms, job_type, offered_salary, career_level,
                    experience, gender, industry, qualification, application_deadline_date, country, city, complete_address,
                    find_on_map, latitude, longitude
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, [
                job_title, job_description, email_address, username, specialisms, job_type, offered_salary, career_level,
                experience, gender, industry, qualification, application_deadline_date, country, city, complete_address,
                find_on_map, latitude, longitude
            ])

        return redirect('/dashboard-manage-job/')

    return render(request, 'dashboard-post-job.html')

def view_job_openings(request):
    if request.method == "POST":
        # Extract data from POST request
        job_title = request.POST.get('job_title')
        job_description = request.POST.get('job_description')
        email_address = request.POST.get('email_address')
        username = request.POST.get('username')
        specialisms = ','.join(request.POST.getlist('specialisms'))
        job_type = request.POST.get('job_type')

        # Handle the offered salary and remove non-numeric characters except the decimal point
        offered_salary_str = request.POST.get('offered_salary')
        offered_salary = re.sub(r'[^\d.]', '', offered_salary_str) if offered_salary_str else None

        career_level = request.POST.get('career_level')
        experience = request.POST.get('experience')
        gender = request.POST.get('gender')
        industry = request.POST.get('industry')
        qualification = request.POST.get('qualification')

        # Handle the date as text in DD.MM.YYYY format
        application_deadline_date_str = request.POST.get('application_deadline_date')
        if not application_deadline_date_str:
            return HttpResponseBadRequest("Error: Application deadline date is required.")
        
        try:
            day, month, year = map(int, application_deadline_date_str.split('.'))
            application_deadline_date = datetime.date(year, month, day)
        except ValueError:
            return HttpResponseBadRequest("Error: Invalid date format. Use DD.MM.YYYY.")
        
        country = request.POST.get('country')
        city = request.POST.get('city')
        complete_address = request.POST.get('complete_address')
        find_on_map = request.POST.get('find_on_map')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

        # Insert data into the job_openings table
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO job_openings (
                    job_title, job_description, email_address, username, specialisms, job_type, offered_salary, career_level,
                    experience, gender, industry, qualification, application_deadline_date, country, city, complete_address,
                    find_on_map, latitude, longitude
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, [
                job_title, job_description, email_address, username, specialisms, job_type, offered_salary, career_level,
                experience, gender, industry, qualification, application_deadline_date, country, city, complete_address,
                find_on_map, latitude, longitude
            ])

        return redirect('/dashboard-manage-job/')

    return render(request, 'dashboard-manage-job.html')



def dashboard_manage_job(request):
    with connections['default'].cursor() as cursor:
        cursor.execute("""
            SELECT id, job_title, job_description, email_address, username, specialisms, 
                   job_type, offered_salary, career_level, experience, gender, industry, 
                   qualification, application_deadline_date, country, city, complete_address, 
                   find_on_map, latitude, longitude 
            FROM job_openings
        """)
        job_listings = cursor.fetchall()

    # Pass the data to the template
    context = {
        'job_listings': job_listings
    }
    return render(request, 'dashboard-manage-job.html', context)

def employer_home(request):
    return render(request, 'dashboard.html')