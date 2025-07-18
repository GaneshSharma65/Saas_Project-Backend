import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import Assessment, Score
from students.models import Student
from django.db.models import Sum

@csrf_exempt
def add_assessment(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            db_name = f"project_{data.get('project_id')}"

            assessment = Assessment.objects.using(db_name).create(
                title=data["title"],
                chapter=data["chapter"],
                week=data["week"],
                total_marks=data["total_marks"]
            )
            return JsonResponse({"status": "success", "assessment_id": assessment.id})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

    return JsonResponse({"error": "Only POST allowed"}, status=405)


@csrf_exempt
def add_score(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            db_name = f"project_{data.get('project_id')}"

            score = Score.objects.using(db_name).create(
                student_id=data["student_id"],
                assessment_id=data["assessment_id"],
                marks=data["marks"]
            )
            return JsonResponse({"status": "success", "score_id": score.id})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

    return JsonResponse({"error": "Only POST allowed"}, status=405)


@csrf_exempt
def update_score(request, score_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            db_name = f"project_{data.get('project_id')}"

            score = Score.objects.using(db_name).get(id=score_id)
            score.marks = data["marks"]
            score.save(using=db_name)

            return JsonResponse({"status": "success", "message": "Score updated"})
        except Score.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Score not found"}, status=404)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

    return JsonResponse({"error": "Only POST allowed"}, status=405)


@csrf_exempt
def delete_score(request, score_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            db_name = f"project_{data.get('project_id')}"

            score = Score.objects.using(db_name).get(id=score_id)
            score.delete(using=db_name)

            return JsonResponse({"status": "success", "message": "Score deleted"})
        except Score.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Score not found"}, status=404)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

    return JsonResponse({"error": "Only POST allowed"}, status=405)


@csrf_exempt
def student_progress_report(request, project_id, student_id):
    if request.method == "GET":
        db_name = f"project_{project_id}"

        try:
            student = Student.objects.using(db_name).get(id=student_id)
        except Student.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Student not found"}, status=404)

        scores = Score.objects.using(db_name).filter(student_id=student_id)
        assessments = Assessment.objects.using(db_name).filter(id__in=scores.values_list('assessment_id', flat=True))
        
        total_marks = assessments.aggregate(Sum("total_marks"))["total_marks__sum"] or 0
        scored = scores.aggregate(Sum("marks"))["marks__sum"] or 0

        percentage = (scored / total_marks * 100) if total_marks > 0 else 0
        percentage = round(percentage, 2)

        if percentage >= 80:
            status = "Excellent"
        elif percentage >= 50:
            status = "Good"
        else:
            status = "Needs Improvement"

        score_details = [
            {
                "assessment": s.assessment.title,
                "marks_scored": s.marks,
                "total_marks": s.assessment.total_marks,
                "week": s.assessment.week
            }
            for s in scores.select_related('assessment')
        ]

        report = {
            "student_id": student.id,
            "name": student.name,
            "total_marks": total_marks,
            "scored_marks": scored,
            "percentage": percentage,
            "status": status,
            "scores": score_details
        }

        return JsonResponse(report, safe=False)

    return JsonResponse({"error": "Only GET allowed"}, status=405)


@csrf_exempt
def weekly_progress(request, project_id, week):
    if request.method == "GET":
        db_name = f"project_{project_id}"

        students = Student.objects.using(db_name).all()
        assessments = Assessment.objects.using(db_name).filter(week=week)
        scores = Score.objects.using(db_name).filter(assessment__in=assessments)

        total_marks = assessments.aggregate(Sum("total_marks"))["total_marks__sum"] or 0

        progress_list = []

        for student in students:
            student_scores = scores.filter(student_id=student.id)
            scored = student_scores.aggregate(Sum("marks"))["marks__sum"]

            if scored is None:
                percentage = "Not Available"
                scored_marks = "Not Available"
                status = "Not Attempted"
            else:
                scored_marks = scored
                percentage = (scored / total_marks * 100) if total_marks > 0 else 0
                percentage = round(percentage, 2)

                if percentage >= 80:
                    status = "Excellent"
                elif percentage >= 50:
                    status = "Good"
                else:
                    status = "Needs Improvement"

            progress_list.append({
                "student_id": student.id,
                "name": student.name,
                "total_marks": total_marks if total_marks > 0 else "Not Available",
                "scored_marks": scored_marks,
                "percentage": percentage,
                "status": status
            })

        return JsonResponse(progress_list, safe=False)

    return JsonResponse({"error": "Only GET allowed"}, status=405)
