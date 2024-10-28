from user.models import User
from .models import Document, JobApplication, AppliedApplication
from django.http import JsonResponse, HttpResponseBadRequest
from django.forms.models import model_to_dict
import json, os
from django.views.decorators.csrf import csrf_exempt



def all_students(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_email = data.get("user")
        if not user_email:
            return HttpResponseBadRequest("User email not provided")

        try:
            user = User.objects.get(reg_no=user_email)
        except User.DoesNotExist:
            return HttpResponseBadRequest("User not found")

        if user.is_staff:
            students = User.objects.all().filter(is_student=True)
        elif user.is_cse:
            students = User.objects.filter(batch__contains="CSE").filter(is_student=True)
        elif user.is_ece:
            students = User.objects.filter(batch__contains="ECE").filter(is_student=True)
        elif user.is_eee:
            students = User.objects.filter(batch__contains="EEE").filter(is_student=True)
        elif user.is_mech:
            students = User.objects.filter(batch__contains="MECH").filter(is_student=True)
        elif user.is_csse:
            students = User.objects.filter(batch__contains="CSSE").filter(is_student=True)
        elif user.is_csit:
            students = User.objects.filter(batch__contains="CSIT").filter(is_student=True)
        elif user.is_csm:
            students = User.objects.filter(batch__contains="CSM").filter(is_student=True)
        else:
            return HttpResponseBadRequest("Invalid user type")

        return JsonResponse(list(students.values()), safe=False)
    else:
        return HttpResponseBadRequest("Invalid request method")


def student(request, pk):
    student = User.objects.get(reg_no=pk)
    student_dict = model_to_dict(student)

    student_dict["documents"] = [
        {
            "id": doc.id,
            "type": doc.type,
            "url": request.build_absolute_uri(
                doc.document.url
            ),
        }
        for doc in student.documents.all()
    ]

    return JsonResponse(student_dict, safe=False)



def add_drive_data(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)
            print(body)
            for i in body['results']:
                student = User.objects.get(reg_no=i['reg_no'])
                if student.drives is None:
                    student.drives = {} 
                company_name = i.get('companyName')
                if company_name:
                    student.drives[company_name] = {'drives': i.get('drives'), 'selected': i.get('selected')}
                else:
                    print("Company name is missing")
                student.save()

            return JsonResponse({'status': 'success'}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({'error': 'Internal server error'}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)



def upload_resume(request, type):
    if request.method == "POST":
        resume_file = request.FILES.get("resume")
        student_id = request.POST.get("student_id")
        if resume_file:
            document = Document.objects.create(document=resume_file, type=type)
            student = User.objects.get(reg_no=student_id)
            student.documents.add(document)
            student.save()
            response_data = {
                "message": "Upload successful",
                "student_id": student_id,
                "file_name": document.document.name,
            }
            return JsonResponse(response_data, status=201)
        else:
            return JsonResponse({"error": "Invalid data"}, status=400)
    return JsonResponse({"error": "Invalid method"}, status=405)


def delete_file(request, file_id):
    if request.method == 'POST':
        document = Document.objects.get(id=file_id)
        del document
        response_data = {
            "message": "Delete successful",
        }
        return JsonResponse(response_data, status=201)
    else:
        return JsonResponse({"error": "Invalid data"}, status=400)


def add_job_applications(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)
            company_name = body.get('companyName')
            job_description = body.get('jobDescription')
            application_deadline = body.get('applicationDeadline')
            drive_date = body.get('driveDate')
            job_application_link = body.get('jobApplicationLink')
            
            
            if not all([company_name, job_description, application_deadline, drive_date, job_application_link]):
                return JsonResponse({'error': 'All fields are required'}, status=400)            
                
            job_application = JobApplication(
                company_name=company_name,
                job_description=job_description,
                application_deadline=application_deadline,
                drive_date=drive_date,
                job_application_link=job_application_link
            )
            job_application.save()
            return JsonResponse({'status': 'success', 'message': 'Job application created successfully', 'id':job_application.id}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({'error': 'Internal server error'}, status=500) 

    return JsonResponse({'error': 'Invalid request method'}, status=405) 


def delete_job_application(request, pk):
    if request.method == 'POST':
        job_application = JobApplication.objects.get(id=pk)
        job_application.delete()
        response_data = {
            "message": "Delete successful",
        }
        return JsonResponse(response_data, status=201)
    else:
        return JsonResponse({"error": "Invalid data"}, status=400)



def edit_job_application(request, pk):
    if request.method == "POST":
        try:
            body = json.loads(request.body)
            company_name = body.get("company_name")
            job_description = body.get("job_description")
            application_deadline = body.get("application_deadline")
            drive_date = body.get("drive_date")
            job_application_link = body.get("job_application_link")

            if not all(
                [
                    company_name,
                    job_description,
                    application_deadline,
                    drive_date,
                    job_application_link,
                ]
            ):
                return JsonResponse({"error": "All fields are required"}, status=400)

            job_application = JobApplication.objects.get(id=pk)
            job_application.company_name = company_name
            job_application.job_description = job_description
            job_application.application_deadline = application_deadline
            job_application.drive_date = drive_date
            job_application.job_application_link = (
                job_application_link  # Corrected this line
            )
            job_application.save()

            return JsonResponse(
                {
                    "status": "success",
                    "message": "Job application updated successfully",
                },
                status=200,
            )
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except JobApplication.DoesNotExist:
            return JsonResponse({"error": "Job application not found"}, status=404)

    return JsonResponse({"error": "Invalid request method"}, status=405)


def job_application(request, pk):
    job_application = JobApplication.objects.get(pk=pk)
    job_application_dict = model_to_dict(job_application)
    return JsonResponse(job_application_dict, safe=False)

def get_all_job_applications(request):
    job_applications = JobApplication.objects.all()
    job_applications_list = [model_to_dict(job_application) for job_application in job_applications]
    return JsonResponse(job_applications_list, safe=False)


def submit_application(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)
            applied = body.get('applied')
            job_id = body.get('job_id')
            date_applied = body.get('date_applied')
            reg_no = body.get('reg_no')


            student = User.objects.get(reg_no=reg_no)
            job = JobApplication.objects.get(pk=job_id)
            applied_application = AppliedApplication.objects.create(
                student=student, job=job, applied_at=date_applied, has_applied=True,
            )

            return JsonResponse(
                {
                    "status": "success",
                    "message": "Job application updated successfully",
                    "applied": applied,
                    "job_id": job_id,
                    "date_applied": date_applied,
                    "reg_no": reg_no,
                },
                status=200,
            )
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except JobApplication.DoesNotExist:
            return JsonResponse({"error": "Job application not found"}, status=404)

    return JsonResponse({"error": "Invalid request method"}, status=405)



def get_applied_applications(request):
    if request.method == "POST":
        body = json.loads(request.body)
        print(body.get("reg_no"))
        student = User.objects.get(reg_no = body.get("reg_no"))
        applied_applications = student.applied_application.all()
        applied_applications_list = [model_to_dict(applied_application) for applied_application in applied_applications]
        return JsonResponse(applied_applications_list, safe=False)
    return JsonResponse({"error": "Invalid request method"}, status=405)



def get_applied_students(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)
            job = JobApplication.objects.get(company_name=body.get("job_name"))
            applied_applications = AppliedApplication.objects.filter(job=job)
            students = []

            for application in applied_applications:
                student = application.student
                students.append(
                    {
                        "id": job.company_name,
                        "email": student.email,
                        "appliedAt": application.applied_at,
                    }
                )

            return JsonResponse(students, safe=False)
        except JobApplication.DoesNotExist:
            return JsonResponse({"error": "Job not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)
def job_company_name(request):
    if request.method == "GET":
        job_applications = JobApplication.objects.all()
        company_names = [job.company_name for job in job_applications]
        if company_names:
            return JsonResponse(company_names, safe=False)
        else:
            return JsonResponse({"error": "No companies found"}, status=404)