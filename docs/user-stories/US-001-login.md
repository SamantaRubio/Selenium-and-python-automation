# US-001 - Successful Login

## User Story

As a customer,
I want to log into SauceDemo with valid credentials,
So that I can access the products page.

## Priority

High

## Preconditions

* User is on the Login page.
* User has valid credentials:

  * username: standard_user
  * password: secret_sauce

## Acceptance Criteria

### Scenario: Successful Login

Given the user is on the Login page

When the user enters a valid username

And enters a valid password

And clicks the Login button

Then the Products page should be displayed

And the inventory list should be visible

And the URL should contain "/inventory.html"

## Expected Result

User is successfully authenticated and redirected to the inventory page.
