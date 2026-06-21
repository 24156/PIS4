def get_initials(user):
    first = (user.first_name or user.username)[:1].upper()
    last = (user.last_name or '')[:1].upper()
    return f'{first}{last}' if last else first
