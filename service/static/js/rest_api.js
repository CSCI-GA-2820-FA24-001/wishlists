$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_wishlist_form(res) {
        $("#wishlist_id").val(res.id);
        $("#wishlist_name").val(res.name);
        $("#wishlist_userid").val(res.userid);
        $("#wishlist_date").val(res.date_created);
        // Update items table
        update_items_table(res.items);
    }

    function update_item_form(res) {
        $("#item_id").val(res.id);
        $("#item_name").val(res.name);
        $("#item_description").val(res.description);
        $("#item_price").val(res.price);
        $("#item_status").val(res.status);
    }

    /// Clears all form fields
    function clear_wishlist_form() {
        $("#wishlist_id").val("");
        $("#wishlist_name").val("");
        $("#wishlist_userid").val("");
        $("#wishlist_date").val("");
        $("#items_list tbody").empty();
    }

    function clear_item_form() {
        $("#item_id").val("");
        $("#item_name").val("");
        $("#item_description").val("");
        $("#item_price").val("");
        $("#item_status").val("pending");
    }

    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").empty();
        $("#flash_message").append(message);
    }
})
