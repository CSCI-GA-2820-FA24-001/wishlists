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

    // TODO:
    // // ****************************************
    // // Create a Pet
    // // ****************************************

    // $("#create-btn").click(function () {

    //     let name = $("#pet_name").val();
    //     let category = $("#pet_category").val();
    //     let available = $("#pet_available").val() == "true";
    //     let gender = $("#pet_gender").val();
    //     let birthday = $("#pet_birthday").val();

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
    //     ajax.done(function(res){
    //         update_form_data(res)
    //         flash_message("Success")
    //     });

    //     ajax.fail(function(res){
    //         flash_message(res.responseJSON.message)
    //     });
    // });


    // // ****************************************
    // // Update a Pet
    // // ****************************************

    // $("#update-btn").click(function () {

    //     let pet_id = $("#pet_id").val();
    //     let name = $("#pet_name").val();
    //     let category = $("#pet_category").val();
    //     let available = $("#pet_available").val() == "true";
    //     let gender = $("#pet_gender").val();
    //     let birthday = $("#pet_birthday").val();

    //     let data = {
    //         "name": name,
    //         "category": category,
    //         "available": available,
    //         "gender": gender,
    //         "birthday": birthday
    //     };

    //     $("#flash_message").empty();

    //     let ajax = $.ajax({
    //             type: "PUT",
    //             url: `/pets/${pet_id}`,
    //             contentType: "application/json",
    //             data: JSON.stringify(data)
    //         })

    //     ajax.done(function(res){
    //         update_form_data(res)
    //         flash_message("Success")
    //     });

    //     ajax.fail(function(res){
    //         flash_message(res.responseJSON.message)
    //     });

    // });

    // // ****************************************
    // // Retrieve a Pet
    // // ****************************************

    // $("#retrieve-btn").click(function () {

    //     let pet_id = $("#pet_id").val();

    //     $("#flash_message").empty();

    //     let ajax = $.ajax({
    //         type: "GET",
    //         url: `/pets/${pet_id}`,
    //         contentType: "application/json",
    //         data: ''
    //     })

    //     ajax.done(function(res){
    //         //alert(res.toSource())
    //         update_form_data(res)
    //         flash_message("Success")
    //     });

        ajax.fail(function(res) {
            flash_message(res.responseJSON.message);
        });
    });
    //     ajax.fail(function(res){
    //         clear_form_data()
    //         flash_message(res.responseJSON.message)
    //     });

    // });

    // // ****************************************
    // // Delete a Pet
    // // ****************************************

    // $("#delete-btn").click(function () {

    //     let pet_id = $("#pet_id").val();

    //     $("#flash_message").empty();

    //     let ajax = $.ajax({
    //         type: "DELETE",
    //         url: `/pets/${pet_id}`,
    //         contentType: "application/json",
    //         data: '',
    //     })

    //     ajax.done(function(res){
    //         clear_form_data()
    //         flash_message("Pet has been Deleted!")
    //     });

    //     ajax.fail(function(res){
    //         flash_message("Server error!")
    //     });
    // });

    // // ****************************************
    // // Clear the form
    // // ****************************************

    // $("#clear-btn").click(function () {
    //     $("#pet_id").val("");
    //     $("#flash_message").empty();
    //     clear_form_data()
    // });

    // // ****************************************
    // // Search for a Pet
    // // ****************************************

    // $("#search-btn").click(function () {

    //     let name = $("#pet_name").val();
    //     let category = $("#pet_category").val();
    //     let available = $("#pet_available").val() == "true";

    //     let queryString = ""

    //     if (name) {
    //         queryString += 'name=' + name
    //     }
    //     if (category) {
    //         if (queryString.length > 0) {
    //             queryString += '&category=' + category
    //         } else {
    //             queryString += 'category=' + category
    //         }
    //     }
    //     if (available) {
    //         if (queryString.length > 0) {
    //             queryString += '&available=' + available
    //         } else {
    //             queryString += 'available=' + available
    //         }
    //     }

    //     $("#flash_message").empty();

    //     let ajax = $.ajax({
    //         type: "GET",
    //         url: `/pets?${queryString}`,
    //         contentType: "application/json",
    //         data: ''
    //     })

    //     ajax.done(function(res){
    //         //alert(res.toSource())
    //         $("#search_results").empty();
    //         let table = '<table class="table table-striped" cellpadding="10">'
    //         table += '<thead><tr>'
    //         table += '<th class="col-md-2">ID</th>'
    //         table += '<th class="col-md-2">Name</th>'
    //         table += '<th class="col-md-2">Category</th>'
    //         table += '<th class="col-md-2">Available</th>'
    //         table += '<th class="col-md-2">Gender</th>'
    //         table += '<th class="col-md-2">Birthday</th>'
    //         table += '</tr></thead><tbody>'
    //         let firstPet = "";
    //         for(let i = 0; i < res.length; i++) {
    //             let pet = res[i];
    //             table +=  `<tr id="row_${i}"><td>${pet.id}</td><td>${pet.name}</td><td>${pet.category}</td><td>${pet.available}</td><td>${pet.gender}</td><td>${pet.birthday}</td></tr>`;
    //             if (i == 0) {
    //                 firstPet = pet;
    //             }
    //         }
    //         table += '</tbody></table>';
    //         $("#search_results").append(table);

    //         // copy the first result to the form
    //         if (firstPet != "") {
    //             update_form_data(firstPet)
    //         }

    //         flash_message("Success")
    //     });

    //     ajax.fail(function(res){
    //         flash_message(res.responseJSON.message)
    //     });

    // });

})
