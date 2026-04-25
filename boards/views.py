from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from .models import Board
from .serializers import BoardSerializer
from users.utils import is_admin_or_manager
import uuid


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_boards(request):
    """Get all boards for the current user"""
    try:
        boards = Board.objects.filter(created_by=request.user.email)
        serializer = BoardSerializer(boards, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({"error": str(e)}, status=500)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_board_details(request, id):
    """Get single board details"""
    try:
        board = get_object_or_404(Board, id=id)
        serializer = BoardSerializer(board)
        return Response(serializer.data)
    except Exception as e:
        return Response({"error": str(e)}, status=500)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_board_issues(request, id):
    """Get all issues for a specific board"""
    try:
        from issues.models import Issue
        from issues.serializers import IssueSerializer
        board = get_object_or_404(Board, id=id)
        issues = Issue.objects.filter(board=board)
        serializer = IssueSerializer(issues, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({"error": str(e)}, status=500)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_board(request):
    """Create a new board"""
    if not is_admin_or_manager(request.user):
        return Response({"error": "Permission denied. Only Admins and Managers can create boards."}, status=403)

    data = request.data
    board_name = data.get('boardName') or data.get('name')

    # 🔧 FIX THIS LINE - Make sure it gets 'SCRUM' correctly
    board_type = data.get('boardType', 'KANBAN')

    # 🔧 DEBUG - Print to see what's coming
    print(f"=== CREATE BOARD DEBUG ===")
    print(f"Raw data: {data}")
    print(f"boardType from request: {data.get('boardType')}")
    print(f"Final board_type value: {board_type}")
    print(f"board_type == 'SCRUM'? {board_type == 'SCRUM'}")

    project_key = data.get('projectKey', str(uuid.uuid4())[:8].upper())

    if not board_name:
        return Response({"error": "Board name is required"}, status=400)

    try:
        board = Board.objects.create(
            name=board_name,
            board_type=board_type,  # This should be 'SCRUM'
            project_key=project_key,
            created_by=request.user.email
        )
        print(f"✅ Board created with type: {board.board_type}")
        serializer = BoardSerializer(board)
        return Response(serializer.data, status=201)
    except IntegrityError:
        return Response({"error": "A board with this Project Key already exists"}, status=400)
    except Exception as e:
        print(f"❌ Error: {e}")
        return Response({"error": str(e)}, status=500)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_board(request, id):
    """Delete a board"""
    if not is_admin_or_manager(request.user):
        return Response({"error": "Permission denied. Only Admins and Managers can delete boards."}, status=403)

    try:
        board = get_object_or_404(Board, id=id)
        board.delete()
        return Response({"message": "Board deleted successfully"}, status=200)
    except Exception as e:
        return Response({"error": str(e)}, status=500)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_board_columns(request, id):
    """Get columns for a board (for Kanban view)"""
    try:
        board = get_object_or_404(Board, id=id)

        # Default columns based on board type
        if board.board_type == 'SCRUM':
            default_columns = ['TODO', 'IN_PROGRESS', 'REVIEW', 'DONE']
        else:
            default_columns = ['TODO', 'IN_PROGRESS', 'DONE']

        columns = [
            {'id': i + 1, 'name': col, 'position': i}
            for i, col in enumerate(default_columns)
        ]
        return Response(columns)
    except Exception as e:
        return Response({"error": str(e)}, status=500)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_board_column(request, id):
    """Create a new column for a board"""
    try:
        board = get_object_or_404(Board, id=id)
        data = request.data
        column_name = data.get('columnName')

        if not column_name:
            return Response({"error": "Column name is required"}, status=400)

        # For now, return success with generated ID
        # You can create a Column model later if needed
        return Response({
            'id': 999,
            'name': column_name,
            'position': data.get('position', 0)
        }, status=201)
    except Exception as e:
        return Response({"error": str(e)}, status=500)