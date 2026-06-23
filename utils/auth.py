import keyring
import utils.firebase_app as fb

auth = fb.auth
user_id = None
id_token = None
_refresh_token = None
email = None

def save_tokens(new_refresh_token, new_id_token):
    global id_token, _refresh_token

    try:
        keyring.set_password("TypeRighter", "current_user_refresh_token", new_refresh_token)
        _refresh_token = new_refresh_token
        id_token = new_id_token
        return True, None
    except Exception as e:
        return False, e

def get_id_token():
    if not id_token:
        # Get new id_token with refresh token
        id_token, e = _get_new_token()
        if id_token:
            return id_token, None
        else:
            return False, e
    elif id_token:
        # If an id_token already exists, just return it
        return id_token, None

def get_email():
    if email:
        return email, None
    elif not email:
        id_token, e = _get_new_token()
        if id_token:
            return email, None
        else:
            return False, e

def _get_new_token():
    global _refresh_token, email, user_id

    if _refresh_token:
        # Get the new refresh and id tokens and save them
        try:
            fresh_tokens = auth.refresh(_refresh_token)
            user_id = fresh_tokens["userId"]
            account_info = auth.get_account_info(fresh_tokens["idToken"])["users"][0]
            email = account_info["email"]
        except Exception as e:
            return False, e
        save_tokens(fresh_tokens["refreshToken"], fresh_tokens["idToken"])

        return fresh_tokens["idToken"], None
    else:
        # Get the previous refresh token with keyring
        _refresh_token = keyring.get_password("TypeRighter", "current_user_refresh_token")
        
        if _refresh_token:
            # Now Get the new refresh and id tokens and save them
            try:
                fresh_tokens = auth.refresh(_refresh_token)
                user_id = fresh_tokens["userId"]
                account_info = auth.get_account_info(fresh_tokens["idToken"])["users"][0]
                email = account_info["email"]
            except Exception as e:
                return False, e
            save_tokens(fresh_tokens["refreshToken"], fresh_tokens["idToken"])

            return fresh_tokens["idToken"], None
        else:
            return False, "No Refresh Token Found"

def login(new_id_token, new_refresh_token, new_email, new_user_id):
    global id_token, _refresh_token, email, user_id

    status, e = save_tokens(new_refresh_token, new_id_token)
    if status:
        email = new_email
        user_id = new_user_id
        return True, None
    else:
        return False, e

def logout():
    global id_token, _refresh_token, email, user_id

    # Clear all the login states

    if id_token:
        id_token = None
    
    if _refresh_token:
        _refresh_token = None

    if email:
        email = None
    
    if user_id:
        user_id = None

    try:
        _refresh_token = keyring.delete_password("TypeRighter", "current_user_refresh_token")
    except Exception as e:
        print(e)