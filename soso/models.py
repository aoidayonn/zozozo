from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
class AccountUser(models.Model):
    # 記事モデル
    class Meta:
        # テーブル名定義
        db_table = "account_user"

    # テーブルフィールド定義
    user_id = models.CharField(verbose_name="会員ID", max_length=128, primary_key=True)
    password = models.CharField(verbose_name="パスワード", max_length=256)
    name = models.CharField(verbose_name="名前", max_length=128)
    address = models.CharField(verbose_name="住所",max_length=256)


class ShoppingCategory(models.Model):
    # 記事モデル
    class Meta:
        # テーブル名定義
        db_table = "shopping_category"

    # テーブルフィールド定義
    category_id = models.IntegerField(verbose_name="カテゴリID", primary_key=True)
    name = models.CharField(verbose_name="カテゴリ名", max_length=256)


class ShoppingItem(models.Model):
    # 記事モデル
    class Meta:
        # テーブル名定義
        db_table = "shopping_item"

    # テーブルフィールド定義
    item_id = models.IntegerField(verbose_name="商品ID", primary_key=True)
    name = models.CharField(verbose_name="商品名", max_length=128)
    manufacturer = models.CharField(verbose_name="メーカ名",max_length=32)
    color = models.CharField(verbose_name="商品の色",max_length=16)
    price = models.IntegerField(verbose_name="価格")
    stock = models.IntegerField(verbose_name="在庫数")
    recommended = models.BooleanField(verbose_name="おすすめ", max_length=1, default=False)
    category = models.ForeignKey(ShoppingCategory, verbose_name="カテゴリID", on_delete=models.CASCADE)
    # ★ 画像フィールドを追加
    image = models.ImageField(
        verbose_name="商品画像",
        upload_to="soso/images/",
        blank=True,
        null=True,
    )



class ShoppingItemsincart(models.Model):
    # 記事モデル
    class Meta:
        # テーブル名定義
        db_table = "shopping_itemsincart"

    # テーブルフィールド定義
    amount = models.IntegerField(verbose_name="数量")
    booked_date = models.DateTimeField(verbose_name="登録日")
    item = models.ForeignKey(ShoppingItem, verbose_name="商品ID", on_delete=models.CASCADE)
    user = models.ForeignKey(AccountUser, verbose_name="会員ID", on_delete=models.CASCADE)


class ShoppingPurchase(models.Model):
    # 記事モデル
    class Meta:
        # テーブル名定義
        db_table = "shopping_purchase"

    # テーブルフィールド定義
    purchase_id = models.IntegerField(verbose_name="注文ID", primary_key=True)
    destination = models.CharField(verbose_name="配送先", max_length=256)
    booked_date = models.DateTimeField(verbose_name="注文日", auto_now_add=True)
    cancel = models.BooleanField(verbose_name="キャンセル", max_length=1, default=False)
    user = models.ForeignKey(AccountUser, verbose_name="注文者", on_delete=models.CASCADE)


class ShoppingPurchasedetail(models.Model):
    # 記事モデル
    class Meta:
        # テーブル名定義
        db_table = "shopping_purchasedetail"

    # テーブルフィールド定義
    purchase_detail_id = models.IntegerField(verbose_name="注文詳細ID", primary_key=True)
    amount = models.IntegerField(verbose_name="注文数")
    item = models.ForeignKey(ShoppingItem, verbose_name="商品ID", on_delete=models.CASCADE)
    purchase = models.ForeignKey(ShoppingPurchase, verbose_name="注文ID", on_delete=models.CASCADE)


class AdministratorAdmin(models.Model):
    # 記事モデル
    class Meta:
        # テーブル名定義
        db_table = "administrator_admin"

    # テーブルフィールド定義
    admin_id = models.CharField(verbose_name="管理者ID", max_length=128 ,primary_key=True)
    password = models.CharField(verbose_name="パスワード", max_length=256)


class ShoppingReview(models.Model):
    class Meta:
        db_table = "shopping_review"
        unique_together = ("item", "user")

    review_id = models.AutoField(verbose_name="レビューID", primary_key=True)
    rating = models.IntegerField(
        verbose_name="評価",
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    comment = models.CharField(verbose_name="コメント", max_length=500)
    created_at = models.DateTimeField(verbose_name="投稿日", auto_now_add=True)
    item = models.ForeignKey(ShoppingItem, verbose_name="商品ID", on_delete=models.CASCADE)
    user = models.ForeignKey(AccountUser, verbose_name="会員ID", on_delete=models.CASCADE)

import random
import string
from django.utils import timezone
from datetime import timedelta


class ShoppingCoupon(models.Model):
    class Meta:
        db_table = "shopping_coupon"

    coupon_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(AccountUser, on_delete=models.CASCADE)
    code = models.CharField(verbose_name="クーポンコード", max_length=20, unique=True)
    discount_rate = models.IntegerField(verbose_name="割引率(%)")
    rarity = models.CharField(verbose_name="レア度", max_length=20)
    expires_at = models.DateTimeField(verbose_name="有効期限")
    used = models.BooleanField(verbose_name="使用済み", default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class GachaHistory(models.Model):
    class Meta:
        db_table = "gacha_history"

    history_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(AccountUser, on_delete=models.CASCADE)
    drawn_at = models.DateTimeField(auto_now_add=True)
    
    
class TetrisPoint(models.Model):
    class Meta:
        db_table = "tetris_point"

    user = models.OneToOneField(AccountUser, on_delete=models.CASCADE, primary_key=True)
    points = models.IntegerField(verbose_name="所持ポイント", default=0)
    total_wins = models.IntegerField(verbose_name="勝利数", default=0)
    updated_at = models.DateTimeField(auto_now=True)


# ★ テトリスガチャ専用の履歴（無制限に引ける）
class TetrisGachaHistory(models.Model):
    class Meta:
        db_table = "tetris_gacha_history"

    history_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(AccountUser, on_delete=models.CASCADE)
    rarity = models.CharField(verbose_name="レア度", max_length=20)
    discount_rate = models.IntegerField(verbose_name="割引率")
    drawn_at = models.DateTimeField(auto_now_add=True)