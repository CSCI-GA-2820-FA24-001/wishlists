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
        // // Update items table
        // update_items_table(res.items);
    }

    function update_item_form(res) {
        $("#wishlist_item_id").val(res.id);
        $("#wishlist_item_name").val(res.name);
        $("#wishlist_item_wishlist").val(res.wishlist_id);
        $("#wishlist_item_description").val(res.description);
        $("#wishlist_item_price").val(res.price);
        $("#wishlist_item_status").val(res.status);
    }

    /// Clears all form fields
    function clear_wishlist_form() {
        $("#wishlist_id").val("");
        $("#wishlist_name").val("");
        $("#wishlist_userid").val("");
        $("#wishlist_date").val("");
        $("#list_items tbody").empty();
    }

    function clear_item_form() {
        $("#wishlist_item_id").val("");
        $("#wishlist_item_name").val("");
        $("#wishlist_item_wishlist").val("");
        $("#wishlist_item_description").val("");
        $("#wishlist_item_price").val("");
        $("#wishlist_item_status").val("");
    }

    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").empty();
        $("#flash_message").append(message);
        $("#flash_message").show();
    }

    // ****************************************
    // Clear wishlist and item form
    // ****************************************
    $("#clear-btn").click(function () {
        $("#flash_message").empty();
        clear_wishlist_form()

    });
    
    $("#clear-item-btn").click(function () {
        $("#flash_message").empty();
        clear_item_form()

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

        ajax.done(function(res) {
            console.log("Success response:", res);
            update_wishlist_form(res);
            flash_message("Wishlist Creation is Successful");
            console.log("Verification - Flash message is:", $("#flash_message").text());
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
        console.log("Retrieve button clicked");
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
    // Delete a Wishlist
    // ****************************************
    $("#delete-btn").click(function () {
        console.log("Delete button clicked");
        let wishlist_id = $("#wishlist_id").val();

        $.ajax({
            type: "DELETE",
            url: `/wishlists/${wishlist_id}`,
            contentType: "application/json"
        })
        .done(function() {
            clear_wishlist_form();
            flash_message("Wishlist Deletion is Successful");
        })
        .fail(function() {
            flash_message(res.responseJSON.message);
        });
    });


    // ****************************************
    // Add an Item to a Wishlist
    // ****************************************
    $("#add_item-btn").click(function () {
        console.log("Add item button clicked");
        let wishlist_id = $("#wishlist_item_wishlist").val();
        let name = $("#wishlist_item_name").val();
        let description = $("#wishlist_item_description").val();
        let price = $("#wishlist_item_price").val();
        let status = $("#wishlist_item_status").val();

        let data = {
            "name": name,
            "wishlist_id": wishlist_id,
            "description": description,
            "price": parseFloat(price),
            "status": status
        };

        $("#flash_message").empty();
        
        let ajax = $.ajax({
            type: "POST",
            url: `/wishlists/${wishlist_id}/items`,
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function(res){
            update_item_form(res);
            flash_message("Item Added Successfully");
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message);
        });
    });


    // ****************************************
    // Update an Item
    // ****************************************
    $("#update_item-btn").click(function () {
        console.log("Update item button clicked");
        let wishlist_id = $("#wishlist_item_wishlist").val();
        let wishlist_item_id = $("#wishlist_item_id").val();
        let name = $("#wishlist_item_name").val();
        let description = $("#wishlist_item_description").val();
        let price = $("#wishlist_item_price").val();
        let status = $("#wishlist_item_status").val();

        let data = {
            "name": name,
            "wishlist_id": wishlist_id,
            "description": description,
            "price": parseFloat(price),
            "status": status
        };

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "PUT",
            url: `/wishlists/${wishlist_id}/items/${wishlist_item_id}`,
            contentType: "application/json",
            data: JSON.stringify(data)
        });

        ajax.done(function(res){
            update_item_form(res);
            flash_message("Item Updated Successfully");
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message);
        });
    });


    // ****************************************
    // Delete an Item
    // ****************************************
    $("#delete_item-btn").click(function () {
        console.log("Delete item button clicked");
        let wishlist_id = $("#wishlist_item_wishlist").val();
        let wishlist_item_id = $("#wishlist_item_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "DELETE",
            url: `/wishlists/${wishlist_id}/items/${wishlist_item_id}`,
            contentType: "application/json",
        });

        ajax.done(function(res){
            clear_item_form();
            flash_message("Item has been Deleted!");
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message);
        });
    });


    // ****************************************
    // Retrieve an Item
    // ****************************************
    $("#retrieve_item-btn").click(function () {
        console.log("Retrieve item button clicked");
        let wishlist_id = $("#wishlist_item_wishlist").val();
        let wishlist_item_id = $("#wishlist_item_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/wishlists/${wishlist_id}/items/${wishlist_item_id}`,
            contentType: "application/json",
        });

        ajax.done(function(res){
            update_item_form(res);
            flash_message("Success");
        });

        ajax.fail(function(res){
            clear_item_form();
            flash_message(res.responseJSON.message);
        });
    });

    
    // ****************************************
    // List all Items in a Wishlist
    // ****************************************
    $("#list_item-btn").click(function () {
        let wishlist_id = $("#wishlist_id").val();
        
        $("#flash_message").empty();
        
        let ajax = $.ajax({
            type: "GET",
            url: `/wishlists/${wishlist_id}/items`,
            contentType: "application/json",
        });

        ajax.done(function(res){
            $("#list_items").empty();
            let table = '<table class="table table-striped" cellpadding="10">';
            table += '<thead><tr>';
            table += '<th class="col-md-2">ID</th>';
            table += '<th class="col-md-2">Name</th>';
            table += '<th class="col-md-2">Wishlist ID</th>';
            table += '<th class="col-md-2">Description</th>';
            table += '<th class="col-md-2">Price</th>';
            table += '<th class="col-md-2">Status</th>';
            table += '<th class="col-md-2">Actions</th>';
            table += '</tr></thead><tbody>';
            
            let firstItem = "";
            for (let i = 0; i < res.length; i++) {
                let item = res[i];
                table += `<tr id="row_${i}"><td>${item.id}</td>`;
                table += `<td>${item.name}</td>`;
                table += `<td>${item.wishlist_id}</td>`;
                table += `<td>${item.description}</td>`;
                table += `<td>$${item.price.toFixed(2)}</td>`;
                table += `<td>${item.status}</td>`;
                table += `<td><button class="btn btn-info" data-id="${item.id}">View</button></td></tr>`;
                if (i == 0) {
                    firstItem = item;
                }
            }
            table += '</tbody></table>';
            $("#list_items").append(table);

            if (firstItem != "") {
                update_item_form(firstItem);
            }

            flash_message("Success");
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message);
        });
    });

})
