from django.urls import reverse

from digitalarz.utils import Context_Utils


def add_base_navbar_items_to_context(request):
    if 'next' in request.GET:
        redirect_path = request.GET['next']
    else:
        redirect_path = request.META.get('HTTP_REFERER', '/')
    next_page = redirect_path

    user_info = {
        "user_name": request.user.username,
        "session_key": request.session.session_key
    }
    user_items =Context_Utils.get_user_items(request.user)
    navbar_items=Context_Utils.get_navbar_items(request.user)

    return {
        'navbar_items': navbar_items,
        'user_items': user_items,
        'next_page': next_page,
        'user_info': user_info
    }




# def get_academics_navbar_items(user, navbarItems, dropdownItems):
#     if user:
#         dropdownItems.append({"name": "Signout", "href": reverse("logout"), "fa": "fa fa-sign-out"})
#         if user.is_staff:
#             if user.is_superuser:
#                 dropdownItems.append({"name": "Manage", "href": reverse("admin:index"), "fa": "fa fa-dashboard"})
#             if user.is_superuser or user.groups.filter(name="Academic_Group").exists():
#                 dropdownItems.append({"name": "Manage Academics", "href": "/academics_admin/", "fa": "fa fa-dashboard"})
#             if user.is_superuser or user.groups.filter(name="course_allocation").exists():
#                 dropdownItems.append({"name": "Manage Academics", "href": "/academics_admin/", "fa": "fa fa-dashboard"})
#                 navbarItems.append({"name":"Course Allocation", "href": reverse("academics_course_allocation")})
#             # if user.is_superuser or user.groups.filter(name="Teachers_Group").exists():
#                 # navbarItems.append({"name": "Teachers", "href": reverse("teacher_home")})
#                 # dropdownItems.append({"name": "Manage Teacher", "href": "/teachers_admin/", "fa": "fa fa-dashboard"})
#             # if user.is_superuser or user.groups.filter(name="Students_Group").exists():
#             #     navbarItems.append({"name": "Students", "href": reverse('student_home')})
