# US-002 - Invalid Login

## User Story

As a customer,
I want to receive an error message when I use invalid credentials,
So that I know my login attempt failed.

## Priority

High

## Acceptance Criteria

### Scenario: Invalid Login

Given the user is on the Login page

When the user enters an invalid username

And enters an invalid password

And clicks Login

Then an error message should be displayed

And the user should remain on the Login page

## Expected Result

Authentication fails and an error message is shown.
