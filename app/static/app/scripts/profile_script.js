// Taken from Django user docs at https://docs.djangoproject.com/en/4.1/howto/csrf/
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// https://stackoverflow.com/questions/6121203/how-to-do-fade-in-and-fade-out-with-javascript-and-css
function fade(element) {
    var op = 1;  // initial opacity
    var timer = setInterval(function () {
        if (op <= 0.1) {
            clearInterval(timer);
            element.remove();
        }
        element.style.opacity = op;
        element.style.filter = 'alpha(opacity=' + op * 100 + ")";
        op -= op * 0.1;
    }, 50);
}

function flash_prof_msg(attribute_type, msg) {
    var attribute_p = "profile_" + attribute_type + "_content";
    var attribute_p_el = document.getElementById(attribute_p);
    var failure_msg = document.createElement('span');
    failure_msg.textContent = msg;
    failure_msg.style.color = "red";

    attribute_p_el.appendChild(failure_msg);

    // Fade out element after a few seconds
    setTimeout(() => {
        fade(failure_msg);
    }, 1000);
}


//function change_prof_pic() {
//    var new_prof_pic = document.getElementById("new_prof_pic").files[0];
//    var new_prof_pic_file_name = document.getElementById("new_prof_pic").value;

//    if (new_prof_pic_file_name == "") {
//        flash_prof_msg("prof_pic", "Please select a file")
//        return;
//    }

//    var file_name = new_prof_pic.name;
//    console.log(file_name);

//    // For CSRF protection
//    const csrftoken = getCookie('csrftoken');
//    // POST data to Django server using AJAX
//    $.ajax({
//        type: "POST",
//        url: "/profile/",
//        headers: {
//            'X-CSRFToken': csrftoken
//        },
//        data: {
//            "attribute_type": "prof_pic",
//            "new_prof_pic": new_prof_pic
//        },
//        success: function (response) {
//            if (response.success == True) {
//                console.log("success");
//            } else {
//                console.log("failure");
//            }
//        },
//        error: function (error) {
//            console.log("Error: ", error);
//        }
//    });
//}

function edit(attribute) {
    var edit_id = "profile_" + attribute + "_edit";
    var display_id = "profile_" + attribute + "_display";
    document.getElementById(edit_id).style.display = "inline";
    document.getElementById(display_id).style.display = "none";

    // Get rid of pencil icon for profile description element
    if (attribute == "prof_desc") {
        document.getElementById("profile_prof_desc_pencil").style.display = "none";
        document.getElementById("profile_prof_desc_check").style.display = "inline";
    }
}

function change_user_attribute(attribute) {
    // To get the new value the user typed in the input box
    var attribute_input_id = "profile_" + attribute + "_input";
    var new_value = document.getElementById(attribute_input_id).value.trim();
    var attribute_display_id = "profile_" + attribute + "_value";
    var old_value = document.getElementById(attribute_display_id).textContent.trim();

    // Get parts of HTML file that either show edit buttons or just display the values
    var edit_id = "profile_" + attribute + "_edit";
    var display_id = "profile_" + attribute + "_display";

    // Don't do anything if the user didn't change the value
    // Avoids wasting ajax call and database update
    if (old_value == new_value) {
        document.getElementById(edit_id).style.display = "none";
        document.getElementById(display_id).style.display = "inline";

        // For profile description
        if (attribute == "prof_desc") {
            document.getElementById("profile_prof_desc_pencil").style.display = "inline";
            document.getElementById("profile_prof_desc_check").style.display = "none";
        }

        // Give input the old value
        document.getElementById(attribute_input_id).value = old_value;

        return;
    }

    // Flash message if user inputted empty string
    if (new_value == "") {
        flash_prof_msg(attribute, "Please enter a value");
        return;
    }

    // For CSRF protection
    const csrftoken = getCookie('csrftoken');
    // POST data to Django server using AJAX
    $.ajax({
        type: "POST",
        url: "/profile/",
        headers: {
            'X-CSRFToken': csrftoken
        },
        data: {
            "attribute_type": attribute,
            "new_value": new_value,
            "old_value": old_value
        },
        dataType: "json",
        success: function (response) {
            if (response.success == true) {
                // If update was successful, then change the value displayed to the new updated value
                var attribute_display_value = "profile_" + response.attribute_type + "_value";
                document.getElementById(attribute_display_value).textContent = new_value;

                // Change profile greeting, as that uses the first name
                if (response.attribute_type == "first_name") {
                    document.getElementById("profile_greeting").textContent = "Hello, " + new_value + "!";
                }
            } else {
                // If the update failed, then change the input value back to the old value, so that the value in the input stays in line with the current value
                var attribute_input_value = "profile_" + response.attribute_type + "_input";
                document.getElementById(attribute_input_value).value = old_value;
                console.log(response.error_msg);

                // Add failure message after the pencil icon
                // Only add if a previous message isn't already there
                if (JSON.stringify(document.getElementById("failure_msg")) == "null") {
                    flash_prof_msg(response.attribute_type, "Could not change user data. Try again later.");
                }

            }
        },
        error: function (error) {
            console.log("Error: ", error);
        }
    });

    // To display and hide edit input and button after attribute has been edited
    document.getElementById(edit_id).style.display = "none";
    document.getElementById(display_id).style.display = "inline";

    if (attribute == "prof_desc") {
        document.getElementById("profile_prof_desc_pencil").style.display = "inline";
        document.getElementById("profile_prof_desc_check").style.display = "none";
    }
}



function post_to_django(post_data) {


    const csrftoken = getCookie('csrftoken');



    // POST data to Django server using AJAX
    $.ajax({
        type: "POST",
        url: "/profile/",
        headers: {
            'X-CSRFToken': csrftoken
        },
        data: post_data,
        success: function (response) {
            if (response.success == true) {
                alert("data successfully posted")
            } else {
                alert("data not successfully posted")
            }
        },
        error: function (error) {
            console.log("Error: ", error);
        }
    });
}

