Feature: User Authentication on Swag Labs
  As a registered user
  I want to log in to the Swag Labs application
  So that I can access the product catalog and place orders

  Background:
    Given the user is on the Swag Labs login page

  @smoke
  Scenario: Successful login with valid credentials
    When the user enters username "standard_user"
    And the user enters password "secret_sauce"
    And the user clicks the login button
    Then the user should be redirected to the products page

  Scenario: Failed login with invalid password
    When the user enters username "standard_user"
    And the user enters password "wrong_password"
    And the user clicks the login button
    Then an error message should be displayed indicating incorrect credentials

  Scenario: Failed login with invalid username
    When the user enters username "unknown_user"
    And the user enters password "secret_sauce"
    And the user clicks the login button
    Then an error message should be displayed indicating incorrect credentials

  Scenario: Failed login with empty credentials
    When the user clicks the login button
    Then an error message should be displayed requiring a username

  Scenario: Failed login with empty password
    When the user enters username "standard_user"
    And the user clicks the login button
    Then an error message should be displayed requiring a password

  Scenario: Login attempt with a locked out user account
    When the user enters username "locked_out_user"
    And the user enters password "secret_sauce"
    And the user clicks the login button
    Then an error message should be displayed indicating the account is locked
