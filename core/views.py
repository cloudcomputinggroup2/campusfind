from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, Count
from django.http import JsonResponse, HttpResponseForbidden
from django.utils import timezone
from .models import Item, AuditLog
from .forms import ItemForm, UserRegistrationForm, ProfileUpdateForm

def home_view(request):
    """
    Landing page showcasing platform overview, dynamic statistics,
    latest lost items, latest found items, and category quick-filters.
    """
    active_items = Item.objects.filter(is_deleted=False)
    recent_lost = active_items.filter(status=Item.STATUS_LOST)[:4]
    recent_found = active_items.filter(status=Item.STATUS_FOUND)[:4]
    recent_resolved = active_items.filter(status=Item.STATUS_CLAIMED)[:4]

    # Category counts for visual category pills
    category_counts = active_items.values('category').annotate(count=Count('id'))
    category_map = {c['category']: c['count'] for c in category_counts}

    context = {
        'recent_lost': recent_lost,
        'recent_found': recent_found,
        'recent_resolved': recent_resolved,
        'category_map': category_map,
    }
    return render(request, 'core/home.html', context)


def item_list_view(request):
    """
    Search and filter catalog for all lost, found, and claimed campus items.
    Supports multi-attribute search, category, status, location filters, sorting, and pagination.
    """
    queryset = Item.objects.filter(is_deleted=False)

    # Search query
    q = request.GET.get('q', '').strip()
    if q:
        queryset = queryset.filter(
            Q(title__icontains=q) |
            Q(description__icontains=q) |
            Q(location__icontains=q) |
            Q(contact__icontains=q)
        )

    # Category filter
    category = request.GET.get('category', '').strip()
    if category and category != 'ALL':
        queryset = queryset.filter(category=category)

    # Status filter
    status = request.GET.get('status', '').strip().upper()
    if status and status != 'ALL':
        queryset = queryset.filter(status=status)

    # Location filter
    location = request.GET.get('location', '').strip()
    if location and location != 'ALL':
        queryset = queryset.filter(location__icontains=location)

    # Sorting
    sort = request.GET.get('sort', 'newest')
    if sort == 'oldest':
        queryset = queryset.order_by('created_at')
    elif sort == 'title':
        queryset = queryset.order_by('title')
    else:  # newest default
        queryset = queryset.order_by('-created_at')

    # View Mode (grid vs table)
    view_mode = request.GET.get('view', 'grid')

    # Pagination: 9 items per page for clean 3x3 grid
    paginator = Paginator(queryset, 9)
    page = request.GET.get('page', 1)
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    context = {
        'items': items,
        'query_q': q,
        'selected_category': category,
        'selected_status': status,
        'selected_location': location,
        'selected_sort': sort,
        'view_mode': view_mode,
        'total_results': paginator.count,
    }
    return render(request, 'core/item_list.html', context)


def item_detail_view(request, pk):
    """
    Detailed single item view with full specifications, photo, contact drawer,
    safe recovery tips, and owner action buttons.
    """
    item = get_object_or_404(Item, pk=pk, is_deleted=False)
    
    # Related items in same category
    related_items = Item.objects.filter(
        category=item.category,
        is_deleted=False
    ).exclude(pk=item.pk)[:3]

    is_owner = item.is_owner(request.user)

    context = {
        'item': item,
        'related_items': related_items,
        'is_owner': is_owner,
    }
    return render(request, 'core/item_detail.html', context)


@login_required
def item_create_view(request):
    """
    Create a new Lost or Found item post.
    Supports query parameter '?type=lost' or '?type=found' for preselection.
    """
    initial_type = request.GET.get('type', '').lower()
    initial_status = Item.STATUS_LOST
    if initial_type == 'found':
        initial_status = Item.STATUS_FOUND

    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            item.save()
            messages.success(
                request,
                f"Successfully reported '{item.title}'! It is now listed publicly on CampusFind."
            )
            return redirect('item_detail', pk=item.pk)
        else:
            messages.error(request, "Please correct the errors in the form below.")
    else:
        form = ItemForm(initial={'status': initial_status, 'date_event': timezone.now().date()})

    context = {
        'form': form,
        'page_title': 'Report an Item',
        'is_edit': False,
    }
    return render(request, 'core/item_form.html', context)


@login_required
def item_update_view(request, pk):
    """
    Edit an existing item post (restricted to post creator or staff).
    """
    item = get_object_or_404(Item, pk=pk, is_deleted=False)

    if not item.is_owner(request.user):
        messages.error(request, "You do not have permission to edit this post.")
        return redirect('item_detail', pk=item.pk)

    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, f"Post '{item.title}' has been successfully updated!")
            return redirect('item_detail', pk=item.pk)
        else:
            messages.error(request, "Please check the form for errors.")
    else:
        form = ItemForm(instance=item)

    context = {
        'form': form,
        'item': item,
        'page_title': f"Edit: {item.title}",
        'is_edit': True,
    }
    return render(request, 'core/item_form.html', context)


@login_required
def item_delete_view(request, pk):
    """
    Delete an existing item post (soft-delete with audit log, restricted to post creator or staff).
    """
    item = get_object_or_404(Item, pk=pk, is_deleted=False)

    if not item.is_owner(request.user):
        messages.error(request, "You do not have permission to delete this post.")
        return redirect('item_detail', pk=item.pk)

    if request.method == 'POST':
        title = item.title
        item.soft_delete(user=request.user, reason="Deleted by creator/staff from portal")
        AuditLog.log_event(
            actor=request.user,
            action_type=AuditLog.ACTION_ITEM_SOFT_DELETED,
            target=item,
            target_repr=title,
            reason="Post deleted by owner or staff"
        )
        messages.success(request, f"Post '{title}' has been deleted.")
        return redirect('my_posts')

    context = {
        'item': item,
    }
    return render(request, 'core/item_confirm_delete.html', context)


@login_required
def item_toggle_status_view(request, pk):
    """
    Quickly toggle status between Claimed/Resolved and active (Lost/Found).
    """
    item = get_object_or_404(Item, pk=pk, is_deleted=False)

    if not item.is_owner(request.user):
        messages.error(request, "You do not have permission to change this item's status.")
        return redirect('item_detail', pk=item.pk)

    if request.method == 'POST':
        action = request.POST.get('action', '')
        if action == 'claim' or item.status != Item.STATUS_CLAIMED:
            item.mark_as_claimed()
            messages.success(request, f"Great news! '{item.title}' has been marked as Claimed / Reunited! 🎉")
        else:
            # Reopen
            target_status = request.POST.get('target_status', Item.STATUS_LOST)
            item.reopen(new_status=target_status)
            messages.info(request, f"'{item.title}' has been reopened as {item.get_status_display()}.")

    return redirect('item_detail', pk=item.pk)


@login_required
def my_posts_view(request):
    """
    Dashboard for the logged-in user displaying their reported items with status tabs and actions.
    """
    user_items = Item.objects.filter(user=request.user, is_deleted=False)

    tab = request.GET.get('tab', 'all').lower()
    if tab == 'lost':
        filtered_items = user_items.filter(status=Item.STATUS_LOST)
    elif tab == 'found':
        filtered_items = user_items.filter(status=Item.STATUS_FOUND)
    elif tab == 'claimed':
        filtered_items = user_items.filter(status=Item.STATUS_CLAIMED)
    else:
        filtered_items = user_items

    stats = {
        'total': user_items.count(),
        'lost': user_items.filter(status=Item.STATUS_LOST).count(),
        'found': user_items.filter(status=Item.STATUS_FOUND).count(),
        'claimed': user_items.filter(status=Item.STATUS_CLAIMED).count(),
    }

    context = {
        'items': filtered_items,
        'current_tab': tab,
        'user_stats': stats,
    }
    return render(request, 'core/my_posts.html', context)


@login_required
def moderator_dashboard_view(request):
    """
    Admin & staff moderation dashboard for managing all posts across campus.
    """
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, "Access restricted to campus administrators and moderators.")
        return redirect('home')

    all_items = Item.objects.filter(is_deleted=False).order_by('-created_at')

    # Moderation quick filter
    filter_status = request.GET.get('status', 'all').upper()
    if filter_status in [Item.STATUS_LOST, Item.STATUS_FOUND, Item.STATUS_CLAIMED]:
        all_items = all_items.filter(status=filter_status)

    paginator = Paginator(all_items, 20)
    page = request.GET.get('page', 1)
    items = paginator.get_page(page)

    context = {
        'items': items,
        'filter_status': filter_status,
        'total_items_count': Item.objects.filter(is_deleted=False).count(),
    }
    return render(request, 'core/moderator_dashboard.html', context)


def register_view(request):
    """
    User registration view.
    """
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            AuditLog.log_event(
                actor=user,
                action_type=AuditLog.ACTION_USER_CREATED,
                target=user,
                target_repr=user.username,
                reason="Self-service student registration"
            )
            login(request, user)
            messages.success(
                request,
                f"Welcome to CampusFind, {user.first_name or user.username}! Your account has been created."
            )
            return redirect('home')
        else:
            messages.error(request, "Registration failed. Please check the requirements below.")
    else:
        form = UserRegistrationForm()

    return render(request, 'core/register.html', {'form': form})


def login_view(request):
    """
    User login view with validation and return URL support.
    """
    if request.user.is_authenticated:
        return redirect('home')

    next_url = request.GET.get('next', 'home')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.first_name or user.username}!")
            return redirect(request.POST.get('next') or 'home')
        else:
            messages.error(request, "Invalid username or password. Please try again.")
    else:
        form = AuthenticationForm()

    return render(request, 'core/login.html', {'form': form, 'next': next_url})


def logout_view(request):
    """
    Log out the user and return to homepage with feedback.
    """
    logout(request)
    messages.info(request, "You have been logged out. Have a great day on campus!")
    return redirect('home')


def print_notice_view(request, pk):
    """
    Printable flyer / notice card for pinning to campus physical notice boards.
    """
    item = get_object_or_404(Item, pk=pk, is_deleted=False)
    return render(request, 'core/print_notice.html', {'item': item})


def health_check_view(request):
    """
    Health check endpoint for AWS EC2 / Application Load Balancer / CloudWatch alarms.
    Returns HTTP 200 with JSON payload when application and database are healthy.
    """
    from django.db import connection
    db_status = "ok"
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
    except Exception as e:
        db_status = f"error: {str(e)}"

    status_code = 200 if db_status == "ok" else 500

    return JsonResponse({
        "status": "healthy" if db_status == "ok" else "unhealthy",
        "service": "CampusFind",
        "version": "1.0.0",
        "database": db_status,
        "timestamp": timezone.now().isoformat(),
    }, status=status_code)
