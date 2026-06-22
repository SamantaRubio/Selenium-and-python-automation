# US-004 - Sort Products

## User Story

As a customer,
I want to sort products,
So that I can organize items according to my preference.

## Acceptance Criteria

### Scenario: Sort A to Z

Given the user is on the inventory page

When the user selects "Name (A to Z)"

Then products should be sorted alphabetically.

### Scenario: Sort Z to A

When the user selects "Name (Z to A)"

Then products should appear in descending order.

### Scenario: Sort Low to High

When the user selects "Price (low to high)"

Then products should be ordered by ascending price.

### Scenario: Sort High to Low

When the user selects "Price (high to low)"

Then products should be ordered by descending price.
