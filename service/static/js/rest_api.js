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
    }

    function update_item_form(res) {
        $("#wishlist_item_id").val(res.id);
        $("#wishlist_item_name").val(res.name);
        $("#wishlist_item_parent").val(res.wishlist_id);
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
        $("#wishlist_item_parent").val("");
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
    
    $("#clear_item-btn").click(function () {
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
        console.log("Update button clicked")
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
        console.log("Retrieve button clicked");
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
            flash_message("Retrieve Wishlist Success")
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
        console.log("Delete button clicked");
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
        console.log("Search button clicked")

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
                table += `<tr id="row_${i}">
                    <td>${wishlist.id}</td>
                    <td>${wishlist.name}</td>
                    <td>${wishlist.userid}</td>
                    <td>${wishlist.date_created}</td>
                    <td>
                        <button class="btn btn-info view-wishlist" data-id="${wishlist.id}">View</button>
                    </td>
                </tr>`;
                
                // Fill the form with the first matching wishlist
                if (i === 0) {
                    update_wishlist_form(wishlist);
                }
            }
            table += '</tbody></table>';
            $("#search_results").append(table);
        
            // Add view functionality
            $(".view-wishlist").off("click").on("click", function () {
                let wishlistId = $(this).data("id");
                console.log(`View clicked for wishlist ID: ${wishlistId}`);
        
                let ajax = $.ajax({
                    type: "GET",
                    url: `/wishlists/${wishlistId}`,
                    contentType: "application/json",
                })
                
                ajax.done(function (res) {
                    console.log("View wishlist response:", res);
                    update_wishlist_form(res);
                    $("#list_items-btn").click(); 
                    flash_message("View Wishlist Success");
                })
                
                ajax.fail(function(res){
                    console.error("View wishlist failed:", res);
                    flash_message(res.responseJSON.message);
                });
            });
        
            flash_message("Success")
        });

        ajax.fail(function (res) {
            clear_wishlist_form()
            flash_message(res.responseJSON.message)
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
                table += `<tr id="row_${i}">
                    <td>${wishlist.id}</td>
                    <td>${wishlist.name}</td>
                    <td>${wishlist.userid}</td>
                    <td>${wishlist.date_created}</td>
                    <td>
                        <button class="btn btn-info view-wishlist" data-id="${wishlist.id}">View</button>
                    </td>
                </tr>`;
            }
            table += '</tbody></table>';
            $("#search_results").append(table);
        
            // Add view functionality
            $(".view-wishlist").off("click").on("click", function () {
                let wishlistId = $(this).data("id");
                console.log(`View clicked for wishlist ID: ${wishlistId}`);
        
                let ajax = $.ajax({
                    type: "GET",
                    url: `/wishlists/${wishlistId}`,
                    contentType: "application/json",
                })
                
                ajax.done(function (res) {
                    console.log("View wishlist response:", res);
                    update_wishlist_form(res);
                    $("#list_items-btn").click(); // Automatically load items
                    flash_message("View Wishlist Success");
                })
                
                ajax.fail(function(res){
                    console.error("View wishlist failed:", res);
                    flash_message(res.responseJSON.message);
                });
            });
        
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
                table += `<tr id="row_${i}">
                    <td>${wishlist.id}</td>
                    <td>${wishlist.name}</td>
                    <td>${wishlist.userid}</td>
                    <td>${wishlist.date_created}</td>
                    <td>
                        <button class="btn btn-info view-wishlist" data-id="${wishlist.id}">View</button>
                    </td>
                </tr>`;
            }
            table += '</tbody></table>';
            $("#search_results").append(table);
        
            // Add view functionality
            $(".view-wishlist").off("click").on("click", function () {
                let wishlistId = $(this).data("id");
                console.log(`View clicked for wishlist ID: ${wishlistId}`);
        
                let ajax = $.ajax({
                    type: "GET",
                    url: `/wishlists/${wishlistId}`,
                    contentType: "application/json",
                })
                
                ajax.done(function (res) {
                    console.log("View wishlist response:", res);
                    update_wishlist_form(res);
                    $("#list_items-btn").click(); // Automatically load items
                    flash_message("View Wishlist Success");
                })
                
                ajax.fail(function(res){
                    console.error("View wishlist failed:", res);
                    flash_message(res.responseJSON.message);
                });
            });
        
            flash_message("Success")
        });

        ajax.fail(function (res) {
            clear_wishlist_form()
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Add an Item to a Wishlist
    // ****************************************
    $("#add_item-btn").click(function () {
        console.log("Add item button clicked");
        let wishlist_id = $("#wishlist_item_parent").val();
        let name = $("#wishlist_item_name").val();
        let description = $("#wishlist_item_description").val();
        let price = $("#wishlist_item_price").val();
        let status = $("#wishlist_item_status").val();
        console.log("Adding item with status:", status);

        let data = {
            "name": name,
            "wishlist_id": wishlist_id,
            "description": description,
            "price": parseFloat(price),
            "status": status || "PENDING"
        };

        console.log("Sending data:", data);
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
        let wishlist_id = $("#wishlist_item_parent").val();
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
        let wishlist_id = $("#wishlist_item_parent").val();
        let wishlist_item_id = $("#wishlist_item_id").val();

        if (!wishlist_id || !wishlist_item_id) {
            flash_message("Please select an item to delete");
            return;
        }

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "DELETE",
            url: `/wishlists/${wishlist_id}/items/${wishlist_item_id}`,
            contentType: "application/json"
        });

        ajax.done(function(res){
            clear_item_form();
            flash_message("Item Deletion Success");
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
        let wishlist_id = $("#wishlist_item_parent").val();
        let wishlist_item_id = $("#wishlist_item_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/wishlists/${wishlist_id}/items/${wishlist_item_id}`,
            contentType: "application/json",
        });

        ajax.done(function(res){
            update_item_form(res);
            flash_message("Retrieve Item Success");
        });

        ajax.fail(function(res){
            clear_item_form();
            flash_message(res.responseJSON.message);
        });
    });

    // ****************************************
    // Purchase an Item
    // ****************************************
    function purchaseItem(wishlistId, itemId) {
        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "PUT",
            url: `/wishlists/${wishlistId}/items/${itemId}/purchase`,
            contentType: "application/json"
        });

        ajax.done(function(res) {
            flash_message("Item purchased successfully!");
            // refresh the items list
            $("#list_items-btn").click();
        });

        ajax.fail(function(res) {
            flash_message(res.responseJSON.message);
        });
    }

    // Add handler for the form purchase button
    $("#purchase_item-btn").click(function () {
        console.log("Purchase item button clicked");
        let wishlist_id = $("#wishlist_item_parent").val();
        let wishlist_item_id = $("#wishlist_item_id").val();
    
        if (!wishlist_id || !wishlist_item_id) {
            flash_message("Please select an item to purchase");
            return;
        }
        purchaseItem(wishlist_id, wishlist_item_id);
        
    });

    // ****************************************
    // List all Items in a Wishlist
    // ****************************************
    $("#list_items-btn").click(function () {
        console.log("List Items button clicked");

        let wishlist_id = $("#wishlist_id").val();
        console.log(`Wishlist ID: ${wishlist_id}`);

        if (!wishlist_id) {
            console.warn("No wishlist ID found");
            $("#flash_message").empty().append("Please select a wishlist first");
            return;
        }

        $("#flash_message").empty();
        $("#list_results").empty(); 

        let ajax = $.ajax({
            type: "GET",
            url: `/wishlists/${wishlist_id}/items`,
            contentType: "application/json",
        });

        ajax.done(function (res) {
            res.forEach(item => {
                console.log("Item details:", {
                    id: item.id,
                    name: item.name,
                    wishlist_id: item.wishlist_id,
                    description: item.description,
                    price: item.price,
                    status: item.status  // Log the status specifically
                });
            });

            if (!Array.isArray(res)) {
                console.error("Response is not an array:", res);
                $("#flash_message").empty().append("Invalid response format");
                return;
            }

            // Initialize table
            let table = `
                <table class="table table-striped" cellpadding="10">
                    <thead>
                        <tr>
                            <th class="col-md-1">ID</th>
                            <th class="col-md-2">Name</th>
                            <th class="col-md-2">Wishlist ID</th>
                            <th class="col-md-3">Description</th>
                            <th class="col-md-2">Price</th>
                            <th class="col-md-2">Status</th>
                            <th class="col-md-2">Actions</th>
                        </tr>
                    </thead>
                    <tbody>
            `;

            // Loop through all items and populate the table
            res.forEach((item, index) => { 
                table += `
                    <tr id="row_${index}">
                        <td>${item.id || ""}</td>
                        <td>${item.name || ""}</td>
                        <td>${item.wishlist_id || ""}</td>
                        <td>${item.description || ""}</td>
                        <td>${item.price ? "$" + parseFloat(item.price).toFixed(2) : ""}</td>
                        <td>${item.status || "pending"}</td>
                        <td>
                            <button class="btn btn-info view-item" data-id="${item.id}">View</button>
                            <button class="btn btn-success purchase-item" 
                                data-wishlist="${item.wishlist_id}" 
                                data-id="${item.id}"
                                ${item.status === 'purchased' ? 'disabled' : ''}>
                                ${item.status === 'purchased' ? 'Purchased' : 'Purchase'}
                            </button>
                        </td>
                    </tr>
                `;
            });

            table += `</tbody></table>`;
            $("#list_results").append(table);
            flash_message("List Items Success");

            // Add view functionality
            $(".view-item").off("click").on("click", function () {
                let itemId = $(this).data("id");
                console.log(`View clicked for item ID: ${itemId}`);

                let ajax = $.ajax({
                    type: "GET",
                    url: `/wishlists/${wishlist_id}/items/${itemId}`,
                    contentType: "application/json",
                })
                
                ajax.done(function (res) {
                    console.log("View item response:", res);
                    $("#wishlist_item_id").val(res.id);
                    $("#wishlist_item_name").val(res.name);
                    $("#wishlist_item_parent").val(res.wishlist_id);
                    $("#wishlist_item_description").val(res.description);
                    $("#wishlist_item_price").val(res.price);
                    $("#wishlist_item_status").val(res.status);
                    
                    flash_message("View Item Action Success");
                })
                
                ajax.fail(function(res){
                    console.error("View item failed:", res);
                    flash_message(res.responseJSON.message);
                });
            });

            // Add purchase functionality
            $(".purchase-item").off("click").on("click", function () {
                const itemId = $(this).data("id");
                const wishlistId = $(this).data("wishlist");
                console.log(`Purchase clicked for item ID: ${itemId} in wishlist ${wishlistId}`);
                purchaseItem(wishlistId, itemId);
            });
        });

        ajax.fail(function(res){
            console.error("List items failed:", res);
            flash_message(res.responseJSON.message);
        });
    });
})
