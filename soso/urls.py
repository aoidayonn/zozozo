from django.urls import path
from . import views

app_name = "soso"

urlpatterns = [
    path("main/", views.TopPage.as_view(), name="top_page"),
    path("login/", views.UserLogin.as_view(), name="user_login"),
    path("registerUser/", views.UserCreate.as_view(), name="user_create"),
    path("registerUserConfirm/", views.UserCreateConfirm.as_view(), name="user_confirm"),
    path("userInfo/", views.UserInfo.as_view(), name="user_info"),
    path("logout/", views.UserLogout.as_view(), name="user_logout"),
    path("updateUser/", views.UserUpdate.as_view(), name="user_update"),
    path("updateUserConfirm/", views.UserUpdateConfirm.as_view(), name="user_update_confirm"),
    path("withdrawConfirm/", views.UserWithdrawConfirm.as_view(), name="user_withdraw_confirm"),
    path("withdrawCommit/", views.UserWithdrawCommit.as_view(), name="user_withdraw_commit"),
    path("searchResult/", views.SearchResult.as_view(), name="search_result"),
    path("itemDetail/<int:item_id>/", views.ItemDetail.as_view(), name="item_detail"),
    path("cart/", views.ShoppingCart.as_view(), name="shopping_cart"),
    path("cart/update/<int:cart_id>/", views.ShoppingCartUpdate.as_view(), name="cart_update"),
    path("cart/delete/<int:cart_id>/", views.ShoppingCartDelete.as_view(), name="cart_delete"),
    path("purchase/", views.Purchase.as_view(), name="purchase"),
    path("purchase/confirm/", views.PurchaseConfirm.as_view(), name="purchase_confirm"),
    path("purchase/commit/", views.PurchaseCommit.as_view(), name="purchase_commit"),
    path("purchaseHistory/", views.UserPurchaseHistory.as_view(), name="user_purchase_history"),
    path("purchaseHistory/<int:purchase_id>/", views.UserPurchaseDetail.as_view(), name="user_purchase_detail"),


    # ★ 管理者用
    path("adminLogin/", views.AdminLogin.as_view(), name="admin_login"),
    path("adminMain/", views.AdminTopPage.as_view(), name="admin_top"),
    path("adminLogout/", views.AdminLogout.as_view(), name="admin_logout"),

    # 商品管理
    path("adminItemList/", views.AdminItemList.as_view(), name="admin_item_list"),
    path("adminItemCreate/", views.AdminItemCreate.as_view(), name="admin_item_create"),
    path("adminItemEdit/<int:item_id>/", views.AdminItemEdit.as_view(), name="admin_item_edit"),
    path("adminItemDelete/<int:item_id>/", views.AdminItemDelete.as_view(), name="admin_item_delete"),

    # おすすめ管理
    path("adminRecommend/", views.AdminRecommend.as_view(), name="admin_recommend"),

    # 購入履歴・キャンセル
    path("adminPurchaseSearch/", views.AdminPurchaseSearch.as_view(), name="admin_purchase_search"),
    path("adminPurchaseDetail/<int:purchase_id>/", views.AdminPurchaseDetail.as_view(), name="admin_purchase_detail"),
    path("adminPurchaseCancel/<int:purchase_id>/", views.AdminPurchaseCancel.as_view(), name="admin_purchase_cancel"),

    path("review/<int:item_id>/", views.ReviewCreate.as_view(), name="review_create"),
    path("reviews/", views.ReviewTimeline.as_view(), name="review_timeline"),
    
    path("tetris/", views.NekoTetris.as_view(), name="neko_tetris"),
    path("vs/", views.TetrisLobby.as_view(), name="tetris_lobby"),
    path("vs/<str:room_name>/", views.TetrisVs.as_view(), name="tetris_vs"),
    path("gacha/", views.GachaPage.as_view(), name="gacha_page"),
    path("gachaDraw/", views.GachaDraw.as_view(), name="gacha_draw"),
    path("myCoupons/", views.MyCoupons.as_view(), name="my_coupons"),

    # ★ 追加：テトリスポイントガチャ
    path("tetris/win/", views.TetrisWin.as_view(), name="tetris_win"),
    path("tetrisGacha/", views.TetrisGachaPage.as_view(), name="tetris_gacha_page"),
    path("tetrisGachaDraw/", views.TetrisGachaDraw.as_view(), name="tetris_gacha_draw"),
]
