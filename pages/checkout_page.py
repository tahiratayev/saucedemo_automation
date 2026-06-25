class CheckoutStepOneLocators:
    FIRST_NAME    = "[data-test='firstName']"
    LAST_NAME     = "[data-test='lastName']"
    POSTAL_CODE   = "[data-test='postalCode']"
    CONTINUE_BTN  = "[data-test='continue']"
    CANCEL_BTN    = "[data-test='cancel']"
    ERROR_MESSAGE = "[data-test='error']"


class CheckoutStepTwoLocators:
    ITEM_NAMES    = ".inventory_item_name"
    ITEM_PRICES   = ".inventory_item_price"
    SUBTOTAL      = ".summary_subtotal_label"
    TAX           = ".summary_tax_label"
    TOTAL         = ".summary_total_label"
    FINISH_BTN    = "[data-test='finish']"
    CANCEL_BTN    = "[data-test='cancel']"


class CheckoutCompleteLocators:
    HEADER        = ".complete-header"
    TEXT          = ".complete-text"
    BACK_HOME_BTN = "[data-test='back-to-products']"


class CheckoutStepOnePage:
    """Checkout step 1 — customer info form."""

    def __init__(self, page):
        self.page = page

    def is_loaded(self) -> bool:
        return "checkout-step-one" in self.page.url

    def fill_info(self, first_name: str, last_name: str, postal_code: str):
        self.page.fill(CheckoutStepOneLocators.FIRST_NAME, first_name)
        self.page.fill(CheckoutStepOneLocators.LAST_NAME, last_name)
        self.page.fill(CheckoutStepOneLocators.POSTAL_CODE, postal_code)

    def continue_checkout(self):
        self.page.click(CheckoutStepOneLocators.CONTINUE_BTN)

    def cancel(self):
        self.page.click(CheckoutStepOneLocators.CANCEL_BTN)

    def get_error_message(self) -> str:
        return self.page.locator(CheckoutStepOneLocators.ERROR_MESSAGE).inner_text()

    def is_error_visible(self) -> bool:
        return self.page.locator(CheckoutStepOneLocators.ERROR_MESSAGE).is_visible()


class CheckoutStepTwoPage:
    """Checkout step 2 — order overview."""

    def __init__(self, page):
        self.page = page

    def is_loaded(self) -> bool:
        return "checkout-step-two" in self.page.url

    def get_item_names(self) -> list:
        items = self.page.locator(CheckoutStepTwoLocators.ITEM_NAMES).all()
        return [i.inner_text() for i in items]

    def get_subtotal(self) -> float:
        text = self.page.locator(CheckoutStepTwoLocators.SUBTOTAL).inner_text()
        return float(text.split("$")[1])

    def get_tax(self) -> float:
        text = self.page.locator(CheckoutStepTwoLocators.TAX).inner_text()
        return float(text.split("$")[1])

    def get_total(self) -> float:
        text = self.page.locator(CheckoutStepTwoLocators.TOTAL).inner_text()
        return float(text.split("$")[1])

    def finish_order(self):
        self.page.click(CheckoutStepTwoLocators.FINISH_BTN)

    def cancel(self):
        self.page.click(CheckoutStepTwoLocators.CANCEL_BTN)


class CheckoutCompletePage:
    """Checkout step 3 — order confirmation."""

    def __init__(self, page):
        self.page = page

    def is_loaded(self) -> bool:
        return "checkout-complete" in self.page.url

    def get_header(self) -> str:
        return self.page.locator(CheckoutCompleteLocators.HEADER).inner_text()

    def get_confirmation_text(self) -> str:
        return self.page.locator(CheckoutCompleteLocators.TEXT).inner_text()

    def back_to_home(self):
        self.page.click(CheckoutCompleteLocators.BACK_HOME_BTN)
