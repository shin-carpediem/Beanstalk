from django.shortcuts import redirect
from account.models import nonLoginUser


def permission(user_uuid):

    if user_uuid.allowed == 'unknown':
        return redirect('customer:waiting')

    if user_uuid.allowed == 'denied':
        return redirect('customer:denied')

    if user_uuid.active == False:
        return redirect('customer:thanks')


def judging(table_num):
    if nonLoginUser.objects.defer('created_at').filter(allowed='unknown', table=table_num, active=True).count() > 0:
        return redirect('customer:judge')


def expired(request):

    if not 'nonloginuser_uuid' in request.session:
        request.session.flush()
        return redirect('customer:thanks')
