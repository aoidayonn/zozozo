from django import forms
from soso.models import ShoppingCategory




class CategoryChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name


class UserLoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""

    user_id = forms.CharField(label="会員ID:", max_length=128)
    password = forms.CharField(
        label="パスワード:",
        max_length=256,
        widget=forms.PasswordInput,
    )


class UserCreateForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""

    user_id = forms.CharField(label="会員ID:", max_length=128)
    password_1 = forms.CharField(
        label="パスワード:",
        max_length=256,
        widget=forms.PasswordInput,
    )
    password_2 = forms.CharField(
        label="パスワード(確認):",
        max_length=256,
        widget=forms.PasswordInput,
    )
    name = forms.CharField(label="お名前:", max_length=128)
    address = forms.CharField(label="ご住所:", max_length=256)

    def clean(self):
        cleaned_data = super().clean()
        password_1 = cleaned_data.get("password_1")
        password_2 = cleaned_data.get("password_2")
        if password_1 != password_2:
            raise forms.ValidationError("パスワードと確認用パスワードが一致しません")
        return cleaned_data


class UserUpdateForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""

    user_id = forms.CharField(label="会員ID:", max_length=128, disabled=True)
    password_1 = forms.CharField(
        label="パスワード:",
        max_length=256,
        widget=forms.PasswordInput,   # ★ 入力時 ●●●● で隠れる
    )
    password_2 = forms.CharField(
        label="パスワード(確認):",
        max_length=256,
        widget=forms.PasswordInput,   # ★ 入力時 ●●●● で隠れる
    )
    name = forms.CharField(label="お名前:", max_length=128)
    address = forms.CharField(label="ご住所:", max_length=256)

    def clean(self):
        cleaned_data = super().clean()
        password_1 = cleaned_data.get("password_1")
        password_2 = cleaned_data.get("password_2")
        if password_1 != password_2:
            raise forms.ValidationError("パスワードと確認用パスワードが一致しません")
        return cleaned_data

    def clean(self):
        cleaned_data = super().clean()
        password_1 = cleaned_data.get("password_1")
        password_2 = cleaned_data.get("password_2")
        if password_1 != password_2:
            raise forms.ValidationError("パスワードと確認用パスワードが一致しません")
        return cleaned_data
    
    
class SearchForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""

        # ★ DBからカテゴリを動的に取得
        category_choices = [("すべて", "すべて")]
        category_choices += [
            (str(c.category_id), c.name)
            for c in ShoppingCategory.objects.all()
        ]
        self.fields["category"].choices = category_choices

    category = forms.ChoiceField(
        label="カテゴリ:",
        required=False,
    )
    keyword = forms.CharField(
        label="キーワード:",
        max_length=128,
        required=False,
    )

# ──────────────────────────────────────
# 購入用フォーム
# ──────────────────────────────────────
class PurchaseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""

    destination = forms.CharField(label="配送先住所", max_length=256, required=False)

    payment_method = forms.ChoiceField(
        label="精算方法",
        choices=[("cod", "代金引換")],
        initial="cod"
    )
    

class AdminLoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""

    admin_id = forms.CharField(label="管理者ID:", max_length=128)
    password = forms.CharField(
        label="パスワード:",
        max_length=256,
        widget=forms.PasswordInput,
    )
    
    
class ItemForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""

    item_id = forms.IntegerField(
        label="商品ID:",
        min_value=1,
        error_messages={"min_value": "商品IDは1以上で入力してください"},
    )
    name = forms.CharField(label="商品名:", max_length=128)
    manufacturer = forms.CharField(label="メーカー:", max_length=32)
    color = forms.CharField(label="色:", max_length=16)
    price = forms.IntegerField(
        label="価格:",
        min_value=1,
        error_messages={"min_value": "価格は1円以上で入力してください"},
    )
    stock = forms.IntegerField(
        label="在庫数:",
        min_value=0,
        error_messages={"min_value": "在庫数は0以上で入力してください"},
    )
    recommended = forms.BooleanField(label="おすすめ:", required=False)
    category = CategoryChoiceField(
        label="カテゴリ:",
        queryset=ShoppingCategory.objects.all(),
    )
    # ★ 画像フィールド追加
    image = forms.ImageField(
        label="商品画像:",
        required=False,
    )


class ItemEditForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""

    item_id = forms.IntegerField(label="商品ID:", disabled=True)
    name = forms.CharField(label="商品名:", max_length=128)
    manufacturer = forms.CharField(label="メーカー:", max_length=32)
    color = forms.CharField(label="色:", max_length=16)
    price = forms.IntegerField(
        label="価格:",
        min_value=1,
        error_messages={"min_value": "価格は1円以上で入力してください"},
    )
    stock = forms.IntegerField(
        label="在庫数:",
        min_value=0,
        error_messages={"min_value": "在庫数は0以上で入力してください"},
    )
    recommended = forms.BooleanField(label="おすすめ:", required=False)
    category = CategoryChoiceField(
        label="カテゴリ:",
        queryset=ShoppingCategory.objects.all(),
    )
    # ★ 画像フィールド追加
    image = forms.ImageField(
        label="商品画像:",
        required=False,
    )


class PurchaseSearchForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""

    user_id = forms.CharField(label="会員ID:", max_length=128, required=False)
    purchase_id = forms.IntegerField(label="注文ID:", required=False)

    
class ReviewForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""

    rating = forms.ChoiceField(
        label="評価:",
        choices=[(i, f"★{i}") for i in range(1, 6)],
    )
    comment = forms.CharField(
        label="コメント:",
        max_length=500,
        widget=forms.Textarea(attrs={"rows": 3}),
    )