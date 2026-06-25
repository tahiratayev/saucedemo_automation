class InventoryPageLocators:
    PRODUCT_LIST        = ".inventory_list"
    PRODUCT_ITEMS       = ".inventory_item"
    PRODUCT_NAME        = ".inventory_item_name"
    PRODUCT_PRICE       = ".inventory_item_price"
    ADD_TO_CART_BTN     = "button[data-test^='add-to-cart']"
    REMOVE_BTN          = "button[data-test^='remove']"
    CART_BADGE          = ".shopping_cart_badge"
    CART_LINK           = ".shopping_cart_link"
    SORT_DROPDOWN       = "[data-test='product-sort-container']"
    PAGE_TITLE          = ".title"


class InventoryPage:
    """
    Page Object for the SauceDemo inventory/products page.
    Only accessible after successful login.
    """

    def __init__(self, page):
        self.page = page

    def is_loaded(self) -> bool:
        """Confirm inventory page is displayed."""
        return "/inventory.html" in self.page.url

    def get_page_title(self) -> str:
        return self.page.locator(InventoryPageLocators.PAGE_TITLE).inner_text()

    def get_product_count(self) -> int:
        """Return total number of products visible."""
        return self.page.locator(InventoryPageLocators.PRODUCT_ITEMS).count()

    def get_product_names(self) -> list:
        """Return list of all visible product names."""
        items = self.page.locator(InventoryPageLocators.PRODUCT_NAME).all()
        return [item.inner_text() for item in items]

    def get_product_prices(self) -> list:
        """Return list of all visible product prices as floats."""
        items = self.page.locator(InventoryPageLocators.PRODUCT_PRICE).all()
        return [float(item.inner_text().replace("$", "")) for item in items]

    def add_first_item_to_cart(self):
        """Click 'Add to cart' on the first product."""
        self.page.locator(InventoryPageLocators.ADD_TO_CART_BTN).first.click()

    def get_cart_count(self) -> int:
        """Return number shown on cart badge. Returns 0 if badge not visible."""
        badge = self.page.locator(InventoryPageLocators.CART_BADGE)
        if badge.is_visible():
            return int(badge.inner_text())
        return 0

    def sort_by(self, option: str):
        """
        Sort products. Options:
        'az' — Name (A to Z)
        'za' — Name (Z to A)
        'lohi' — Price (low to high)
        'hilo' — Price (high to low)
        """
        self.page.select_option(InventoryPageLocators.SORT_DROPDOWN, option)

    def go_to_cart(self):
        """Click the cart icon."""
        self.page.click(InventoryPageLocators.CART_LINK)
