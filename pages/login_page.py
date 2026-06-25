class LoginPageLocators:
    """
    All locators in one place.
    If the UI changes, you fix it here — not in 20 test files.
    """
    USERNAME_INPUT = "#user-name"
    PASSWORD_INPUT = "#password"
    LOGIN_BUTTON   = "#login-button"
    ERROR_MESSAGE  = "[data-test='error']"


class LoginPage:
    """
    Page Object for the SauceDemo login page.
    Tests interact with this class — never with raw selectors.
    """

    def __init__(self, page, base_url: str):
        self.page = page
        self.base_url = base_url

    def navigate(self):
        """Go to the login page."""
        self.page.goto(self.base_url)

    def enter_username(self, username: str):
        self.page.fill(LoginPageLocators.USERNAME_INPUT, username)

    def enter_password(self, password: str):
        self.page.fill(LoginPageLocators.PASSWORD_INPUT, password)

    def click_login(self):
        self.page.click(LoginPageLocators.LOGIN_BUTTON)

    def login(self, username: str, password: str):
        """Full login flow — convenience method for happy path."""
        self.navigate()
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()

    def get_error_message(self) -> str:
        """Return the error message text if visible."""
        return self.page.locator(LoginPageLocators.ERROR_MESSAGE).inner_text()

    def is_error_displayed(self) -> bool:
        """Check if an error message is currently visible."""
        return self.page.locator(LoginPageLocators.ERROR_MESSAGE).is_visible()

    def is_on_inventory_page(self) -> bool:
        """Confirm successful login by checking URL."""
        return "/inventory.html" in self.page.url
