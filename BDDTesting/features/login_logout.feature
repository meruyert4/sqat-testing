Feature: Reddit Login and Logout
  As a Reddit user
  I want to login and logout
  So that I can access my account securely

  Scenario: Successful login to Reddit
    Given I am on the Reddit login page
    When I enter my username
    And I enter my password
    And I click the login button
    Then I should be logged in successfully
    And I should be redirected away from the login page

  Scenario: Successful logout from Reddit
    Given I am logged in to Reddit
    When I navigate to the logout page
    Then I should be logged out successfully
    And I should be on the Reddit homepage
