Feature: Flight Booking on Aviasales
  As a user
  I want to search and book flights
  So that I can plan my travel

  Scenario: Search for available flights
    Given I am on the Aviasales homepage
    When I disable the Booking.com checkbox
    And I enter "Астана" as departure city
    And I enter "Уральск" as destination city
    And I select departure date "28.02.2025"
    And I click the search button
    Then I should see available flight options

  Scenario: Select and proceed with flight booking
    Given I am on the Aviasales homepage
    When I search for flights from "Астана" to "Уральск" on "28.02.2025"
    And I select the first available flight
    And I click the buy button
    And I switch to the booking page
    Then the booking page should load successfully

  Scenario: Complete passenger information form
    Given I have navigated to a flight booking form
    When I fill in contact email "23232323@astanait.edu.kz"
    And I fill in contact phone "7787296919"
    And I fill in passenger first name "Meruyert"
    And I fill in passenger last name "Boranbay"
    And I select gender as "Female"
    And I fill in date of birth as "02/07/2005"
    And I fill in passport number "123456798"
    And I fill in passport expiration date as "12/12/2030"
    And I select nationality "Казахстан"
    And I select "Comfort" package
    Then the booking form should be completed successfully
