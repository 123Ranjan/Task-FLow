from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Sprint
from .serializers import SprintSerializer
from boards.models import Board
from users.utils import is_admin_or_manager
from issues.models import Issue


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_sprints(request):
    """Get all sprints for the user's boards"""
    sprints = Sprint.objects.filter(board__created_by=request.user.email)
    serializer = SprintSerializer(sprints, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_sprints_by_board(request, board_id):
    """Get sprints for a specific board"""
    board = get_object_or_404(Board, id=board_id)
    sprints = Sprint.objects.filter(board=board)
    serializer = SprintSerializer(sprints, many=True)

    # Add statistics to each sprint
    data = []
    for sprint in sprints:
        sprint_data = serializer.data
        issues = Issue.objects.filter(sprint=sprint)
        sprint_data['issue_count'] = issues.count()
        sprint_data['completed_issues'] = issues.filter(status='DONE').count()
        data.append(sprint_data)

    return Response(data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_sprint(request):
    """Create a new sprint"""
    if not is_admin_or_manager(request.user):
        return Response({"error": "Permission denied"}, status=403)

    data = request.data
    board_id = data.get('board_id')
    board = None

    if board_id:
        board = get_object_or_404(Board, id=board_id)

    sprint = Sprint.objects.create(
        name=data.get('name'),
        start_date=data.get('start_date'),
        end_date=data.get('end_date'),
        goal=data.get('goal', ''),
        board=board,
        status='PLANNED'
    )

    serializer = SprintSerializer(sprint)
    return Response(serializer.data, status=201)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def start_sprint(request, sprint_id):
    """Start a sprint (change status to ACTIVE)"""
    if not is_admin_or_manager(request.user):
        return Response({"error": "Permission denied"}, status=403)

    sprint = get_object_or_404(Sprint, id=sprint_id)
    sprint.status = 'ACTIVE'
    sprint.save()
    return Response({"message": "Sprint started successfully"})


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def close_sprint(request, sprint_id):
    """Close/complete a sprint"""
    if not is_admin_or_manager(request.user):
        return Response({"error": "Permission denied"}, status=403)

    sprint = get_object_or_404(Sprint, id=sprint_id)
    sprint.status = 'COMPLETED'

    # Calculate completed points
    issues = Issue.objects.filter(sprint=sprint, status='DONE')
    sprint.completed_points = sum(issue.story_points for issue in issues if hasattr(issue, 'story_points'))
    sprint.completed_issues = issues.count()
    sprint.save()

    return Response({"message": "Sprint completed successfully"})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_sprint_issues(request, sprint_id):
    """Get all issues in a sprint"""
    sprint = get_object_or_404(Sprint, id=sprint_id)
    issues = Issue.objects.filter(sprint=sprint)
    from issues.serializers import IssueSerializer
    serializer = IssueSerializer(issues, many=True)
    return Response(serializer.data)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_sprint(request, sprint_id):
    """Delete a sprint"""
    if not is_admin_or_manager(request.user):
        return Response({"error": "Permission denied. Only Admins and Managers can delete sprints."}, status=403)

    try:
        sprint = get_object_or_404(Sprint, id=sprint_id)
        sprint.delete()
        return Response({"message": "Sprint deleted successfully"}, status=200)
    except Exception as e:
        return Response({"error": str(e)}, status=500)