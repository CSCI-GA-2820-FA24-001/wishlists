Feature: The wishlist service back-end
    As a Store Manager
    I need a RESTful wishlist service
    So that I can manage customer wishlists

Background:
    Given the following wishlists
        | name           | userid    | date_created |
        | Birthday List  | user123   | 2024-11-13   |
        | Holiday List   | user123   | 2024-03-02   |
        | Christmas List | user456   | 2024-12-01   |
        | Shopping List  | user789   | 2024-08-22   |
    And the following items in "Birthday List" 
        | name          | description            | price    | status    |
        | iPhone        | iPhone Latest model    | 999.99   | pending   |
        | AirPods       | AirPods Pro 2nd gen    | 199.00   | purchased |
        
Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Wishlist Demo RESTful Service" in the title
    And I should not see "404 Not Found"

Scenario: Create a Wishlist
    When I visit the "Home Page"
    And I set the "Name" to "Gift List"
    And I set the "UserId" to "user987"
    And I set the "Date" to "01-01-2024"
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    Then the "Id" field should be empty
    And the "Name" field should be empty
    And the "UserId" field should be empty
    When I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "Gift List" in the "Name" field
    And I should see "user987" in the "UserId" field
    And I should see "2024-01-01" in the "Date" field

Scenario: Delete a Wishlist
    When I visit the "Home Page"
    And I set the "Name" to "Gift List"
    And I set the "UserId" to "user987"
    And I set the "Date" to "01-01-2024"
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    When I paste the "Id" field
    And I press the "Delete" button
    Then I should see the message "Success"
    # And I set the "Name" to "Birthday List"
    # And I press the "Search" button
    # Then I should see the message "Not Found"

Scenario: Create a Wishlist and Add Item
    When I visit the "Home Page"
    And I set the "Name" to "Gaming Wishlist"
    And I set the "UserID" to "gamer123"
    And I set the "Date" to "12-25-2024"
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    
    # Add an item to the newly created wishlist
    When I paste the "Wishlist ID" 
    And I set the "Item Name" to "PS5"
    And I set the "Item Description" to "PlayStation 5 Console"
    And I set the "Item Price" to "499.99"
    And I set the "Item Status" to "pending"
    And I press the "Add Item" button
    Then I should see the message "Item Added Successfully"
    
    # # Verify wishlist contains the item
    # When I press the "List Items" button
    # Then I should see "PS5" in the results
    # And I should see "PlayStation 5 Console" in the results
    # And I should see "499.99" in the results
    # And I should see "pending" in the results
    
    # # Verify original wishlist data persists
    # When I press the "Retrieve" button
    # Then I should see "Gaming Wishlist" in the "Name" field
    # And I should see "gamer123" in the "UserID" field
    # And I should see "2024-12-25" in the "Date" field