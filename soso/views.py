from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.generic import View
from django.db import transaction


from soso.models import AccountUser, ShoppingItem, ShoppingItemsincart
from soso.forms import UserLoginForm, UserCreateForm, UserUpdateForm, SearchForm
from django.db.models import Avg
from soso.models import ShoppingReview
from soso.forms import ReviewForm
from soso.models import (
    AccountUser,
    ShoppingItem,
    ShoppingItemsincart,
    ShoppingPurchase,
    ShoppingPurchasedetail,
    ShoppingCategory,
    AdministratorAdmin,
)

from soso.forms import (
    UserLoginForm,
    UserCreateForm,
    UserUpdateForm,
    SearchForm,
    PurchaseForm,
    AdminLoginForm,
    ItemForm,
    ItemEditForm,
    PurchaseSearchForm,
)

# ──────────────────────────────────────
# ログイン中のユーザーを取得
# ──────────────────────────────────────
def get_login_user(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return None
    try:
        return AccountUser.objects.get(user_id=user_id)
    except AccountUser.DoesNotExist:
        return None


# ──────────────────────────────────────
# ログイン
# ──────────────────────────────────────
class UserLogin(View):
    def get(self, request):
        form = UserLoginForm()
        return render(request, "soso/login.html", {"form": form})

    def post(self, request):
        form = UserLoginForm(request.POST)

        user_exists = AccountUser.objects.filter(
            user_id=request.POST["user_id"],
            password=request.POST["password"],
        ).exists()

        if not user_exists:
            context = {
                "form": form,
                "error": "ユーザ名またはパスワードが違います",
            }
            return render(request, "soso/login.html", context)

        request.session["user_id"] = request.POST["user_id"]
        return redirect("soso:top_page")


# ──────────────────────────────────────
# ログアウト
# ──────────────────────────────────────
class UserLogout(View):
    def get(self, request):
        request.session.flush()
        return redirect("soso:user_login")


# ──────────────────────────────────────
# 新規会員登録
# ──────────────────────────────────────
class UserCreate(View):
    def get(self, request):
        form = UserCreateForm()
        return render(request, "soso/registerUser.html", {"form": form})

    def post(self, request):
        form = UserCreateForm(request.POST)

        if not form.is_valid():
            return render(request, "soso/registerUser.html", {"form": form})

        if AccountUser.objects.filter(user_id=form.cleaned_data["user_id"]).exists():
            context = {
                "form": form,
                "error": "そのユーザ名は既に使用されています",
            }
            return render(request, "soso/registerUser.html", context)

        return render(request, "soso/registerUserConfirm.html", {"form": form})


class UserCreateConfirm(View):
    def get(self, request):
        return redirect("soso:user_create")

    def post(self, request):
        new_user = AccountUser()
        new_user.user_id = request.POST["user_id"]
        new_user.password = request.POST["password_1"]
        new_user.name = request.POST["name"]
        new_user.address = request.POST["address"]
        new_user.save()

        request.session["user_id"] = new_user.user_id
        return render(request, "soso/registerUserCommit.html", {"user_info": new_user})


# ──────────────────────────────────────
# トップページ（検索フォーム表示）
# ──────────────────────────────────────
class TopPage(View):
    def get(self, request):
        user_info = get_login_user(request)
        form = SearchForm()

        # ★ おすすめ商品を取得
        recommended_items = ShoppingItem.objects.filter(recommended=True)

        context = {
            "user_info": user_info,
            "form": form,
            "recommended_items": recommended_items,
        }
        return render(request, "soso/main.html", context)


# ──────────────────────────────────────
# 商品検索（GET）
# ──────────────────────────────────────
class SearchResult(View):
    def get(self, request):
        form = SearchForm(request.GET)

        products = None
        if form.is_valid():
            category = form.cleaned_data.get("category", "すべて")
            keyword = form.cleaned_data.get("keyword", "")

            products = ShoppingItem.objects.all()

            # ★ category_map 不要！IDで直接フィルタ
            if category != "すべて":
                products = products.filter(category_id=category)
            if keyword:
                products = products.filter(name__icontains=keyword)

        context = {
            "form": form,
            "products": products,
        }
        return render(request, "soso/searchResult.html", context)


# ──────────────────────────────────────
# 会員情報の確認
# ──────────────────────────────────────
class UserInfo(View):
    def get(self, request):
        user_info = get_login_user(request)
        if not user_info:
            return redirect("soso:user_login")
        return render(request, "soso/userInfo.html", {"user_info": user_info})


# ──────────────────────────────────────
# 会員情報の変更
# ──────────────────────────────────────
class UserUpdate(View):
    def get(self, request):
        user = get_login_user(request)
        if not user:
            return redirect("soso:user_login")

        form = UserUpdateForm(initial={
            "user_id": user.user_id,
            "name": user.name,
            "address": user.address,
        })
        return render(request, "soso/updateUser.html", {"form": form})

    def post(self, request):
        user = get_login_user(request)
        if not user:
            return redirect("soso:user_login")

        form = UserUpdateForm(request.POST, initial={"user_id": user.user_id})

        if not form.is_valid():
            return render(request, "soso/updateUser.html", {"form": form})

        return render(request, "soso/updateUserConfirm.html", {"form": form})


class UserUpdateConfirm(View):
    def get(self, request):
        return redirect("soso:user_update")

    def post(self, request):
        user = get_login_user(request)
        if not user:
            return redirect("soso:user_login")

        user.password = request.POST["password_1"]
        user.name = request.POST["name"]
        user.address = request.POST["address"]
        user.save()

        return render(request, "soso/updateUserCommit.html", {"user_info": user})


# ──────────────────────────────────────
# 退会
# ──────────────────────────────────────
class UserWithdrawConfirm(View):
    def get(self, request):
        user_info = get_login_user(request)
        if not user_info:
            return redirect("soso:user_login")
        return render(request, "soso/withdrawConfirm.html", {"user_info": user_info})


class UserWithdrawCommit(View):
    def post(self, request):
        user = get_login_user(request)
        if not user:
            return redirect("soso:user_login")

        name = user.name
        user.delete()
        request.session.flush()
        return render(request, "soso/withdrawCommit.html", {"name": name})


# ──────────────────────────────────────
# 商品詳細
# ──────────────────────────────────────
class ItemDetail(View):
    def get(self, request, item_id):
        item_info = ShoppingItem.objects.get(item_id=item_id)
        numbers = range(1, item_info.stock + 1)

        
        reviews = ShoppingReview.objects.filter(item=item_info).order_by("-created_at")
        avg_rating = reviews.aggregate(Avg("rating"))["rating__avg"]
        user = get_login_user(request)
        already_reviewed = False
        if user:
            already_reviewed = ShoppingReview.objects.filter(item=item_info, user=user).exists()
        form = ReviewForm()
    

        return render(request, "soso/itemDetail.html", {
            "item_info": item_info,
            "numbers": numbers,    
            "reviews": reviews,
            "avg_rating": avg_rating,
            "form": form,
            "already_reviewed": already_reviewed,
            "user_info": user,
        
        })


# ──────────────────────────────────────
# ショッピングカート
# ──────────────────────────────────────
class ShoppingCart(View):
    def get(self, request):
        user = get_login_user(request)
        if not user:
            return redirect("soso:user_login")

        cart_items = ShoppingItemsincart.objects.filter(user=user)

        total = 0
        for ci in cart_items:
            ci.amount_choices = range(1, ci.item.stock + 1)  # ★これ追加
            total += ci.item.price * ci.amount

        context = {
            "cart_items": cart_items,
            "total": total,
        }
        return render(request, "soso/cart.html", context)

    def post(self, request):
        user = get_login_user(request)
        if not user:
            return redirect("soso:user_login")

        item_id = request.POST.get("item_id")
        num = int(request.POST.get("num", 1))

        item = ShoppingItem.objects.get(item_id=item_id)

        cart_item = ShoppingItemsincart.objects.filter(
            user=user,
            item=item,
        ).first()

        if cart_item:
            cart_item.amount += num
            cart_item.booked_date = timezone.now()
            cart_item.save()
        else:
            ShoppingItemsincart.objects.create(
                user=user,
                item=item,
                amount=num,
                booked_date=timezone.now(),
            )

        return redirect("soso:shopping_cart")

# ──────────────────────────────────────
# カート数量変更
# ──────────────────────────────────────
class ShoppingCartUpdate(View):
    def post(self, request, cart_id):
        user = get_login_user(request)
        if not user:
            return redirect("soso:user_login")

        cart_item = ShoppingItemsincart.objects.get(id=cart_id, user=user)

        amount = request.POST.get("amount")

        try:
            amount = int(amount)
        except:
            return redirect("soso:shopping_cart")

        if amount <= 0:
            return redirect("soso:shopping_cart")

        if cart_item.item.stock < amount:
            return redirect("soso:shopping_cart")

        cart_item.amount = amount
        cart_item.booked_date = timezone.now()
        cart_item.save()

        return redirect("soso:shopping_cart")

# ──────────────────────────────────────
# カート削除
# ──────────────────────────────────────
class ShoppingCartDelete(View):
    def post(self, request, cart_id):
        user = get_login_user(request)
        if not user:
            return redirect("soso:user_login")

        cart_item = ShoppingItemsincart.objects.get(id=cart_id, user=user)
        cart_item.delete()

        return redirect("soso:shopping_cart")
    
# ──────────────────────────────────────
# 購入画面
# ──────────────────────────────────────
class Purchase(View):
    def get(self, request):
        user = get_login_user(request)
        if not user:
            return redirect("soso:user_login")

        cart_items = ShoppingItemsincart.objects.filter(user=user)

        if not cart_items:
            return redirect("soso:shopping_cart")

        total = 0
        for ci in cart_items:
            ci.subtotal = ci.item.price * ci.amount   # ★追加
            total += ci.subtotal

        form = PurchaseForm(initial={
            "destination": user.address,
            "payment_method": "cod",
        })

        context = {
            "cart_items": cart_items,
            "total": total,
            "form": form,
            "user_info": user,
        }

        return render(request, "soso/purchase.html", context)

# ──────────────────────────────────────
# 購入確認画面
# ──────────────────────────────────────
class PurchaseConfirm(View):
    def post(self, request):
        user = get_login_user(request)
        if not user:
            return redirect("soso:user_login")

        cart_items = ShoppingItemsincart.objects.filter(user=user)

        if not cart_items:
            return redirect("soso:shopping_cart")

        destination = (request.POST.get("destination") or "").strip()
        if not destination:
            destination = user.address

        payment_method = "代金引換"

        total = 0
        for ci in cart_items:
            ci.subtotal = ci.item.price * ci.amount
            total += ci.subtotal

        context = {
            "cart_items": cart_items,
            "total": total,
            "destination": destination,
            "payment_method": payment_method,
        }
        return render(request, "soso/purchaseConfirm.html", context) 

# ──────────────────────────────────────
# 購入確定
# ──────────────────────────────────────
class PurchaseCommit(View):
    def post(self, request):
        user = get_login_user(request)
        if not user:
            return redirect("soso:user_login")

        cart_items = ShoppingItemsincart.objects.filter(user=user).select_related("item")

        if not cart_items.exists():
            return redirect("soso:shopping_cart")

        destination = request.POST.get("destination", "").strip()
        if not destination:
            destination = user.address

        payment_method = "代金引換"

        # ① 先に全商品の在庫確認
        total = 0
        for ci in cart_items:
            if ci.item.stock < ci.amount:
                # 再表示用にsubtotalを作る
                for x in cart_items:
                    x.subtotal = x.item.price * x.amount

                context = {
                    "cart_items": cart_items,
                    "total": sum(x.item.price * x.amount for x in cart_items),
                    "destination": destination,
                    "payment_method": payment_method,
                    "error": f"{ci.item.name} の在庫が不足しています。",
                }
                return render(request, "soso/purchaseConfirm.html", context)

            total += ci.item.price * ci.amount

        # ② 問題なければまとめて保存
        with transaction.atomic():
            last_purchase = ShoppingPurchase.objects.order_by("-purchase_id").first()
            next_purchase_id = 1 if not last_purchase else last_purchase.purchase_id + 1

            purchase = ShoppingPurchase.objects.create(
                purchase_id=next_purchase_id,
                destination=destination,
                cancel=False,
                user=user,
            )

            last_detail = ShoppingPurchasedetail.objects.order_by("-purchase_detail_id").first()
            next_detail_id = 1 if not last_detail else last_detail.purchase_detail_id + 1

            for ci in cart_items:
                ShoppingPurchasedetail.objects.create(
                    purchase_detail_id=next_detail_id,
                    purchase=purchase,
                    item=ci.item,
                    amount=ci.amount,
                )
                next_detail_id += 1

                ci.item.stock -= ci.amount
                ci.item.save()

            cart_items.delete()

        context = {
            "purchase": purchase,
            "destination": destination,
            "payment_method": payment_method,
            "total": total,
        }

        return render(request, "soso/purchaseCommit.html", context)

# ──────────────────────────────────────
# 購入履歴一覧
# ──────────────────────────────────────
class UserPurchaseHistory(View):
    def get(self, request):
        user = get_login_user(request)
        if not user:
            return redirect("soso:user_login")

        purchases = ShoppingPurchase.objects.filter(user=user).order_by("-booked_date")

        context = {
            "user_info": user,
            "purchases": purchases,
        }
        return render(request, "soso/userPurchaseHistory.html", context)

# ──────────────────────────────────────
# 購入履歴詳細
# ──────────────────────────────────────
class UserPurchaseDetail(View):
    def get(self, request, purchase_id):
        user = get_login_user(request)
        if not user:
            return redirect("soso:user_login")

        try:
            purchase = ShoppingPurchase.objects.get(purchase_id=purchase_id, user=user)
        except ShoppingPurchase.DoesNotExist:
            return redirect("soso:user_purchase_history")

        details = ShoppingPurchasedetail.objects.filter(purchase=purchase).select_related("item")

        total = 0
        for detail in details:
            detail.subtotal = detail.item.price * detail.amount
            total += detail.subtotal

        context = {
            "user_info": user,
            "purchase": purchase,
            "details": details,
            "total": total,
        }
        return render(request, "soso/userPurchaseDetail.html", context)

# ──────────────────────────────────────
# ヘルパー：管理者ログインチェック
# ──────────────────────────────────────
def get_login_admin(request):
    admin_id = request.session.get("admin_id")
    if not admin_id:
        return None
    try:
        return AdministratorAdmin.objects.get(admin_id=admin_id)
    except AdministratorAdmin.DoesNotExist:
        return None


# ──────────────────────────────────────
# 管理者ログイン（既存のまま）
# ──────────────────────────────────────
class AdminLogin(View):
    def get(self, request):
        form = AdminLoginForm()
        return render(request, "soso/adminLogin.html", {"form": form})

    def post(self, request):
        form = AdminLoginForm(request.POST)

        admin_exists = AdministratorAdmin.objects.filter(
            admin_id=request.POST["admin_id"],
            password=request.POST["password"],
        ).exists()

        if not admin_exists:
            context = {
                "form": form,
                "error": "管理者IDまたはパスワードが違います",
            }
            return render(request, "soso/adminLogin.html", context)

        request.session["admin_id"] = request.POST["admin_id"]
        return redirect("soso:admin_top")


# ──────────────────────────────────────
# 管理者メインページ
# ──────────────────────────────────────
class AdminTopPage(View):
    def get(self, request):
        admin = get_login_admin(request)
        if not admin:
            return redirect("soso:admin_login")

        return render(request, "soso/adminMain.html", {"admin_id": admin.admin_id})


# ──────────────────────────────────────
# 管理者ログアウト
# ──────────────────────────────────────
class AdminLogout(View):
    def get(self, request):
        request.session.flush()
        return redirect("soso:admin_login")


# ══════════════════════════════════════
# 商品管理
# ══════════════════════════════════════

# ──────────────────────────────────────
# 商品一覧
# ──────────────────────────────────────
class AdminItemList(View):
    def get(self, request):
        admin = get_login_admin(request)
        if not admin:
            return redirect("soso:admin_login")

        items = ShoppingItem.objects.all().order_by("item_id")
        return render(request, "soso/adminItemList.html", {"items": items})


# ──────────────────────────────────────
# 商品登録
# ──────────────────────────────────────
class AdminItemCreate(View):
    def get(self, request):
        admin = get_login_admin(request)
        if not admin:
            return redirect("soso:admin_login")

        form = ItemForm()
        return render(request, "soso/adminItemCreate.html", {"form": form})

    def post(self, request):
        admin = get_login_admin(request)
        if not admin:
            return redirect("soso:admin_login")

        # ★ request.FILES を追加（画像データを受け取る）
        form = ItemForm(request.POST, request.FILES)
        if not form.is_valid():
            return render(request, "soso/adminItemCreate.html", {"form": form})

        if ShoppingItem.objects.filter(item_id=form.cleaned_data["item_id"]).exists():
            context = {
                "form": form,
                "error": "その商品IDは既に存在します",
            }
            return render(request, "soso/adminItemCreate.html", context)

        ShoppingItem.objects.create(
            item_id=form.cleaned_data["item_id"],
            name=form.cleaned_data["name"],
            manufacturer=form.cleaned_data["manufacturer"],
            color=form.cleaned_data["color"],
            price=form.cleaned_data["price"],
            stock=form.cleaned_data["stock"],
            recommended=form.cleaned_data["recommended"],
            category=form.cleaned_data["category"],
            image=form.cleaned_data.get("image"),  # ★ 画像を保存
        )
        return redirect("soso:admin_item_list")


# ──────────────────────────────────────
# 商品修正
# ──────────────────────────────────────
class AdminItemEdit(View):
    def get(self, request, item_id):
        admin = get_login_admin(request)
        if not admin:
            return redirect("soso:admin_login")

        item = ShoppingItem.objects.get(item_id=item_id)
        form = ItemEditForm(initial={
            "item_id": item.item_id,
            "name": item.name,
            "manufacturer": item.manufacturer,
            "color": item.color,
            "price": item.price,
            "stock": item.stock,
            "recommended": item.recommended,
            "category": item.category,
        })
        return render(request, "soso/adminItemEdit.html", {
            "form": form,
            "item_id": item_id,
            "item": item,  # ★ 現在の画像表示用
        })

    def post(self, request, item_id):
        admin = get_login_admin(request)
        if not admin:
            return redirect("soso:admin_login")

        # ★ request.FILES を追加
        form = ItemEditForm(request.POST, request.FILES, initial={"item_id": item_id})
        if not form.is_valid():
            item = ShoppingItem.objects.get(item_id=item_id)
            return render(request, "soso/adminItemEdit.html", {
                "form": form,
                "item_id": item_id,
                "item": item,
            })

        item = ShoppingItem.objects.get(item_id=item_id)
        item.name = form.cleaned_data["name"]
        item.manufacturer = form.cleaned_data["manufacturer"]
        item.color = form.cleaned_data["color"]
        item.price = form.cleaned_data["price"]
        item.stock = form.cleaned_data["stock"]
        item.recommended = form.cleaned_data["recommended"]
        item.category = form.cleaned_data["category"]

        # ★ 新しい画像がアップロードされた場合のみ更新
        if form.cleaned_data.get("image"):
            item.image = form.cleaned_data["image"]

        item.save()
        return redirect("soso:admin_item_list")


# ──────────────────────────────────────
# 商品削除
# ──────────────────────────────────────
class AdminItemDelete(View):
    def get(self, request, item_id):
        admin = get_login_admin(request)
        if not admin:
            return redirect("soso:admin_login")

        item = ShoppingItem.objects.get(item_id=item_id)
        return render(request, "soso/adminItemDelete.html", {"item": item})

    def post(self, request, item_id):
        admin = get_login_admin(request)
        if not admin:
            return redirect("soso:admin_login")

        item = ShoppingItem.objects.get(item_id=item_id)
        item.delete()
        return redirect("soso:admin_item_list")


# ══════════════════════════════════════
# おすすめ管理
# ══════════════════════════════════════
class AdminRecommend(View):
    def get(self, request):
        admin = get_login_admin(request)
        if not admin:
            return redirect("soso:admin_login")

        items = ShoppingItem.objects.all().order_by("item_id")
        return render(request, "soso/adminRecommend.html", {"items": items})

    def post(self, request):
        admin = get_login_admin(request)
        if not admin:
            return redirect("soso:admin_login")

        # チェックされた商品IDのリストを取得
        recommended_ids = request.POST.getlist("recommended")

        # 全商品のおすすめを一旦OFFにしてから、チェックされたものだけON
        ShoppingItem.objects.all().update(recommended=False)
        ShoppingItem.objects.filter(item_id__in=recommended_ids).update(recommended=True)

        return redirect("soso:admin_recommend")


# ══════════════════════════════════════
# 購入履歴検索・キャンセル
# ══════════════════════════════════════

# ──────────────────────────────────────
# 購入履歴検索
# ──────────────────────────────────────
class AdminPurchaseSearch(View):
    def get(self, request):
        admin = get_login_admin(request)
        if not admin:
            return redirect("soso:admin_login")

        form = PurchaseSearchForm(request.GET or None)
        purchases = None

        if form.is_valid():
            user_id = form.cleaned_data.get("user_id")
            purchase_id = form.cleaned_data.get("purchase_id")

            purchases = ShoppingPurchase.objects.all().order_by("-booked_date")

            if user_id:
                purchases = purchases.filter(user__user_id=user_id)
            if purchase_id:
                purchases = purchases.filter(purchase_id=purchase_id)

        context = {
            "form": form,
            "purchases": purchases,
        }
        return render(request, "soso/adminPurchaseSearch.html", context)


# ──────────────────────────────────────
# 購入詳細
# ──────────────────────────────────────
class AdminPurchaseDetail(View):
    def get(self, request, purchase_id):
        admin = get_login_admin(request)
        if not admin:
            return redirect("soso:admin_login")

        purchase = ShoppingPurchase.objects.get(purchase_id=purchase_id)
        details = ShoppingPurchasedetail.objects.filter(purchase=purchase)

        context = {
            "purchase": purchase,
            "details": details,
        }
        return render(request, "soso/adminPurchaseDetail.html", context)


# ──────────────────────────────────────
# 購入キャンセル
# ──────────────────────────────────────
class AdminPurchaseCancel(View):
    def post(self, request, purchase_id):
        admin = get_login_admin(request)
        if not admin:
            return redirect("soso:admin_login")

        purchase = ShoppingPurchase.objects.get(purchase_id=purchase_id)
        purchase.cancel = True
        purchase.save()

        return redirect("soso:admin_purchase_detail", purchase_id=purchase_id)

class ReviewCreate(View):
    def post(self, request, item_id):
        user = get_login_user(request)
        if not user:
            return redirect("soso:user_login")

        item = ShoppingItem.objects.get(item_id=item_id)

        if ShoppingReview.objects.filter(item=item, user=user).exists():
            return redirect("soso:item_detail", item_id=item_id)

        form = ReviewForm(request.POST)

        if not form.is_valid():
            reviews = ShoppingReview.objects.filter(item=item).order_by("-created_at")
            avg_rating = reviews.aggregate(Avg("rating"))["rating__avg"]
            numbers = range(1, item.stock + 1)
            return render(request, "soso/itemDetail.html", {
                "item_info": item,
                "numbers": numbers,
                "reviews": reviews,
                "avg_rating": avg_rating,
                "form": form,
                "already_reviewed": False,
                "user_info": user,
            })

        ShoppingReview.objects.create(
            item=item,
            user=user,
            rating=form.cleaned_data["rating"],
            comment=form.cleaned_data["comment"],
        )
        return redirect("soso:item_detail", item_id=item_id)
    
    
from soso.models import (
    AccountUser, ShoppingItem, ShoppingItemsincart,
    ShoppingCategory, ShoppingPurchase, ShoppingPurchasedetail,
    AdministratorAdmin, ShoppingReview,  # ★ 追加
)


# ──────────────────────────────────────
# レビュータイムライン
# ──────────────────────────────────────
class ReviewTimeline(View):
    def get(self, request):
        # 新しい順に全レビューを取得（関連データも一緒に）
        reviews = ShoppingReview.objects.select_related(
            "item", "user"
        ).order_by("-created_at")

        context = {
            "reviews": reviews,
        }
        return render(request, "soso/reviewTimeline.html", context)