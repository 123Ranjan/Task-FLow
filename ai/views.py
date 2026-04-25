from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Count, Q
from datetime import datetime, timedelta
from boards.models import Board
from issues.models import Issue
from sprints.models import Sprint
from notifications.models import Notification
from django.contrib.auth import get_user_model

User = get_user_model()


def get_smart_date_time_response(message, user, stats, issues):
    """Generate intelligent date/time responses"""
    now = datetime.now()

    if any(word in message for word in ['current date', 'today date', 'what date', 'todays date', 'date today']):
        return f"""📅 **Today's Date**

{now.strftime('%A, %B %d, %Y')}

⏰ **Current Time:** {now.strftime('%I:%M %p')}

📊 **Today's Overview:**
• Due today: {stats.get('due_today', 0)} tasks
• Overdue: {stats.get('overdue_tasks', 0)} tasks
• Upcoming this week: {stats.get('upcoming_this_week', 0)} tasks"""

    if 'current time' in message or 'what time' in message or 'time now' in message:
        return f"""⏰ **Current Time**

{now.strftime('%I:%M:%S %p')}

📅 **Date:** {now.strftime('%B %d, %Y')}"""

    if 'what day' in message or 'day of week' in message:
        return f"""📅 **Today is {now.strftime('%A')}**

• Day #{now.strftime('%j')} of the year
• Week #{now.strftime('%W')} of the year"""

    if 'tomorrow' in message:
        tomorrow = now + timedelta(days=1)
        return f"📅 **Tomorrow is {tomorrow.strftime('%A, %B %d, %Y')}**"

    if 'yesterday' in message:
        yesterday = now - timedelta(days=1)
        return f"📅 **Yesterday was {yesterday.strftime('%A, %B %d, %Y')}**"

    return None


def get_deadline_insights(issues, stats):
    """Get deadline-based insights"""
    today = datetime.now().date()

    overdue = issues.filter(due_date__lt=today, status__in=['TODO', 'IN_PROGRESS'])
    due_today = issues.filter(due_date=today, status__in=['TODO', 'IN_PROGRESS'])
    due_tomorrow = issues.filter(due_date=today + timedelta(days=1), status__in=['TODO', 'IN_PROGRESS'])

    if overdue.count() == 0 and due_today.count() == 0 and due_tomorrow.count() == 0:
        return None

    response = "⏰ **Deadline Insights**\n\n"
    if overdue.count() > 0:
        response += f"⚠️ **Overdue:** {overdue.count()} task(s) past deadline!\n"
    if due_today.count() > 0:
        response += f"🔴 **Due TODAY:** {due_today.count()} task(s) need immediate attention\n"
    if due_tomorrow.count() > 0:
        response += f"🟡 **Due Tomorrow:** {due_tomorrow.count()} task(s)\n"

    response += "\n💡 **Tip:** Focus on overdue and due-today tasks first!"
    return response


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def smart_chat(request):
    """Advanced AI Assistant for Task Management - Answers EVERYTHING about your system"""

    try:
        message = request.data.get('message', '').lower().strip()

        # Get ALL user data
        user = request.user
        boards = Board.objects.filter(created_by=user.email)
        issues = Issue.objects.filter(assigned_email=user.email)
        sprints = Sprint.objects.filter(board__created_by=user.email)
        notifications = Notification.objects.filter(user=user) if hasattr(Notification, 'user') else []

        # Calculate comprehensive stats
        stats = {
            'total_boards': boards.count(),
            'scrum_boards': boards.filter(board_type='SCRUM').count(),
            'kanban_boards': boards.filter(board_type='KANBAN').count(),
            'total_issues': issues.count(),
            'completed': issues.filter(status='DONE').count(),
            'in_progress': issues.filter(status='IN_PROGRESS').count(),
            'todo': issues.filter(status='TODO').count(),
            'high_priority': issues.filter(priority='HIGH', status__in=['TODO', 'IN_PROGRESS']).count(),
            'medium_priority': issues.filter(priority='MEDIUM', status__in=['TODO', 'IN_PROGRESS']).count(),
            'low_priority': issues.filter(priority='LOW', status__in=['TODO', 'IN_PROGRESS']).count(),
            'total_sprints': sprints.count(),
            'active_sprints': sprints.filter(status='ACTIVE').count(),
            'completed_sprints': sprints.filter(status='COMPLETED').count(),
            'planned_sprints': sprints.filter(status='PLANNED').count(),
            'unread_notifications': notifications.count() if notifications else 0,
            'completion_rate': round(
                (issues.filter(status='DONE').count() / issues.count() * 100) if issues.count() > 0 else 0),
            'due_today': issues.filter(due_date=datetime.now().date(), status__in=['TODO', 'IN_PROGRESS']).count(),
            'overdue_tasks': issues.filter(due_date__lt=datetime.now().date(), status__in=['TODO', 'IN_PROGRESS']).count(),
            'upcoming_this_week': issues.filter(due_date__gte=datetime.now().date(), due_date__lte=datetime.now().date() + timedelta(days=7), status__in=['TODO', 'IN_PROGRESS']).count()
        }

        # Generate response - handles ANY question
        response = generate_intelligent_response(message, stats, user, boards, issues, sprints, notifications)

        return Response({"response": response})

    except Exception as e:
        print(f"AI Error: {e}")
        import traceback
        traceback.print_exc()
        return Response({"response": "I'm having trouble processing your request. Please try again."})


def generate_intelligent_response(message, stats, user, boards, issues, sprints, notifications):
    """Generate intelligent response for ANY question about the system"""

    # ============ DATE & TIME QUESTIONS (ADDED) ============
    date_response = get_smart_date_time_response(message, user, stats, issues)
    if date_response:
        return date_response

    # ============ DEADLINE QUESTIONS ============
    if any(word in message for word in ['deadline', 'due', 'overdue', 'whats due', 'pending deadlines']):
        deadline_insight = get_deadline_insights(issues, stats)
        if deadline_insight:
            return deadline_insight
        return "📋 **No pending deadlines!** All your tasks are on track. Great job! 🎉"

    # ============ TODAY'S TASKS ============
    if 'today\'s tasks' in message or 'tasks due today' in message:
        today = datetime.now().date()
        tasks_today = issues.filter(due_date=today, status__in=['TODO', 'IN_PROGRESS'])

        if tasks_today.count() == 0:
            return f"📅 **No tasks due today!**\n\nYou have {stats['todo']} pending tasks but none are due today. Use this time to make progress! 🚀"

        task_list = "\n".join([f"• **{t.title}** ({t.priority})" for t in tasks_today[:5]])
        return f"📅 **Tasks Due Today ({tasks_today.count()})**\n\n{task_list}\n\n💡 Focus on completing these first!"

    # ============ THIS WEEK'S TASKS ============
    if 'this week' in message and 'tasks' in message:
        today = datetime.now().date()
        end_of_week = today + timedelta(days=7)
        tasks_week = issues.filter(due_date__gte=today, due_date__lte=end_of_week, status__in=['TODO', 'IN_PROGRESS'])

        if tasks_week.count() == 0:
            return f"📅 **No deadlines this week!**\n\nYou have {stats['todo']} pending tasks. Consider setting due dates to stay organized! 📝"

        return f"📅 **Tasks Due This Week ({tasks_week.count()})**\n\nYou have {tasks_week.count()} tasks with deadlines in the next 7 days.\n\n💡 Plan your week to meet these deadlines!"

    # ============ USER PROFILE QUESTIONS ============
    if any(word in message for word in ['username', 'user name', 'my name']):
        return f"👤 **Your Username:** `{user.username}`\n\n📧 Email: {user.email}\n👔 Role: {getattr(user, 'role', 'Member')}"

    if 'email' in message:
        return f"📧 **Your Email:** `{user.email}`"

    if 'role' in message:
        return f"👔 **Your Role:** `{getattr(user, 'role', 'Member')}`\n\n💡 As a {getattr(user, 'role', 'Member')}, you have appropriate permissions for boards, sprints, and tasks."

    if 'bio' in message:
        bio = getattr(user, 'bio', None) or 'No bio added yet'
        return f"📝 **Your Bio:** {bio}\n\n💡 You can update your bio in Profile settings."

    if 'joined' in message or 'member since' in message:
        joined = user.date_joined.strftime("%B %d, %Y") if hasattr(user, 'date_joined') else "Recently"
        return f"📅 **Member Since:** {joined}\n\n🎉 Thank you for being part of TaskFlow!"

    # ============ BOARD QUESTIONS ============
    if 'board' in message:
        if 'how many' in message or 'count' in message or 'total' in message:
            return f"📊 **Board Statistics:**\n\n• Total Boards: **{stats['total_boards']}**\n• 🏃 Scrum Boards: **{stats['scrum_boards']}**\n• 📋 Kanban Boards: **{stats['kanban_boards']}**"

        if 'name' in message or 'list' in message or 'show' in message:
            if not boards.exists():
                return "📊 **No boards found.** Create your first board to get started!"

            board_list = "\n".join([f"• **{b.name}** ({b.board_type}) - Key: {b.project_key or 'N/A'}" for b in boards])
            return f"📊 **Your Boards:**\n\n{board_list}"

        if 'scrum' in message:
            scrum_boards = boards.filter(board_type='SCRUM')
            if not scrum_boards.exists():
                return "🏃 **No Scrum boards found.** Create a Scrum board for sprint-based development!"
            return f"🏃 **Scrum Boards ({scrum_boards.count()}):**\n\n" + "\n".join([f"• **{b.name}**" for b in scrum_boards])

        if 'kanban' in message:
            kanban_boards = boards.filter(board_type='KANBAN')
            if not kanban_boards.exists():
                return "📋 **No Kanban boards found.** Create a Kanban board for continuous workflow!"
            return f"📋 **Kanban Boards ({kanban_boards.count()}):**\n\n" + "\n".join([f"• **{b.name}**" for b in kanban_boards])

        if 'project key' in message or 'key' in message:
            if not boards.exists():
                return "🔑 No boards found to show project keys."
            keys = "\n".join([f"• **{b.name}** → `{b.project_key or 'Not set'}`" for b in boards])
            return f"🔑 **Project Keys:**\n\n{keys}"

        return get_board_insights(boards, stats)

    # ============ BACKLOG/TASK QUESTIONS ============
    if any(word in message for word in ['task', 'issue', 'backlog', 'todo', 'pending']):
        if 'how many' in message or 'count' in message or 'total' in message:
            return f"📋 **Task Statistics:**\n\n• Total Tasks: **{stats['total_issues']}**\n• ✅ Completed: **{stats['completed']}**\n• 🏃 In Progress: **{stats['in_progress']}**\n• 📝 To Do: **{stats['todo']}**\n• 📈 Completion Rate: **{stats['completion_rate']}%**"

        if 'high priority' in message:
            high_tasks = issues.filter(priority='HIGH', status__in=['TODO', 'IN_PROGRESS'])
            if not high_tasks.exists():
                return "✅ **Great news!** You have no pending high priority tasks."
            return f"⚠️ **High Priority Tasks ({high_tasks.count()}):**\n\n" + "\n".join([f"• **{t.title}** - {t.status}" for t in high_tasks[:5]])

        if 'completed' in message:
            completed = issues.filter(status='DONE')
            if not completed.exists():
                return "📋 **No completed tasks yet.** Start working on your tasks!"
            return f"✅ **Completed Tasks ({completed.count()}):**\n\n" + "\n".join([f"• **{t.title}**" for t in completed[:5]])

        if 'in progress' in message:
            in_progress = issues.filter(status='IN_PROGRESS')
            if not in_progress.exists():
                return "🏃 **No tasks in progress.** Start working on a task!"
            return f"🏃 **Tasks In Progress ({in_progress.count()}):**\n\n" + "\n".join([f"• **{t.title}**" for t in in_progress])

        return get_backlog_insights(issues, stats)

    # ============ SPRINT QUESTIONS ============
    if 'sprint' in message:
        if 'how many' in message or 'count' in message or 'total' in message:
            return f"🏃 **Sprint Statistics:**\n\n• Total Sprints: **{stats['total_sprints']}**\n• Active: **{stats['active_sprints']}**\n• Completed: **{stats['completed_sprints']}**\n• Planned: **{stats['planned_sprints']}**"

        if 'active' in message or 'current' in message:
            active = sprints.filter(status='ACTIVE').first()
            if not active:
                return "🏃 **No active sprint.** Start a sprint to begin tracking progress!"
            return get_sprint_progress(sprints, issues, stats)

        if 'name' in message or 'list' in message:
            if not sprints.exists():
                return "🏃 **No sprints found.** Create your first sprint!"
            sprint_list = "\n".join([f"• **{s.name}** - {s.status} ({s.start_date or 'No date'} to {s.end_date or 'No date'})" for s in sprints])
            return f"🏃 **Your Sprints:**\n\n{sprint_list}"

        if 'goal' in message:
            active = sprints.filter(status='ACTIVE').first()
            if active and active.goal:
                return f"🎯 **Current Sprint Goal:** {active.goal}"
            return "🎯 **No sprint goal set.** You can add a goal when creating or editing a sprint."

        return get_sprint_insights(sprints, stats)

    # ============ NOTIFICATION QUESTIONS ============
    if any(word in message for word in ['notification', 'notif', 'alert', 'bell']):
        if 'how many' in message or 'count' in message:
            return f"🔔 **Notifications:** You have **{stats['unread_notifications']}** unread notification(s)."
        return get_notification_status(stats)

    # ============ ANALYTICS QUESTIONS ============
    if any(word in message for word in ['analytics', 'report', 'statistic', 'performance', 'progress']):
        return generate_detailed_report(stats, issues)

    # ============ COMPLETION RATE QUESTIONS ============
    if 'completion' in message or 'complete rate' in message:
        return f"📈 **Your Completion Rate:** **{stats['completion_rate']}%**\n\n• Completed: {stats['completed']}/{stats['total_issues']} tasks\n\n{get_motivation_message(stats['completion_rate'])}"

    # ============ GREETINGS ============
    if any(word in message for word in ['hi', 'hello', 'hey', 'greetings']):
        return f"""😊 **Hello {user.username}!** Welcome back to TaskFlow!

**Quick Stats:**
• 📊 {stats['total_boards']} Boards
• 📋 {stats['total_issues']} Tasks ({stats['completion_rate']}% complete)
• 🏃 {stats['active_sprints']} Active Sprint(s)

How can I help you today? 🚀"""

    # ============ HELP ============
    if 'help' in message or 'what can you do' in message or 'capabilities' in message:
        return get_comprehensive_help()

    # ============ TIME ESTIMATES ============
    if any(word in message for word in ['how long', 'estimate', 'when will', 'time to complete']):
        return generate_time_estimate(stats, issues, message)

    # ============ RECOMMENDATIONS ============
    if any(word in message for word in ['recommend', 'suggest', 'advice', 'tip', 'improve']):
        return get_smart_recommendations(stats, issues)

    # ============ PROJECT OVERVIEW ============
    if any(word in message for word in ['overview', 'summary', 'dashboard']):
        return generate_project_overview(stats, boards, issues, sprints)

    # ============ DEFAULT ============
    return f"""🤖 **I understand you're asking about:** "{message}"

**Here's what I can tell you about your TaskFlow system:**

📊 **Current Status:**
• {stats['total_boards']} Board(s) ({stats['scrum_boards']} Scrum, {stats['kanban_boards']} Kanban)
• {stats['total_issues']} Task(s) ({stats['completion_rate']}% complete)
• {stats['total_sprints']} Sprint(s) ({stats['active_sprints']} active)

**Try asking me:**
• "Show me my profile"
• "List all my boards"
• "What's my completion rate?"
• "Show active sprint progress"
• "How many tasks are pending?"

What would you like to know? 🚀"""


# ============ HELPER FUNCTIONS (KEEP ALL YOUR EXISTING ONES) ============

def get_motivation_message(rate):
    if rate >= 80:
        return "🎉 Outstanding! You're crushing your goals!"
    elif rate >= 50:
        return "👍 Great progress! Keep the momentum going!"
    elif rate >= 20:
        return "💪 Making steady progress! Stay focused!"
    else:
        return "🚀 Ready to start! Create your first task to begin your journey!"


def generate_project_overview(stats, boards, issues, sprints):
    active_sprint = sprints.filter(status='ACTIVE').first() if sprints.exists() else None

    overview = f"""📊 **Project Health Dashboard**

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**📋 Task Summary**
• Total Tasks: **{stats['total_issues']}**
• ✅ Completed: **{stats['completed']}** ({stats['completion_rate']}%)
• 🏃 In Progress: **{stats['in_progress']}**
• 📝 To Do: **{stats['todo']}**
• ⚠️ High Priority: **{stats['high_priority']}**

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**📊 Boards & Sprints**
• 📁 Boards: **{stats['total_boards']}** ({stats['scrum_boards']} Scrum, {stats['kanban_boards']} Kanban)
• 🏃 Sprints: **{stats['total_sprints']}** ({stats['active_sprints']} active)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

    if active_sprint:
        overview += f"""
**🏃 Current Sprint**
• Name: **{active_sprint.name}**
• Goal: {active_sprint.goal or 'Not set'}
"""

    overview += f"\n{get_motivation_message(stats['completion_rate'])}"

    return overview


def get_board_insights(boards, stats):
    if not boards.exists():
        return "📊 **No boards found.**\n\nCreate your first board to start organizing your work!"

    return f"""📊 **Board Insights**

You have {stats['total_boards']} board(s) actively helping you organize work.

• 🏃 Scrum: **{stats['scrum_boards']}**
• 📋 Kanban: **{stats['kanban_boards']}**

💡 **Tip:** Use Scrum boards for sprint-based development and Kanban for continuous workflow."""


def get_backlog_insights(issues, stats):
    if stats['total_issues'] == 0:
        return "📋 **Backlog is empty!** Create your first task to get started. 🚀"

    high_priority = issues.filter(priority='HIGH', status__in=['TODO', 'IN_PROGRESS']).count()

    return f"""📋 **Backlog Insights**

• 📝 To Do: **{stats['todo']}**
• 🏃 In Progress: **{stats['in_progress']}**
• ✅ Completed: **{stats['completed']}**
• ⚠️ High Priority: **{high_priority}**

{get_motivation_message(stats['completion_rate'])}"""


def get_sprint_progress(sprints, issues, stats):
    try:
        active_sprint = sprints.filter(status='ACTIVE').first()

        if not active_sprint:
            if stats['total_sprints'] > 0:
                return "🏃 **No active sprint.**\n\nYou have existing sprints but none are active. Start a sprint to track progress!"
            else:
                return "🏃 **No sprints found.**\n\nCreate your first sprint to start tracking progress!"

        sprint_issues = issues.filter(sprint=active_sprint)
        total = sprint_issues.count()
        completed = sprint_issues.filter(status='DONE').count()
        progress = round((completed / total * 100) if total > 0 else 0)

        days_left = 0
        if active_sprint.end_date:
            days_left = max(0, (active_sprint.end_date - datetime.now().date()).days)

        response = f"""🏃 **Sprint Progress: {active_sprint.name}**

• 📊 Progress: **{progress}%** ({completed}/{total} tasks)
• 📅 Days remaining: **{days_left}**
• 🎯 Goal: {active_sprint.goal if active_sprint.goal else 'Not set'}

"""

        if progress >= 80:
            response += "🎉 **Almost there!** You're crushing this sprint!"
        elif progress >= 50:
            response += "💪 **Good progress!** Keep pushing to complete the remaining tasks!"
        elif progress > 0:
            response += "🚀 **Making progress!** Stay focused and you'll reach your sprint goal."
        else:
            response += "🌟 **Ready to begin!** Start moving tasks from backlog to make progress on this sprint."

        return response

    except Exception as e:
        return "🏃 **Sprint Progress**\n\nUnable to fetch sprint details at the moment. Please try again later."


def get_sprint_insights(sprints, stats):
    if not sprints.exists():
        return "🏃 **No sprints found.**\n\nCreate your first sprint to start agile planning!"

    return f"""🏃 **Sprint Insights**

• Total Sprints: **{stats['total_sprints']}**
• Active: **{stats['active_sprints']}**
• Completed: **{stats['completed_sprints']}**
• Planned: **{stats['planned_sprints']}**

💡 **Tip:** Keep sprints focused and achievable. Aim for 70-80% completion rate!"""


def get_notification_status(stats):
    if stats['unread_notifications'] == 0:
        return "🔔 **All caught up!** You have no unread notifications. ✨"
    else:
        return f"🔔 **You have {stats['unread_notifications']} unread notification(s).**\n\nCheck your notifications to stay updated!"


def generate_detailed_report(stats, issues):
    report = f"""📈 **Analytics Report**

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Task Distribution:**
• 📝 To Do: {stats['todo']}
• 🏃 In Progress: {stats['in_progress']}
• ✅ Completed: {stats['completed']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Priority Breakdown:**
• 🔴 High: {stats['high_priority']}
• 🟡 Medium: {stats['medium_priority']}
• 🟢 Low: {stats['low_priority']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Key Metrics:**
• Completion Rate: **{stats['completion_rate']}%**
• Active Boards: **{stats['total_boards']}**
• Active Sprints: **{stats['active_sprints']}**

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{get_motivation_message(stats['completion_rate'])}"""

    return report


def generate_time_estimate(stats, issues, message):
    todo_count = stats['todo']

    if todo_count == 0:
        return "✅ **Great news!** You have no pending tasks. Time to celebrate! 🎉"

    recent_completed = issues.filter(status='DONE', updated_at__gte=datetime.now() - timedelta(days=7)).count()
    daily_rate = recent_completed / 7 if recent_completed > 0 else 0.5

    estimated_days = int(todo_count / daily_rate) if daily_rate > 0 else 7

    if estimated_days <= 1:
        time_msg = "about 1 day"
    elif estimated_days <= 7:
        time_msg = f"about {estimated_days} days"
    else:
        time_msg = f"about {estimated_days // 7} weeks"

    return f"""📅 **Estimated Completion Time**

Based on your current progress, you have approximately **{time_msg}** of work remaining.

📋 **Pending Tasks:** {todo_count}
⚡ **Daily Rate:** ~{daily_rate:.1f} tasks/day

💡 **Tip:** Focus on high priority tasks first to make faster progress!"""


def get_smart_recommendations(stats, issues):
    recommendations = []

    if stats['high_priority'] > 3:
        recommendations.append("⚠️ Focus on completing your high priority tasks first")

    if stats['todo'] > 10 and stats['in_progress'] < 3:
        recommendations.append("📋 Limit your work in progress to 2-3 tasks for better focus")

    if stats['completion_rate'] < 30 and stats['total_issues'] > 0:
        recommendations.append("💡 Break down large tasks into smaller, manageable chunks")

    if stats['active_sprints'] == 0 and stats['total_sprints'] > 0:
        recommendations.append("🏃 Start a sprint to organize your work better")

    if stats['scrum_boards'] == 0 and stats['kanban_boards'] > 0:
        recommendations.append("📊 Consider creating a Scrum board for sprint-based development")

    if len(recommendations) == 0:
        recommendations.append("✨ You're doing great! Keep maintaining your current workflow")
        recommendations.append("🎯 Set weekly goals to track your progress")

    response = "💡 **Smart Recommendations**\n\n"
    for rec in recommendations:
        response += f"• {rec}\n"

    return response


def get_comprehensive_help():
    return """🤖 **I can answer ANY question about your TaskFlow system!**

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**👤 Profile Questions**
• "What's my username?"
• "Show my email and role"
• "When did I join?"

**📊 Board Questions**
• "How many boards do I have?"
• "List all my boards"
• "Show Scrum boards only"
• "What are my project keys?"

**📋 Task Questions**
• "How many tasks are pending?"
• "Show high priority tasks"
• "What's my completion rate?"
• "List completed tasks"

**🏃 Sprint Questions**
• "Show active sprint progress"
• "How many sprints do I have?"
• "What's my sprint goal?"

**🔔 Notification Questions**
• "Any unread notifications?"
• "How many notifications?"

**📈 Analytics Questions**
• "Generate performance report"
• "Show project statistics"
• "Give me recommendations"

**⏰ Date & Time Questions**
• "What's today's date?"
• "What time is it?"
• "Show me today's tasks"
• "What's due this week?"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Just ask naturally - I understand context!** 🚀"""


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_suggestions(request):
    """Get dynamic suggestions based on user data"""

    user = request.user
    issues = Issue.objects.filter(assigned_email=user.email)
    boards = Board.objects.filter(created_by=user.email)
    sprints = Sprint.objects.filter(board__created_by=user.email)

    suggestions = []

    # Profile suggestions
    suggestions.append("What's my username?")
    suggestions.append("Show my profile")

    # Date/Time suggestions
    suggestions.append("What's today's date?")
    suggestions.append("What time is it?")

    # Board suggestions
    if boards.count() > 0:
        suggestions.append("How many boards do I have?")
        suggestions.append("List all my boards")
    else:
        suggestions.append("Create a board")

    # Task suggestions
    if issues.filter(status='TODO').count() > 0:
        suggestions.append("How many tasks are pending?")
        suggestions.append("Show high priority tasks")
        suggestions.append("What's due today?")
    else:
        suggestions.append("Create a task")

    # Sprint suggestions
    if sprints.filter(status='ACTIVE').exists():
        suggestions.append("What's my sprint progress?")
    elif sprints.count() > 0:
        suggestions.append("Start a sprint")
    else:
        suggestions.append("Create a sprint")

    # Analytics suggestions
    if issues.count() > 0:
        suggestions.append("What's my completion rate?")
        suggestions.append("Give me recommendations")

    # Remove duplicates and limit
    suggestions = list(dict.fromkeys(suggestions))[:10]

    return Response({"suggestions": suggestions})