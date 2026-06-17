from django.db import models

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
