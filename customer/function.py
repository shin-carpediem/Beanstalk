from django.shortcuts import redirect
from account.models import nonLoginUser


def permission(request):

    uuid = request.session['nonloginuser_uuid']

    try:
        user_uuid = nonLoginUser.objects.get(uuid=uuid)
    except Exception:
        return redirect('customer:index')

    if user_uuid.allowed == 'unknown':
        return redirect('customer:waiting')

    if user_uuid.allowed == 'denied':
        return redirect('customer:denied')

    if user_uuid.active == False:
        return redirect('customer:thanks')

    return user_uuid


def judging(request):
    table_num = request.session['table']

    if nonLoginUser.objects.defer('created_at').filter(allowed='unknown', table=table_num, active=True).count() > 0:
        return redirect('customer:judge')

    return table_num


def expired(request):

    if not 'nonloginuser_uuid' in request.session:
        request.session.flush()
        return redirect('customer:thanks')


def make_session(request, restaurant_name, restaurant_logo, table_num, uuid):

    # レストラン名のセッションを作成
    request.session['restaurant_name'] = restaurant_name
    # レストランのロゴのセッションを作成
    request.session['restaurant_logo'] = restaurant_logo
    # テーブル番号のセッションを作成
    request.session['table'] = table_num
    # uuidのセッションを作成
    request.session['nonloginuser_uuid'] = uuid
