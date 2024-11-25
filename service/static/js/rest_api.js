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
        $("#flash_message").show();
    }

    // ****************************************
    // Clear wishlist form
    // ****************************************
    $("#clear-btn").click(function () {
        $("#wishlist_id").val("");
        $("#flash_message").empty();
        clear_wishlist_form()

    });

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

        ajax.done(function (res) {
            console.log("Success response:", res);
            update_wishlist_form(res);
            flash_message("Wishlist Creation is Successful");
            console.log("Verification - Flash message is:", $("#flash_message").text());
        })

        ajax.fail(function (res) {
            console.log("Failed response:", res);
            flash_message(res.responseJSON.message);
        });
    });

    // ****************************************
    // Update a Wishlist
    // ****************************************
    $("#update-btn").click(function () {
        let wishlist_id = $("#wishlist_id").val();
        let name = $("#wishlist_name").val();
        let userid = $("#wishlist_userid").val();
        let date_created = $("#wishlist_date").val();

        let data = {
            "name": name,
            "userid": userid,
            "date_created": date_created,
            "items": []
        };

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "PUT",
            url: `/wishlists/${wishlist_id}`,
            contentType: "application/json",
            data: JSON.stringify(data)
        })

        ajax.done(function (res) {
            update_wishlist_form(res)
            flash_message("Success")
        });

        ajax.fail(function (res) {
            flash_message(res.responseJSON.message)
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

        ajax.done(function (res) {
            //alert(res.toSource())
            update_wishlist_form(res)
            flash_message("Success")
        });

        ajax.fail(function (res) {
            clear_wishlist_form()
            flash_message(res.responseJSON.message)
        });

    });


    // ****************************************
    // Delete a Wishlist
    // ****************************************
    $("#delete-btn").click(function () {
        let wishlist_id = $("#wishlist_id").val();

        $.ajax({
            type: "DELETE",
            url: `/wishlists/${wishlist_id}`,
            contentType: "application/json"
        })
            .done(function () {
                clear_wishlist_form();
                flash_message("Wishlist Deletion is Successful");
            })
            .fail(function () {
                flash_message(res.responseJSON.message);
            });
    });


    // ****************************************
    // Query a Wishlist
    // ****************************************

    $("#search-btn").click(function () {

        let wishlist_name = $("#wishlist_name").val();
        let wishlist_userid = $("#wishlist_userid").val();
        let wishlist_date = $("#wishlist_date").val();

        let queryString = ""

        if (wishlist_name) {
            queryString += 'name=' + wishlist_name
        }
        if (wishlist_userid) {
            if (queryString.length > 0) {
                queryString += '&userid=' + wishlist_userid
            } else {
                queryString += 'userid=' + wishlist_userid
            }
        }
        if (wishlist_date) {
            if (queryString.length > 0) {
                queryString += '&date_created=' + wishlist_date
            } else {
                queryString += 'date_created=' + wishlist_date
            }
        }

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/wishlists?${queryString}`,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function (res) {
            $("#search_results").empty();
            let table = '<table class="table table-striped" cellpadding="10">'
            table += '<thead><tr>'
            table += '<th class="col-md-1">ID</th>'
            table += '<th class="col-md-3">Name</th>'
            table += '<th class="col-md-2">User ID</th>'
            table += '<th class="col-md-2">Date Created</th>'
            table += '<th class="col-md-2">Actions</th>'
            table += '</tr></thead><tbody>'
            for (let i = 0; i < res.length; i++) {
                let wishlist = res[i];
                table += `<tr id="row_${i}"><td>${wishlist.id}</td><td>${wishlist.name}</td><td>${wishlist.userid}</td><td>${wishlist.date_created}</td><td>"placeholder"</td></tr>`;
            }
            table += '</tbody></table>';
            $("#search_results").append(table);
            flash_message("Success")
        });

        ajax.fail(function (res) {
            clear_wishlist_form()
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // List all Wishlists
    // ****************************************

    $("#list_all_wishlists-btn").click(function () {

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/wishlists`,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function (res) {
            //alert(res.toSource())
            $("#search_results").empty();
            let table = '<table class="table table-striped" cellpadding="10">'
            table += '<thead><tr>'
            table += '<th class="col-md-1">ID</th>'
            table += '<th class="col-md-3">Name</th>'
            table += '<th class="col-md-2">User ID<</th>'
            table += '<th class="col-md-2">Date Created</th>'
            table += '<th class="col-md-2">Actions</th>'
            table += '</tr></thead><tbody>'
            // let firstWishlist= "";
            for (let i = 0; i < res.length; i++) {
                let wishlist = res[i];
                table += `<tr id="row_${i}"><td>${wishlist.id}</td><td>${wishlist.name}</td><td>${wishlist.userid}</td><td>${wishlist.date_created}</td><td>"placeholder"</td></tr>`;
                // if (i == 0) {
                //     firstWishlist = wishlist;
                // }
            }
            table += '</tbody></table>';
            $("#search_results").append(table);

            // copy the first result to the form
            // if (firstWishlist != "") {
            //     update_wishlist_form(firstWishlist)
            // }
            flash_message("Success")
        });

        ajax.fail(function (res) {
            clear_wishlist_form()
            flash_message(res.responseJSON.message)
        });

    });




})
