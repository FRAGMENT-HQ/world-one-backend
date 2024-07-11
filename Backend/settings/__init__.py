from .dev import Dev
from .prod import Prod


try:
    from django.contrib.auth.models import Group, Permission


    groups = Group.objects.all()
    permissions = Permission.objects.all()

    if "content_admin" not in groups:
        group = Group.objects.create(name="content_admin")
        # for permission in permissions:
            # group.permissions.add(permission)
        group.save()
        print("Group content_admin created")
except Exception as e:
    print(e)