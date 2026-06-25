class CartPageLocators:
    CART_ITEMS        = ".cart_item"
    ITEM_NAME         = ".inventory_item_name"
    ITEM_PRICE        = ".inventory_item_price"
    ITEM_QUANTITY     = ".cart_quantity"
    REMOVE_BTN        = "button[data-test^='remove']"
    CONTINUE_SHOPPING = "[data-test='continue-shopping']"
    CHECKOUT_BTN      = "[data-test='checkout']"
    CART_TITLE        = ".title"


class CartPage:
    """Page Object for the SauceDemo cart page."""

    def __init__(self, page):
        self.page = page

    def is_loaded(self) -> bool:
        return "/cart.html" in self.page.url

    def get_item_count(self) -> int:
        return self.page.locator(CartPageLocators.CART_ITEMS).count()

    def get_item_names(self) -> list:
        items = self.page.locator(CartPageLocators.ITEM_NAME).all()
        return [i.inner_text() for i in items]

    def get_item_prices(self) -> list:
        items = self.page.locator(CartPageLocators.ITEM_PRICE).all()
        return [float(i.inner_text().replace("$", "")) for i in items]

    def remove_item(self, index: int = 0):
        """Remove item by position (default: first item)."""
        btns = self.page.locator(CartPageLocators.REMOVE_BTN).all()
        btns[index].click()

    def proceed_to_checkout(self):
        self.page.click(CartPageLocators.CHECKOUT_BTN)

    def continue_shopping(self):
        self.page.click(CartPageLocators.CONTINUE_SHOPPING)
