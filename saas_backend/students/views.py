from django.conf import settings
from django.db import connections
import json
from django.http import JsonResponse
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from .models import Student
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def add_student(request):
    if request.method == "POST":
        data = json.loads(request.body)
        name = data.get("name")
        roll = data.get("roll_number")
        class_name = data.get("class_name")
        section = data.get("section")
        project_id = data.get("project_id")
        db_name = f"project_{project_id}"

    if db_name not in settings.DATABASES:
            settings.DATABASES[db_name] = {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': 'project_1',
                'USER': 'postgres',
                'PASSWORD': 'Tiger99@@',
                'HOST': 'localhost',
                'PORT': '5432',
            }

    try:
            connections[db_name].ensure_connection()
            Student.objects.using(db_name).create(
                name=name,
                roll_number=roll,
                class_name=class_name,
                section=section
            )
            return JsonResponse({"status": "success"})
    except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

    return JsonResponse({"error": "Only POST method allowed"}, status=405)



def create_new_db(db_name):
    conn = psycopg2.connect(dbname='project_1', user='postgres', password='Tiger99@@', host='localhost')
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute(f'CREATE DATABASE "{db_name}";')
    cur.close()
    conn.close()


def list_students(request):
    project_id = request.GET.get("project_id")
    db_name = f"project_{project_id}"
    
    try:
        students = Student.objects.using(db_name).all().values()
        return JsonResponse(list(students), safe=False)
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=400)
    
@csrf_exempt
def update_student(request, student_id):
    if request.method == "PUT":
        data = json.loads(request.body)
        db_name = f"project_{data.get('project_id')}"

        try:
            student = Student.objects.using(db_name).get(id=student_id)
            student.name = data.get("name", student.name)
            student.roll_number = data.get("roll_number", student.roll_number)
            student.class_name = data.get("class_name", student.class_name)
            student.section = data.get("section", student.section)
            student.save(using=db_name)
            return JsonResponse({"status": "success", "message": "Student updated successfully"})
        except Student.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Student not found"}, status=404)
    return JsonResponse({'error': 'Only PUT method is allowed'}, status=405)

        
        
        
@csrf_exempt
def delete_student(request, student_id):
    if request.method == "DELETE":
        try:
            data = json.loads(request.body)
            db_name = f"project_{data.get('project_id')}"
            student = Student.objects.using(db_name).get(id=student_id)
            student.delete(using=db_name)
            return JsonResponse({"status": "success", "message": "Student deleted successfully"})
        except Student.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Student not found"}, status=404)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
    return JsonResponse({"error": "Only DELETE method is allowed"}, status=405)

