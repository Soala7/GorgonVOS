from boot.login_screen import LoginScreen

def main():

    login = LoginScreen()

    login.select_user("Soala")

    login.set_username("Soala")

    login.set_password("1234")

    assert login.login()

    assert login.logged_in

    login.logout()

    assert not login.logged_in

    print("LoginScreen tests passed.")

if __name__ == "__main__":
    main()
