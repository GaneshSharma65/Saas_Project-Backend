from django.shortcuts import render

# Create your views here.
import json
import subprocess
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .models import Project
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        user = authenticate(username=username, password=password)
        if user:
            return JsonResponse({'status': 'success', 'user_id': user.id})
        else:
            return JsonResponse({'status': 'fail', 'message': 'Invalid credentials'}, status=401)
    
   
    return JsonResponse({'error': 'Only POST method is allowed'}, status=405)

@csrf_exempt
def create_project(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            name = data.get("name")
            desc = data.get("description")
            user_id = data.get("created_by")

            user = User.objects.get(id=user_id)
            project = Project.objects.create(name=name, description=desc, created_by=user)

            db_name = f"project_{project.id}"

            
            create_new_db(db_name)

            return JsonResponse({"status": "success", "project_id": project.id})
        
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)


def list_projects(request):
    if request.method == "GET":
        projects = Project.objects.all().values("id", "name", "description", "created_by__username", "created_at")
        return JsonResponse(list(projects), safe=False)


def create_new_db(db_name):
    conn = psycopg2.connect(dbname='postgres', user='postgres', password='Tiger99@@', host='localhost')
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute(f'CREATE DATABASE "{db_name}";')
    cur.close()
    conn.close()