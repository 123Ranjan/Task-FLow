from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import datetime, timedelta
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from boards.models import Board
from .models import Issue, Comment
from .serializers import IssueSerializer


# 🔹 CREATE ISSUE (GOES TO BACKLOG)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_issue(request):
    serializer = IssueSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(sprint=None, board=None)
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


# 🔹 GET SINGLE ISSUE
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_issue(request, id):
    try:
        issue = Issue.objects.get(id=id)
    except Issue.DoesNotExist:
        return Response({"error": "Issue not found"}, status=404)
    serializer = IssueSerializer(issue)
    return Response(serializer.data)


# 🔹 BACKLOG (GET ALL ISSUES NOT IN ANY BOARD)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def backlog(request):
    status_filter = request.GET.get("status")
    priority_filter = request.GET.get("priority")
    title_filter = request.GET.get("title")

    issues = Issue.objects.filter(board__isnull=True, sprint__isnull=True)

    if status_filter:
        issues = issues.filter(status=status_filter)
    if priority_filter:
        issues = issues.filter(priority=priority_filter)
    if title_filter:
        issues = issues.filter(title__icontains=title_filter)

    serializer = IssueSerializer(issues, many=True)
    return Response(serializer.data)


# 🔹 ASSIGN ISSUE TO SPRINT
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def assign_to_sprint(request, id):
    try:
        issue = Issue.objects.get(id=id)
    except Issue.DoesNotExist:
        return Response({"error": "Issue not found"}, status=404)

    sprint_id = request.data.get("sprint_id")
    issue.sprint_id = sprint_id
    issue.save()
    return Response({"message": "Moved to sprint"})


# 🔹 MOVE TO BOARD
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def move_to_board(request, id):
    try:
        issue = Issue.objects.get(id=id)
    except Issue.DoesNotExist:
        return Response({"error": "Issue not found"}, status=404)

    board_id = request.data.get('board_id')
    if not board_id:
        return Response({"error": "board_id required"}, status=400)

    try:
        board = Board.objects.get(id=board_id)
        issue.board = board
        issue.status = 'TODO'
        issue.save()
        return Response({"message": f"Moved to board: {board.name}"})
    except Board.DoesNotExist:
        return Response({"error": "Board not found"}, status=404)


# 🔹 MOVE BACK TO BACKLOG
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def move_to_backlog(request, id):
    try:
        issue = Issue.objects.get(id=id)
    except Issue.DoesNotExist:
        return Response({"error": "Issue not found"}, status=404)

    issue.board = None
    issue.sprint = None
    issue.save()
    return Response({"message": "Moved to backlog"})


SCRUM_FLOW = ["TODO", "IN_PROGRESS", "DONE"]
KANBAN_FLOW = ["TODO", "IN_PROGRESS", "BLOCKED", "ABANDONED", "DONE"]


# 🔹 UPDATE STATUS (FOR DRAG & DROP)
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_issue_status(request, id):
    try:
        issue = Issue.objects.get(id=id)
    except Issue.DoesNotExist:
        return Response({"error": "Issue not found"}, status=404)

    new_status = request.data.get("status")
    board_type = request.data.get("board_type", "KANBAN")

    allowed_flow = SCRUM_FLOW if board_type == "SCRUM" else KANBAN_FLOW

    if new_status not in allowed_flow:
        return Response({"error": f"Invalid status. Allowed: {allowed_flow}"}, status=400)

    issue.status = new_status
    issue.save()
    return Response({"message": f"Status updated to {new_status}"})


# 🔹 ADD COMMENT
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_comment(request, issue_id):
    try:
        issue = Issue.objects.get(id=issue_id)
    except Issue.DoesNotExist:
        return Response({"error": "Issue not found"}, status=404)

    Comment.objects.create(
        issue=issue,
        user_email=request.data.get("user_email") or request.user.email,
        text=request.data.get("text")
    )
    return Response({"message": "Comment added"})


# 🔹 GET COMMENTS
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_comments(request, issue_id):
    comments = Comment.objects.filter(issue_id=issue_id)
    data = [
        {"id": c.id, "user": c.user_email, "text": c.text, "time": c.created_at}
        for c in comments
    ]
    return Response(data)


# 🔹 GET BOARD CARDS (FOR BOARD VIEW)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_board_cards(request, board_id):
    board = get_object_or_404(Board, id=board_id)
    issues = Issue.objects.filter(board=board)
    serializer = IssueSerializer(issues, many=True)
    return Response(serializer.data)


# 🔹 MOVE CARD (FOR DRAG & DROP)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def move_card(request, card_id, column_id):
    issue = get_object_or_404(Issue, id=card_id)

    status_map = {
        1: 'TODO',
        2: 'IN_PROGRESS',
        3: 'IN_PROGRESS',
        4: 'DONE'
    }

    new_status = status_map.get(column_id, 'TODO')
    issue.status = new_status
    issue.save()
    return Response({'message': f'Card moved to {new_status}', 'status': new_status})


# ============ DATE/TIME RELATED ENDPOINTS ============

# 🔹 GET OVERDUE TASKS
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_overdue_tasks(request):
    today = timezone.now().date()
    overdue_issues = Issue.objects.filter(
        assigned_email=request.user.email,
        due_date__lt=today,
        status__in=['TODO', 'IN_PROGRESS']
    ).order_by('due_date')

    serializer = IssueSerializer(overdue_issues, many=True)
    return Response({"count": overdue_issues.count(), "overdue_tasks": serializer.data})


# 🔹 GET UPCOMING TASKS (NEXT 7 DAYS)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_upcoming_tasks(request):
    today = timezone.now().date()
    next_week = today + timedelta(days=7)

    upcoming_issues = Issue.objects.filter(
        assigned_email=request.user.email,
        due_date__gte=today,
        due_date__lte=next_week,
        status__in=['TODO', 'IN_PROGRESS']
    ).order_by('due_date')

    serializer = IssueSerializer(upcoming_issues, many=True)
    return Response({"count": upcoming_issues.count(), "upcoming_tasks": serializer.data})


# 🔹 GET TASKS BY SPECIFIC DATE
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_tasks_by_date(request, date_str):
    try:
        target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        issues = Issue.objects.filter(
            assigned_email=request.user.email,
            due_date=target_date
        ).order_by('priority')

        serializer = IssueSerializer(issues, many=True)
        return Response({"date": date_str, "count": issues.count(), "tasks": serializer.data})
    except ValueError:
        return Response({"error": "Invalid date format. Use YYYY-MM-DD"}, status=400)


# 🔹 GET TASKS BY MONTH
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_tasks_by_month(request, year, month):
    try:
        start_date = datetime(int(year), int(month), 1).date()
        if int(month) == 12:
            end_date = datetime(int(year) + 1, 1, 1).date()
        else:
            end_date = datetime(int(year), int(month) + 1, 1).date()

        issues = Issue.objects.filter(
            assigned_email=request.user.email,
            due_date__gte=start_date,
            due_date__lt=end_date
        ).order_by('due_date')

        serializer = IssueSerializer(issues, many=True)
        return Response({"year": year, "month": month, "count": issues.count(), "tasks": serializer.data})
    except ValueError:
        return Response({"error": "Invalid year or month"}, status=400)


# 🔹 UPDATE TASK DUE DATE
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_task_due_date(request, id):
    try:
        issue = Issue.objects.get(id=id)
    except Issue.DoesNotExist:
        return Response({"error": "Issue not found"}, status=404)

    due_date = request.data.get('due_date')
    estimated_hours = request.data.get('estimated_hours')
    actual_hours = request.data.get('actual_hours')

    if due_date:
        try:
            issue.due_date = datetime.strptime(due_date, '%Y-%m-%d').date()
        except ValueError:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD"}, status=400)

    if estimated_hours is not None:
        issue.estimated_hours = estimated_hours
    if actual_hours is not None:
        issue.actual_hours = actual_hours

    issue.save()
    serializer = IssueSerializer(issue)
    return Response({"message": "Task updated successfully", "task": serializer.data})


# 🔹 GET TASK STATISTICS WITH DATES
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_task_statistics(request):
    today = timezone.now().date()

    overdue_count = Issue.objects.filter(
        assigned_email=request.user.email,
        due_date__lt=today,
        status__in=['TODO', 'IN_PROGRESS']
    ).count()

    due_today_count = Issue.objects.filter(
        assigned_email=request.user.email,
        due_date=today,
        status__in=['TODO', 'IN_PROGRESS']
    ).count()

    next_week = today + timedelta(days=7)
    upcoming_count = Issue.objects.filter(
        assigned_email=request.user.email,
        due_date__gt=today,
        due_date__lte=next_week,
        status__in=['TODO', 'IN_PROGRESS']
    ).count()

    no_due_date_count = Issue.objects.filter(
        assigned_email=request.user.email,
        due_date__isnull=True,
        status__in=['TODO', 'IN_PROGRESS']
    ).count()

    return Response({
        "overdue_tasks": overdue_count,
        "due_today": due_today_count,
        "upcoming_this_week": upcoming_count,
        "no_due_date": no_due_date_count,
        "today_date": today.strftime("%Y-%m-%d")
    })