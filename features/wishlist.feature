Feature: The wishlist service back-end
    As a Store Manager
    I need a RESTful wishlist service
    So that I can manage customer wishlists

Background:
    Given the following wishlists
        | name           | userid    | date_created |
        | Birthday List  | user123   | 2024-11-13  |
        | Holiday List   | user123   | 2024-03-02  |
        | Christmas List | user456   | 2024-12-01  |
        | Shopping List  | user789   | 2024-08-22  |
    And the following items in "Birthday List" 
        | name          | description            | price    | status    |
        | iPhone        | iPhone Latest model    | 999.99   | pending   |
        | AirPods       | AirPods Pro 2nd gen    | 199.00   | purchased |
        
Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Wishlist Admin Service" in the title
    And I should not see "404 Not Found"