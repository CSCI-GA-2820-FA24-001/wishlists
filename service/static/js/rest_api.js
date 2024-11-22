$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************


    // ****************************************
    // Create a Wishlist
    // ****************************************
    $("#create-btn").click(function () {
        let name = $("#wishlist_name").val();
        let userid = $("#wishlist_userid").val();
        let date_created = $("#date_created").val()

        let data = {
            "name": name,
            "userid": userid,
            "date_created": date_created,
            "items": []
        };

        let ajax = $.ajax({
            type: "POST",
            url: "/wishlists",
            contentType: "application/json",
            data: JSON.stringify(data),
        })

        ajax.done(function(res) {
            update_wishlist_form(res);
            flash_message("Wishlist Creation Success");
        })

        ajax.fail(function(res) {
            flash_message(res.responseJSON.message);
        });
    });


    // ****************************************
    // Create a Wishlist
    // ****************************************
    $("#create-btn").click(function () {
        let name = $("#wishlist_name").val();
        let userid = $("#wishlist_userid").val();
        let date_create = $("#wishlist_date").val()

        let data = {
            "name": name,
            "userid": userid,
            "date_created": date_create,
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
            update_wishlist_form(res);
            flash_message("Wishlist has been Created!");
        })
        
        ajax.fail(function(res) {
            flash_message(res.responseJSON.message);
        });
    });

})
