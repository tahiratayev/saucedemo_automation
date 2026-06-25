Feature: Login functionality
  As a user
  I want to log into SauceDemo
  So that I can access the inventory

  @smoke @login
  Scenario: Successful login with valid credentials
    Given I am on the login page
    When I login with username "standard_user" and password "secret_sauce"
    Then I should be redirected to the inventory page

  @smoke @login
  Scenario: Login fails with invalid password
    Given I am on the login page
    When I login with username "standard_user" and password "wrong_password"
    Then I should see an error message

  @login
  Scenario: Login fails with locked out user
    Given I am on the login page
    When I login with username "locked_out_user" and password "secret_sauce"
    Then I should see an error message

  @login
  Scenario: Login fails with empty credentials
    Given I am on the login page
    When I submit login with empty credentials
    Then I should see an error message
