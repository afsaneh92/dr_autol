def send_user_registration(request):
    if request.is_json:
        return True
    return False


def send_login(request):
    if request.is_json:
        return True
    return False
