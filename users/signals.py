from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from django.apps import apps

@receiver(post_migrate)
def create_groups_and_permissions(sender, **kwargs):
    if sender.name != "users":
        return

    regular_group, _ = Group.objects.get_or_create(name="RegularUsers")
    moderator_group, _ = Group.objects.get_or_create(name="Moderator")

    permissions_to_add = []

    try:
        user_ct = ContentType.objects.get_for_model(apps.get_model("users", "CustomUser"))
        post_ct = ContentType.objects.get_for_model(apps.get_model("network", "Post"))

        can_ban = Permission.objects.get(codename="can_ban_users", content_type=user_ct)
        can_delete_any_post = Permission.objects.get(codename="can_delete_any_post", content_type=post_ct)

        permissions_to_add = [can_ban, can_delete_any_post]
    except Permission.DoesNotExist:
        print("🚨 Some permissions not found. Make sure migrations are applied.")
        return

    for perm in permissions_to_add:
        moderator_group.permissions.add(perm)