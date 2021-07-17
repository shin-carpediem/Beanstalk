from customer.models import Order
from django.http import request
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db.models import Q
from django.template import Context, Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import random
import datetime
from itertools import groupby
from .models import Category, Allergy, Menu
from account.models import User, nonLoginUser
from beanstalk.settings import EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, EMAIL_HOST, EMAIL_PORT


# Create your views here.
# default
table_num = '管理者'
categories = Category.objects.defer('created_at').order_by('id')
first_category = categories[0]
menus = Menu.objects.defer('created_at').filter(
    category=first_category).order_by('-id')
allergies = Allergy.objects.all().order_by('id')
ctx = {
    'table_num': table_num,
    'categories': categories,
    'menus': menus,
    'allergies': allergies,
}


def login_as_user(request):
    return render(request, 'restaurant/login.html')


@require_POST
def confirm(request):
    # メールアドレスを取得
    email = request.POST.get('username')

    # セッションにすでにユーザがいれば削除
    if 'user' in request.session:
        del request.session['user']

    # ランダムな6桁の文字列を生成
    passcode = str(random.randrange(10)) + str(random.randrange(10)) + str(random.randrange(10)) + \
        str(random.randrange(10)) + \
        str(random.randrange(10)) + str(random.randrange(10))

    # メールアドレスとパスコードのセットになったセッションを作成
    request.session['user'] = {email: passcode}

    # パスコードをメール送信
    EMAIL = EMAIL_HOST_USER
    PASSWORD = EMAIL_HOST_PASSWORD
    TO = email

    msg = MIMEMultipart('alternative')
    msg['Subject'] = '【注文・メニュー管理システム】6ケタの数字をログイン画面に入力してください'
    msg['From'] = EMAIL
    msg['To'] = TO

    html = """\
    <html>
      <head>
      </head>
      <body>
        <p>{{ passcode }}</p>
      </body>
    </html>
    """

    html = Template(html)
    context = Context({'passcode': passcode})
    template = MIMEText(html.render(context=context), 'html')
    msg.attach(template)

    try:
        s = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        s.starttls()
        s.login(EMAIL, PASSWORD)
        s.sendmail(EMAIL, TO, msg.as_string())
        s.quit()
        messages.info(
            request, f"入力したメールアドレス宛てに6ケタの数字が書かれたメールを送信しました。その数字を以下に入力してください。")
    except Exception:
        messages.error(request, f"メール送信に失敗しました。お手数ですがメールアドレスの入力からやり直してください。")
        return redirect(request, 'restaurant:login')

    ctx['email'] = email

    return render(request, 'restaurant/confirm.html', ctx)


def order_manage(request):
    # ログインから
    if request.method == 'POST':
        email = request.POST.get('username')
        passcode = request.POST.get('passcode')

        # 入力されたパスコードがセッションに保持されたパスコードと一致するならログインを許可
        if passcode == request.session['user'][email]:
            user = User.objects.get(email=email)
            login(request, user)

            # emailのセッションを作成(いきなりオーダー画面にアクセスするお店を識別する為)
            email = user.email
            request.session['user_email'] = {1: email}

            return render(request, 'restaurant/order_manage.html', ctx)
        else:
            messages.info(
                request, f"ログインに失敗しました。お手数ですがメールアドレスの入力からやり直してください。")
            return redirect(request, 'restaurant:login')
    # いきなりこの画面(多くの店がこの想定)
    elif 'user_email' in request.session:
        user_email = request.session['user_email']['1']
        user = User.objects.get(email=user_email)
        formatted_logo = user.formatted_logo
        name = user.name

        order_list = Order.objects.filter(status='調理中')

        ctx['formatted_logo'] = formatted_logo
        ctx['name'] = name
        ctx['order_list'] = order_list

        return render(request, 'restaurant/order_manage.html', ctx)
    else:
        messages.info(
            request, f"ログインの有効期限が切れました。お手数ですが再度ログインしてください。")
        return redirect(request, 'restaurant:login')


@login_required
@require_POST
def order_status_ch(request):
    order_status = request.POST.get('order_status')
    order_id = request.POST.get('order_id')
    order = Order.objects.get(id=order_id)
    order.status = order_status
    order.save()
    return redirect('restaurant:order_manage')


@login_required
def history(request):
    user = User.objects.get(id=request.user.id)
    name = user.name

    order_list = Order.objects.filter(Q(status='キャンセル') | Q(status='済'))

    ctx['name'] = name
    ctx['order_list'] = order_list

    return render(request, 'restaurant/history.html', ctx)


@login_required
def total(request):
    dt_now = datetime.datetime.now()
    # 同日日時、あるいは昨日に作られた注文のみを抽出
    orders = Order.objects.filter(Q(created_at__date=datetime.date(
        dt_now.year, dt_now.month, dt_now.day)) | Q(created_at__date=datetime.date(
            dt_now.year, dt_now.month, (dt_now.day)-1)))

    ctx['orders'] = orders

    return render(request, 'restaurant/total.html', ctx)


@login_required
def daily(request):
    orders = Order.objects.filter(status='済').order_by('-id')

    total_price = 0

    for order in orders:
        total_price = total_price + (order.menu.price * order.num)

    # 1日の売上と各商品の数量
    dt_now = datetime.datetime.now()
    todays_orders = Order.objects.filter(status='済', created_at__date=datetime.date(
        dt_now.year, dt_now.month, dt_now.day)).order_by('-id')

    totays_total_price = 0

    for todays_order in todays_orders:
        totays_total_price = totays_total_price + \
            (todays_order.menu.price * todays_order.num)

    ctx['orders'] = orders
    ctx['total_price'] = total_price
    ctx['todays_orders'] = todays_orders
    ctx['totays_total_price'] = totays_total_price

    return render(request, 'restaurant/daily.html', ctx)


# for manageing customer screen
def manage_login(request):
    return render(request, 'restaurant/login.html', ctx)


@login_required
def manage_menu(request):
    user = request.user
    restaurant_name = user.name

    ctx['restaurant_name'] = restaurant_name

    return render(request, 'customer/menu.html', ctx)


@login_required
@require_POST
def category_add(request):
    name = request.POST.get('add_category_form')
    if Category.objects.filter(name=name).count() == 0:
        category = Category(name=name)
        category.save()
        messages.success(request, f"カテゴリーに{name}を追加しました。")
    else:
        messages.warning(request, f"同じ名前のカテゴリは作成できません。")

    return redirect('customer:menu')


@login_required
@require_POST
def category_ch(request):
    name = request.POST.get('category_name')
    required_name = request.POST.get('ch_category_form')
    category = Category.objects.get(name=name)
    category.name = required_name
    category.save()
    messages.success(request, f"カテゴリーの名前を{name}から{required_name}に変更しました。")

    return redirect('customer:menu')


@login_required
@require_POST
def category_del(request):
    name = request.POST.get('del_category_form')
    try:
        category = Category.objects.get(name=name)
        category.delete()
        messages.success(request, f"カテゴリーから{name}を削除しました。")
    except Exception:
        messages.warning(request, f"削除に失敗しました。")

    return redirect('customer:menu')


@login_required
@require_POST
def menu_add(request):
    name = request.POST.get('name')
    if Menu.objects.filter(name=name).count() != 0:
        messages.warning(request, f"同一の名前のメニューは作れません。")
    else:
        category = request.POST.get('category')
        # foreign_key
        category_id = Category.objects.get(name=category)
        price = request.POST.get('price')
        img = request.FILES.get('img')

        menu = Menu(name=name, category=category_id,
                    price=price, img=img)
        menu.save()

        allergy_list = request.POST.getlist('allergy')
        for allergy in allergy_list:
            allergy_query = Allergy.objects.get(ingredient=allergy)
            menu.allergies.add(allergy_query)

        menu.save()
        messages.success(request, f"{category}に{name}を追加しました。")

    return redirect('customer:menu')


@login_required
@require_POST
def menu_del(request):
    required_menu = request.POST.get('menu')
    menu = Menu.objects.get(name=required_menu)
    menu.delete()
    messages.success(request, f"{required_menu}をメニューから削除しました。")

    return redirect('customer:menu')


@login_required
@require_POST
def menu_img_manage(request):
    menu_img = request.FILES.get('menu_img')
    menu_id = request.POST.get('menu_id')
    menu = Menu.objects.get(id=menu_id)

    # 以前のファイルは削除
    menu.img.delete(False)

    menu.img = menu_img
    menu.save()
    name = menu.name
    messages.success(request, f"{name}の写真を変更しました。")

    return redirect('customer:menu_detail', menu_id=menu.id)


@login_required
@require_POST
def menu_name_manage(request):
    menu_name = request.POST.get('menu_name')
    menu_id = request.POST.get('menu_id')
    menu = Menu.objects.get(id=menu_id)
    menu.name = menu_name
    menu.save()
    messages.success(request, f"{menu_name}に名前を変更しました。")

    return redirect('customer:menu_detail', menu_id=menu.id)


@login_required
@require_POST
def menu_price_manage(request):
    menu_price = request.POST.get('menu_price')
    menu_id = request.POST.get('menu_id')
    menu = Menu.objects.get(id=menu_id)
    menu.price = menu_price
    menu.save()
    name = menu.name
    messages.success(request, f"{name}の金額を{menu_price}円に変更しました。")

    return redirect('customer:menu_detail', menu_id=menu.id)


@login_required
@require_POST
def allergy_ch(request):
    allergy_list = request.POST.getlist('allergy')
    menu_id = request.POST.get('menu_id')

    menu = Menu.objects.get(id=menu_id)
    for allergy in allergy_list:
        # データと変わらない場合は何もしない
        if allergy in menu.allergies.all():
            None
        # 新しくチェックをつけたものは登録する
        else:
            allergy_query = Allergy.objects.get(ingredient=allergy)
            menu.allergies.add(allergy_query)

    menu.save()

    menu = Menu.objects.get(id=menu_id)
    for allergy in menu.allergies.all():
        # チェックされているものとデータが同じ場合は何もしない
        if allergy.ingredient in allergy_list:
            None
        # 新しくチェックを外したものはデータからも外す
        else:
            allergy_query = Allergy.objects.get(ingredient=allergy)
            menu.allergies.remove(allergy_query)

    menu.save()

    return redirect('customer:menu_detail', menu_id=menu.id)


@login_required
@require_POST
def allergy_add(request):
    get_allergy = request.POST.get('allergy')
    menu_id = request.POST.get('menu_id')
    menu = Menu.objects.get(id=menu_id)
    menu.allergies.create(ingredient=get_allergy)
    menu.save()
    messages.success(request, f"{get_allergy}をアレルギー項目一覧に追加しました。")

    return redirect('customer:menu_detail', menu_id=menu.id)


@login_required
@require_POST
def allergy_del(request):
    get_allergy = request.POST.get('allergy')
    menu_id = request.POST.get('menu_id')
    menu = Menu.objects.get(id=menu_id)
    allergy = Allergy.objects.get(ingredient=get_allergy)
    allergy.delete()
    messages.success(request, f"{get_allergy}をアレルギー項目一覧から削除しました。")

    return redirect('customer:menu_detail', menu_id=menu.id)
