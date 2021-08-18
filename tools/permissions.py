import discord

from collections import OrderedDict


if __name__ == "__main__":
    raise Exception()

dev = 750718445783351367

permissions_roles = OrderedDict()
permissions_roles["IKA"] = 750725982842912909
permissions_roles["STRAZNIK"] = 732416472227381349
permissions_roles["RADNY"] = 732411030621257758
permissions_roles["PRZEWODNICZACY"] = 660223312034529301

def has_role(role_id, member :discord.Member):
    for role in member.roles:
        if role.id == role_id:
            return True
    return False


def is_ika(member :discord.Member):
    return has_role(permissions_roles["IKA"], member)


def can_access_channel(channel, member):
    permissions = channel.permissions_for(member)
    return permissions.connect and permissions.view_channel


def get_permission_lvl(permission):
    """
    :param permission: permission name eg. "ADMIN"
    :return: int permission lvl value
    """
    if permission == "DEV":
        return len(permissions_roles) + 2
    if permission == "ADMIN":
        return len(permissions_roles) + 1
    for i, key in enumerate(permissions_roles):
        if key == permission:
            return i + 1
    return 0


def get_member_permission_lvl(member):
    """
    :param member: discord.Member object
    :return: permission lvl for that member
    """
    if member.id == dev:
        return  len(permissions_roles) + 2
    if member.guild_permissions.administrator:
        return len(permissions_roles) + 1
    max_role = 0
    for i, role_name in enumerate(permissions_roles.keys()):
        for role in member.roles:
            if role.id == permissions_roles[role_name]:
                max_role = max(i+1, max_role)
    return max_role

def check_permission(ctx, permission):
    """
    :param ctx: context
    :param permission: permission name eg. "ADMIN"
    :return: True if author of ctx command matches permission if not then False
    """
    author = ctx.message.author
    return get_member_permission_lvl(author) >= get_permission_lvl(permission)

