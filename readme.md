# PlurkAPI

官方的有點難用，也懶得丟PR自己寫一個順便摸一摸比較實際呢。

# 驗證 (Oauth)
Plurk用了比較弱的Oauth1，所以很簡單的使用[oauth](https://github.com/joestump/python-oauth2)，然後發請求的部分我習慣使用[requests](https://github.com/kennethreitz/requests)。

# 使用
依照[API](https://www.plurk.com/API)指示。
```python
plurk = user(app_key, app_secret)
plurk.authorize() # 依照指示流程（？）
print(plruk.me())
>>> {'verified_account': False, 'avatar_small': 'https://avatars.plurk.com/999999-small999999.gif', 'anniversary': {'days': 99, 'years': 99}, 'badges': ['9', '1000_views', '1000_plurks', '500_comments', 'upload_profile_image'], 'fans_count': 0, 'profile_views': 99, 'display_name': '踢低吸@睡眠補充'.....
```