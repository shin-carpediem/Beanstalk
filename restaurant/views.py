import datetime
from django.http import request
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db.models import Q
from itertools import chain
from django.template import Context, Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import datetime
from itertools import groupby
from .models import Category, Allergy, Menu, Nomiho
from account.models import Table, User, nonLoginUser
import customer.models
from beanstalk.settings import (
    CODE,
    EMAIL_HOST_USER,
    EMAIL_HOST_PASSWORD,
    EMAIL_HOST,
    EMAIL_PORT
)


# Create your views here.
def login_as_user(request):
    user = User.objects.get(id=1)
    try:
        user = User.objects.get(id=2)
    except Exception:
        pass
    try:
        user = User.objects.get(id=3)
    except Exception:
        pass

    email = user.email
    ctx = {
        'email': email
    }

    return render(request, 'restaurant/login.html', ctx)


# @require_POST
# def confirm(request):
    # categories = Category.objects.defer('created_at').order_by('id')
    # try:
    #     first_category = categories[0]
    #     menus = Menu.objects.defer('created_at').filter(
    #         category=first_category).order_by('-id')
    # except:
    #     menus = None
    # allergies = Allergy.objects.all().order_by('id')
    # ctx = {
    #     'categories': categories,
    #     'menus': menus,
    #     'allergies': allergies,
    # }

#     # メールアドレスを取得
#     email = request.POST.get('username')

#     # セッションにすでにユーザがいれば削除
#     if 'user' in request.session:
#         del request.session['user']

#     # ランダムな4桁の文字列を生成
#     passcode = str(random.randrange(10)) + str(random.randrange(10)) + str(random.randrange(10)) + \
#         str(random.randrange(10))

#     # メールアドレスとパスコードのセットになったセッションを作成
#     request.session['user'] = {email: passcode}

#     # パスコードをメール送信
#     EMAIL = EMAIL_HOST_USER
#     PASSWORD = EMAIL_HOST_PASSWORD
#     TO = email

#     msg = MIMEMultipart('alternative')
#     msg['Subject'] = '【注文・メニュー管理システム】4ケタの数字をログイン画面に入力してください'
#     msg['From'] = EMAIL
#     msg['To'] = TO

#     html = """\
#     <html>
#       <head>
#       </head>
#       <body>
#         <p>{{ passcode }}</p>
#       </body>
#     </html>
#     """

#     html = Template(html)
#     context = Context({'passcode': passcode})
#     template = MIMEText(html.render(context=context), 'html')
#     msg.attach(template)

#     try:
#         s = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
#         s.starttls()
#         s.login(EMAIL, PASSWORD)
#         s.sendmail(EMAIL, TO, msg.as_string())
#         s.quit()
#         messages.info(
#             request, f"入力したメールアドレス宛てに4ケタの数字が書かれたメールを送信しました。その数字を以下に入力してください。")
#     except Exception:
#         messages.error(request, f"メール送信に失敗しました。お手数ですがメールアドレスの入力からやり直してください。")
#         return redirect('restaurant:login')

#     ctx['email'] = email

#     return render(request, 'restaurant/confirm.html', ctx)


def send_code(request):
    # メールアドレスを取得
    email = request.POST.get('username')
    code = CODE

    if email == None:
        messages.info(request, f"送信対象となるメールアドレスが登録されていません。")
        return redirect('restaurant:login')

    EMAIL = EMAIL_HOST_USER
    PASSWORD = EMAIL_HOST_PASSWORD
    TO = email

    msg = MIMEMultipart('alternative')
    msg['Subject'] = '【注文・メニュー管理システム】4ケタの暗証番号をお送りします'
    msg['From'] = EMAIL
    msg['To'] = TO

    html = """\
    <html>
      <head>
      </head>
      <body>
        <p>{{ code }}</p>
      </body>
    </html>
    """

    html = Template(html)
    context = Context({'code': code})
    template = MIMEText(html.render(context=context), 'html')
    msg.attach(template)

    try:
        s = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        s.starttls()
        s.login(EMAIL, PASSWORD)
        s.sendmail(EMAIL, TO, msg.as_string())
        s.quit()
        messages.info(
            request, f"メールアドレス宛てに4桁の暗証番号が書かれたメールを送信しました。その数字を入力してください。")
        return redirect('restaurant:login')
    except Exception:
        messages.error(request, f"メール送信に失敗しました。お手数ですがメールアドレスの入力からやり直してください。")
        return redirect('restaurant:login')


def order_manage(request):
    try:
        filter_type = request.POST.get('filter-type')
    except Exception:
        filter_type = None

    # ログインから
    if request.method == 'POST' and filter_type == 'login':
        email = request.POST.get('username')
        # passcode = request.POST.get('passcode')

        # 入力されたパスコードがセッションに保持されたパスコードと一致するならログインを許可
        # if passcode == request.session['user'][email]:
        try:
            user = User.objects.get(email=email)
            code = request.POST.get('code')

            if code == CODE:
                login(request, user)
                request.session['table'] = '管理者'
            else:
                messages.info(request, f"暗証番号が異なります。")
                return redirect('restaurant:login')

        except Exception:
            messages.info(request, f"メールアドレスが異なります。")
            return redirect('restaurant:login')

        # emailのセッションを作成(いきなりオーダー画面にアクセスするお店を識別する為)
        email = user.email
        request.session['user_email'] = email

        return render(request, 'restaurant/order_manage.html')

    # いきなりこの画面から＆メニュー編集画面から戻ってくるパターン(多くの店がこの想定)
    elif 'user_email' in request.session:
        user_email = request.session['user_email']
        user = User.objects.get(email=user_email)
    else:
        user = User.objects.get(id=1)
        try:
            user = User.objects.get(id=2)
        except Exception:
            pass
        try:
            user = User.objects.get(id=3)
        except Exception:
            pass

    formatted_logo = user.formatted_logo
    name = user.name
    order_list = ''
    table = None

    active_users = nonLoginUser.objects.defer('created_at').filter(active=True)
    menus = Menu.objects.defer('created_at').order_by('id')

    # テーブル番号でフィルタした際
    if request.POST.get('table') != None:
        table = request.POST.get('table')
        active_users = nonLoginUser.objects.defer(
            'created_at').filter(table=table, active=True)

    for active_user in active_users:
        active_user_order = customer.models.Order.objects.filter(
            customer=active_user, status='調理中', curr=True).order_by('-id')
        order_list = list(chain(order_list, active_user_order))

    ctx = {
        'formatted_logo': formatted_logo,
        'name': name,
        'table': table,
        'order_list': order_list,
        'menus': menus,
    }

    return render(request, 'restaurant/order_manage.html', ctx)


@login_required
@require_POST
def order_status_ch(request, order_id):
    order_status = request.POST.get('order_status')
    order = customer.models.Order.objects.get(id=order_id)
    order.status = order_status
    order.save()
    return redirect('restaurant:order_manage')


@login_required
@require_POST
def order_status_ch_menu(request, order_id):
    required_menu_id = request.POST.get('required_menu_id')
    required_order_num = request.POST.get('required_order_num')
    menu = Menu.objects.get(id=required_menu_id)
    order = customer.models.Order.objects.get(id=order_id)

    curr_menu = order.menu
    curr_num = order.num

    order.menu = menu
    order.num = required_order_num
    order.save()

    # テーブルの合計も変更する
    table_num = order.customer.table
    table = Table.objects.get(table=table_num, active=True)
    table.price -= int(curr_menu.price) * int(curr_num)
    table.price += int(menu.price) * int(required_order_num)
    table.save()

    return redirect('restaurant:order_manage')


@login_required
def history(request):
    user = User.objects.get(id=request.user.id)
    name = user.name
    active_users = nonLoginUser.objects.defer('created_at').filter(active=True)
    menus = Menu.objects.defer('created_at').order_by('id')
    order_list = ''
    start = None
    end = None
    table = None

    # 日付の範囲指定分の売上
    if request.method == 'POST':
        filter_type = request.POST.get('filter-type')
        start = request.POST.get('start')
        end = request.POST.get('end')
        table = request.POST.get('table')

        if (start != None) and (end != None):
            request.session['filter_date_start'] = start
            request.session['filter_date_end'] = end

            if 'filter_table' in request.session:
                table = request.session['filter_table']
                same_table_users = nonLoginUser.objects.defer(
                    'created_at').filter(table=table, active=True)
            else:
                same_table_users = active_users

            if start > end:
                messages.warning(request, f"左の日付をより昔にしてください。")
                (start, end) = (end, start)

            for same_table_user in same_table_users:
                active_user_order = customer.models.Order.objects.filter(
                    customer=same_table_user, created_at__range=(start, end)).order_by('-id')
                order_list = list(chain(order_list, active_user_order))

        elif filter_type == 'date-filter-clear':
            request.session['filter_date_start'] = None
            request.session['filter_date_end'] = None

            if 'filter_table' in request.session:
                table = request.session['filter_table']
                active_users = nonLoginUser.objects.defer(
                    'created_at').filter(table=table, active=True)

            for active_user in active_users:
                active_user_order = customer.models.Order.objects.filter(
                    customer=active_user).order_by('-id')
                order_list = list(chain(order_list, active_user_order))

        elif table != None:
            request.session['filter_table'] = table

            same_table_users = nonLoginUser.objects.defer(
                'created_at').filter(table=table, active=True)

            if 'filter_date_start' in request.session:
                start = request.session['filter_date_start']
                end = request.session['filter_date_end']

                for same_table_user in same_table_users:
                    same_user_order = customer.models.Order.objects.filter(
                        customer=same_table_user, created_at__range=(start, end)).order_by('-id')
                    order_list = list(chain(order_list, same_user_order))
            else:

                for same_table_user in same_table_users:
                    same_user_order = customer.models.Order.objects.filter(
                        customer=same_table_user).order_by('-id')
                    order_list = list(chain(order_list, same_user_order))

        elif filter_type == 'table-filter-clear':
            request.session['filter_table'] = None

            if 'filter_date_start' in request.session:

                if request.session['filter_date_start'] != None:
                    start = request.session['filter_date_start']
                    end = request.session['filter_date_end']
                    active_users = nonLoginUser.objects.defer(
                        'created_at').filter(active=True, created_at__range=(start, end))

            for active_user in active_users:
                active_user_order = customer.models.Order.objects.filter(
                    customer=active_user).order_by('-id')
                order_list = list(chain(order_list, active_user_order))

    else:
        # デフォルトは昨日から今日の範囲
        dt_now = datetime.datetime.now()
        start = dt_now - datetime.timedelta(days=1)
        end = dt_now

        for active_user in active_users:
            active_user_order = customer.models.Order.objects.filter(
                customer=active_user, created_at__range=(start, end)).order_by('-id')
            order_list = list(chain(order_list, active_user_order))

    ctx = {
        'name': name,
        'table': table,
        'order_list': order_list,
        'menus': menus,
        'start': start,
        'end': end,
    }

    return render(request, 'restaurant/history.html', ctx)


@login_required
def total(request):
    # 利用開始申請済みのテーブル番号リスト
    pre_admin_table_list = []
    # 利用中のテーブルお会計終了ボタンのためのリスト
    active_table_list = []
    # テーブル毎単品詳細（飲み放題メニュー抜き）のクエリセット
    orders = ''
    table_price = 0

    if Table.objects.defer('created_at').filter(active=True).count() > 1:
        table_prices = Table.objects.defer('created_at').filter(active=True)
        for each in table_prices:
            table_price += each.price

    else:

        try:
            table_price = Table.objects.get(active=True).price
        except Exception:
            pass

    pre_admin_table_user_list = nonLoginUser.objects.defer(
        'created_at').filter(allowed='pre_admin', active=True)
    active_non_login_user_list = nonLoginUser.objects.defer(
        'created_at').filter(Q(allowed='admin', active=True) | Q(allowed='allowed', active=True))
    nomiho_orders = customer.models.NomihoOrder.objects.filter(
        curr=True).order_by('created_at')

    # 利用開始申請済みのテーブル番号を抽出
    for pre_admin_table_user in pre_admin_table_user_list:
        table_int = pre_admin_table_user.table
        if table_int == None:
            continue
        table = str(table_int)

        if not table in pre_admin_table_list:
            pre_admin_table_list.append(table)

    # アクティブ客のテーブル番号を抽出
    for active_non_login_user in active_non_login_user_list:
        table_int = active_non_login_user.table
        if table_int == None:
            continue
        table = str(table_int)

        active_non_login_user_orders = customer.models.Order.objects.defer(
            'created_at').filter(status='済', customer=active_non_login_user.uuid).order_by('-id')
        orders = list(chain(orders, active_non_login_user_orders))

        # アクティブ客のテーブル番号をリスト化
        if not table in active_table_list:
            active_table_list.append(table)

    ctx = {
        'table_price': table_price,
        'pre_admin_table_list': pre_admin_table_list,
        'active_table_list': active_table_list,
        'orders': orders,
        'nomiho_orders': nomiho_orders,
    }

    return render(request, 'restaurant/total.html', ctx)


@login_required
@require_POST
def allowing(request, pre_admin_table):
    try:
        pre_admin_user = nonLoginUser.objects.get(allowed='pre_admin',
                                                  table=str(pre_admin_table), active=True)
        pre_admin_user.allowed = 'admin'
        pre_admin_user.save()

        messages.info(request, f'{pre_admin_table}テーブルの利用を許可しました。')
    except Exception:
        pass

    return redirect('restaurant:total')


@login_required
@require_POST
def deny(request, pre_admin_table):
    pre_admin_user = nonLoginUser.objects.get(allowed='pre_admin',
                                              table=str(pre_admin_table), active=True)
    pre_admin_user.allowed = 'denied'
    pre_admin_user.save()

    messages.info(request, f'{pre_admin_table}テーブルの利用を拒否しました。')

    return redirect('restaurant:total')


@login_required
@require_POST
def stop_user_order(request, active_table):
    same_user_table_list = nonLoginUser.objects.defer(
        'created_at').filter(table=str(active_table), active=True)

    for same_user in same_user_table_list:
        same_user.active = False
        same_user.save()

        same_user_carts = customer.models.Cart.objects.defer(
            'created_at').filter(customer=same_user, curr=True)
        same_user_orders = customer.models.Order.objects.defer(
            'created_at').filter(customer=same_user, curr=True)

        for same_user_cart in same_user_carts:
            # same_user_cart.curr = False
            # same_user_cart.save()
            same_user_cart.delete()
        for same_user_order in same_user_orders:
            same_user_order.curr = False
            same_user_order.save()

    nomiho_orders = customer.models.NomihoOrder.objects.defer(
        'created_at').filter(table=str(active_table), curr=True)
    for nomiho_order in nomiho_orders:
        nomiho_order.status = '終了'
        nomiho_order.curr = False
        nomiho_order.save()

    deactivate_tables = Table.objects.defer(
        'created_at').filter(table=active_table, active=True)
    for deactivate_table in deactivate_tables:
        deactivate_table.active = False
        deactivate_table.save()

    messages.info(request, f'{active_table}テーブルのお会計完了を保存しました。')

    return redirect('restaurant:total')


@login_required
@require_POST
def price_ch(request, active_table):
    try:
        get_table_price = Table.objects.get(id=active_table, active=True)
        required_price = request.POST.get('required_price')
        get_table_price.price = int(required_price)
        get_table_price.save()

        messages.info(
            request, f'{active_table}テーブルの合計金額を{required_price}円に変更しました。')
    except Exception:
        pass

    return redirect('restaurant:total')


@login_required
def daily(request):
    # 日付の範囲指定分の売上
    if request.method == 'POST':
        start = request.POST.get('start')
        end = request.POST.get('end')
        if start > end:
            messages.warning(request, f"左の日付をより昔にしてください。")
    else:
        # デフォルトは昨日から今日の範囲
        dt_now = datetime.datetime.now()
        start = dt_now - datetime.timedelta(days=1)
        end = dt_now

    pointed_tables = Table.objects.defer('created_at').filter(
        created_at__range=(start, end)).order_by('-id')
    pointed_orders = customer.models.Order.objects.exclude(
        status='キャンセル').filter(created_at__range=(start, end)).order_by('-id')
    pointed_nomiho_orders = customer.models.NomihoOrder.objects.filter(
        created_at__range=(start, end)).order_by('-id')

    pointed_total_price = 0
    pointed_order_sum = 0
    pointed_nomiho_sum = 0

    for each in pointed_tables:
        pointed_total_price += each.price
    for each in pointed_orders:
        pointed_order_sum += each.menu.price
    for each in pointed_nomiho_orders:
        pointed_nomiho_sum += each.nomiho.price

    # pointed_sum = pointed_order_sum + pointed_nomiho_sum
    # discount_pointed_price = pointed_sum - pointed_total_price

    # 総売上
    tables = Table.objects.defer('created_at')
    orders = customer.models.Order.objects.exclude(
        status='キャンセル').order_by('-id')
    nomiho_orders = customer.models.NomihoOrder.objects.order_by('-id')

    total_price = 0
    order_sum = 0
    nomiho_sum = 0

    for each in tables:
        total_price += each.price
    for each in orders:
        order_sum += each.menu.price
    for each in nomiho_orders:
        nomiho_sum += each.nomiho.price

    # sum = order_sum + nomiho_sum
    # discount_price = sum - total_price

    ctx = {
        'start': start,
        'end': end,
        'pointed_total_price': pointed_total_price,
        # 'discount_pointed_price': discount_pointed_price,
        'pointed_orders': pointed_orders,
        'pointed_nomiho_orders': pointed_nomiho_orders,
        'total_price': total_price,
        # 'discount_price': discount_price,
        'orders': orders,
        'nomiho_orders': nomiho_orders,
    }

    return render(request, 'restaurant/daily.html', ctx)


# for manageing customer screen
def manage_login(request):
    categories = Category.objects.defer('created_at').order_by('id')

    try:
        first_category = categories[0]
        menus = Menu.objects.defer('created_at').filter(
            category=first_category).order_by('-id')
    except:
        menus = None

    allergies = Allergy.objects.defer('created_at').order_by('id')

    ctx = {
        'categories': categories,
        'menus': menus,
        'allergies': allergies,
    }

    return render(request, 'restaurant/login.html', ctx)


@login_required
def manage_menu(request):
    categories = Category.objects.defer('created_at').order_by('id')

    try:
        first_category = categories[0]
        menus = Menu.objects.defer('created_at').filter(
            category=first_category).order_by('-id')
    except:
        menus = None

    allergies = Allergy.objects.defer('created_at').order_by('id')
    nomihos = Nomiho.objects.defer('created_at').order_by('-id')
    user = request.user
    restaurant_name = user.name

    ctx = {
        'categories': categories,
        'menus': menus,
        'allergies': allergies,
        'nomihos': nomihos,
        'restaurant_name': restaurant_name,
    }

    return render(request, 'customer/menu.html', ctx)


@login_required
@require_POST
def company_logo(request):
    user = request.user
    company_img = request.FILES.get('company_img')

    # 以前のファイルは削除
    user.logo.delete(False)

    user.logo = company_img
    user.save()
    messages.success(request, f"ロゴ画像を変更しました。")

    return redirect('customer:menu')


@login_required
@require_POST
def company_name(request):
    user = request.user
    company_name = request.POST.get('company_name')

    user.name = company_name
    user.save()
    messages.success(request, f"表示するお店の名前を{company_name}に変更しました。")

    return redirect('customer:menu')


@login_required
@require_POST
def category_add(request):
    name = request.POST.get('add_category_form')

    try:
        nomiho = request.POST.get('nomiho')
    except Exception:
        nomiho = False

    if Category.objects.filter(name=name).count() == 0:
        category = Category(name=name, nomiho=nomiho)
        category.save()
        messages.success(request, f"カテゴリーに{name}を追加しました。")
    else:
        messages.warning(request, f"同一の名前のカテゴリーは作成できません。")

    return redirect('customer:menu')


@login_required
@require_POST
def category_ch(request):
    name = request.POST.get('category_name')
    required_name = request.POST.get('ch_category_form')

    category = Category.objects.get(name=name)
    category.name = required_name

    if request.POST.get('nomiho') != None:
        category.nomiho = True
        # 飲み放題ではないカテゴリから飲み放題カテゴリにした場合、その中にある全てのメニューの金額を0にする
        menus_in_this_categories = Menu.objects.defer(
            'created_at').filter(category=category)

        for menus_in_this_category in menus_in_this_categories:
            menus_in_this_category.price = 0
            menus_in_this_category.save()
    else:
        category.nomiho = False

    category.save()
    messages.success(request, f"カテゴリー{name}を変更しました。")

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
def category_menu_ch(request):
    menu_id = request.POST.get('menu_id')
    category_id = request.POST.get('category_id')

    menu = Menu.objects.get(id=menu_id)
    category = Category.objects.get(id=category_id)
    menu.category = category
    menu.save()

    menu_name = menu.name
    pre_category = menu.category.name
    category_name = category.name

    messages.success(
        request, f"{menu_name}のカテゴリーを{pre_category}から{category_name}に変更しました。")

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

        # 飲み放題カテゴリに追加するメニューは、たとえ間違って金額を0以外で入力しても、0にする処理をする
        if menu.category.nomiho == True:
            nomiho_categorys = Category.objects.defer(
                'created_at').filter(nomiho=True)

            for nomiho_category in nomiho_categorys:
                nomiho_menus = Menu.objects.defer(
                    'created_at').filter(category=nomiho_category)

                for nomiho_menu in nomiho_menus:
                    nomiho_menu.price = 0
                    nomiho_menu.save()

    return redirect('customer:menu')


@login_required
@require_POST
def menu_del(request, menu_id):
    menu = Menu.objects.get(id=menu_id)
    menu.delete()
    name = menu.name
    messages.success(request, f"{name}をメニューから削除しました。")

    return redirect('customer:menu')


@login_required
@require_POST
def menu_img_manage(request, menu_id):
    menu_img = request.FILES.get('menu_img')
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
def menu_name_manage(request, menu_id):
    menu_name = request.POST.get('menu_name')
    menu = Menu.objects.get(id=menu_id)
    menu.name = menu_name
    menu.save()
    messages.success(request, f"{menu_name}に名前を変更しました。")

    return redirect('customer:menu_detail', menu_id=menu.id)


@login_required
@require_POST
def menu_price_manage(request, menu_id):
    menu_price = request.POST.get('menu_price')
    menu = Menu.objects.get(id=menu_id)
    menu.price = menu_price
    menu.save()
    name = menu.name
    messages.success(request, f"{name}の金額を{menu_price}円に変更しました。")

    return redirect('customer:menu_detail', menu_id=menu.id)


@login_required
@require_POST
def allergy_ch(request, menu_id):
    allergy_list = request.POST.getlist('allergy')

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
    get_allergy_query = Allergy.objects.filter(ingredient=get_allergy)

    if get_allergy_query.count() == 0:
        menu.allergies.create(ingredient=get_allergy)
        menu.save()
        messages.success(request, f"{get_allergy}をアレルギー項目一覧に追加しました。")
    else:
        messages.info(request, f"同一の名前のアレルギーを項目に追加はできません。")

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


@login_required
@require_POST
def chef(request, menu_id):
    chef_img = request.FILES.get('chef_img')
    comment = request.POST.get('comment')
    menu = Menu.objects.get(id=menu_id)

    # 以前のファイルは削除
    if not menu.chef_img == None:
        menu.chef_img.delete(False)

    menu.chef_img = chef_img
    menu.comment = comment
    menu.save()
    name = menu.name
    messages.success(request, f"{name}のシェフの顔写真・コメントを更新しました。")

    return redirect('customer:menu_detail', menu_id=menu.id)


@login_required
@require_POST
def nomiho_add(request):
    nomiho_name = request.POST.get('nomiho_name')
    nomiho_price = request.POST.get('nomiho_price')
    nomiho_duration = request.POST.get('nomiho_duration')
    nomiho_comment = request.POST.get('nomiho_comment')

    nomiho = Nomiho(name=nomiho_name, price=nomiho_price,
                    duration=nomiho_duration, comment=nomiho_comment)
    nomiho.save()
    messages.success(request, f"飲み放題プラン『{nomiho_name}』を追加しました。")

    return redirect('customer:menu')


@login_required
@require_POST
def nomiho_ch(request):
    nomiho_id = request.POST.get('nomiho_id')
    nomiho = Nomiho.objects.get(id=nomiho_id)

    nomiho_name = request.POST.get('nomiho_name')
    nomiho_price = request.POST.get('nomiho_price')
    nomiho_duration = request.POST.get('nomiho_duration')
    nomiho_comment = request.POST.get('nomiho_comment')

    nomiho.name = nomiho_name
    nomiho.price = nomiho_price
    nomiho.duration = nomiho_duration
    nomiho.comment = nomiho_comment
    nomiho.save()
    messages.success(request, f"飲み放題プランの内容を変更しました。")

    return redirect('customer:menu')


@login_required
@require_POST
def nomiho_del(request):
    id = request.POST.get('del_nomiho_form')
    nomiho = Nomiho.objects.get(id=id)
    name = nomiho.name
    nomiho.delete()
    messages.success(request, f"飲み放題プランから{name}を削除しました。")

    return redirect('customer:menu')
