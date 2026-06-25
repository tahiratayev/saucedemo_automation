Feature: Inventory page functionality
  As a logged in user
  I want to browse and interact with the product inventory
  So that I can find and add products to my cart

  Background:
    Given I am logged in as a standard user

  @smoke @inventory
  Scenario: Inventory page loads with products
    Then I should see the inventory page
    And the page should display 6 products

  @smoke @inventory
  Scenario: Add product to cart
    When I add the first product to the cart
    Then the cart badge should show 1

  @inventory
  Scenario: Sort products by price low to high
    When I sort products by price low to high
    Then products should be sorted by ascending price

  @inventory
  Scenario: Sort products by name Z to A
    When I sort products by name Z to A
    Then products should be sorted in reverse alphabetical order
