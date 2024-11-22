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

        // update_items_table(res.items);
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

    // ****************************************
    // Create a Wishlist
    // ****************************************
    $("#create-btn").click(function () {
        console.log("Create button clicked");
        let name = $("#wishlist_name").val();
        let userid = $("#wishlist_userid").val();
        let date_created = $("#wishlist_date").val()


        let data = {
            "name": name,
            "userid": userid,
            "date_created": date_created,
            "items": []
        };

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "POST",
            url: "/wishlists",
            contentType: "application/json",
            data: JSON.stringify(data),
        })

        ajax.done(function(res) {
            console.log("Success response:", res);
            update_wishlist_form(res);
            flash_message("Success");
        })

        ajax.fail(function(res) {
            console.log("Failed response:", res);
            flash_message(res.responseJSON.message);
        });
    });

    // ****************************************
    // Retrieve a Wishlist
    // ****************************************

    $("#retrieve-btn").click(function () {

        let wishlist_id = $("#wishlist_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/wishlists/${wishlist_id}`,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            update_wishlist_form(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            clear_wishlist_form()
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Clear wishlist form
    // ****************************************
    $("#clear-btn").click(function () {
        $("#wishlist_id").val("");
        $("#flash_message").empty();
        clear_wishlist_form()

    });

})
