Feature: Checkout flow
  As a logged in user
  I want to complete a purchase
  So that I can buy products from SauceDemo

  Background:
    Given I am logged in and have added a product to the cart
    And I am on the cart page

  @smoke @checkout
  Scenario: Complete a full checkout successfully
    When I proceed to checkout
    And I fill in my details with first name "John" last name "Doe" and postal code "12345"
    And I continue to order overview
    And I finish the order
    Then I should see the order confirmation page
    And the confirmation header should say "Thank you for your order!"

  @checkout
  Scenario: Checkout fails with missing first name
    When I proceed to checkout
    And I submit checkout info with empty first name
    Then I should see a checkout error message

  @checkout
  Scenario: Checkout fails with missing last name
    When I proceed to checkout
    And I submit checkout info with empty last name
    Then I should see a checkout error message

  @checkout
  Scenario: Checkout fails with missing postal code
    When I proceed to checkout
    And I submit checkout info with empty postal code
    Then I should see a checkout error message

  @checkout
  Scenario: Order total matches subtotal plus tax
    When I proceed to checkout
    And I fill in my details with first name "Jane" last name "Smith" and postal code "99999"
    And I continue to order overview
    Then the order total should equal subtotal plus tax

  @checkout
  Scenario: Cancel checkout returns to cart
    When I proceed to checkout
    And I cancel checkout
    Then I should be back on the cart page
