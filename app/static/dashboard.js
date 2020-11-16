// div expand function
$('#expand_fav').click(function() {
    $('#favorites').toggleClass('expanded');
    $('#expand_fav').text(function(i, text) {
        return text === "Collapse" ? "Expand" : "Collapse";
    })
});
$('#changes').click(function() {
    $(this).toggleClass('expanded');
});

// execute search
$(function() {
    $('#search_submit').click(function() {
        loading_animation()
        $.ajax({
            url: '/search',
            data: $('#search_form').serialize(),
            type: 'POST',
            success: function(response) {
                $("#loading_search").fadeOut('#loading_search', function() {
                    $('#search_results').html(response);
                    $("#search_results").fadeIn();
                    if ($(".error_box").length) {
                        $("#search_submit").fadeIn();
                    } else {
                        $("#another_search").fadeIn();
                    }
                });
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});

// search loading animation
function loading_animation() {
    $("#search_submit").fadeOut('#search_submit', function() {
        $("#loading_search").fadeIn();
    });
    $("#search_results").fadeOut();
}

// trigger another search
$(function() {
    $('#another_search').click(function() {
        $("#another_search").fadeOut('#another_search', function() {
            //$("#search_form").trigger("reset");
            $("#search_submit").fadeIn();
            $("#search_results").fadeOut();
        });
    })
});

// add item to favorites
$(document).on('click', '.index.fav', function() {
    var query = $(this).attr("value");
    $.ajax({
        url: '/add_to_favorites',
        data: {
            qSet: query
        },
        type: 'POST',
        success: function(response) {
            $('.listing_container_placeholder').replaceWith(response);
            if ($('#favorites').find('h3.center-text').length !== 0) {
                $('#favorites').find('h3.center-text').closest('div').remove();
            }
        },
        error: function(error) {
            console.log(error);
        }
    });
});

// remove item from favorites
$(document).on('click', '.index.rm', function() {
    var element = $(this).closest('div');
    $.ajax({
        url: '/remove_from_favorites',
        data: { id: $(this).attr("id") },
        type: 'POST',
        success: function(response) {
            $(element).fadeOut("normal", function() {
                $(element).remove();
            });
            if ($('#favorites').find('div.listing_container').length !== 0) {
                $.ajax({
                    url: '/load_favorites',
                    type: 'POST',
                    success: function(response) {
                        $("#favorites").fadeOut('normal', function() {
                            $('#favorites').html(response);
                        });
                        $("#favorites").fadeIn()
                    },
                });
            }
        },
        error: function(error) {
            console.log(error);
        }
    });
});

// check for changes, update the database and favorites
$(document).ready(function() {
    var element = $(this).closest('div');
    $.ajax({
        url: '/check_changes',
        type: 'POST',
        success: function(response) {
            $("#changes").fadeOut('#changes', function() {
                $('#changes').html(response);
            });
            $("#changes").fadeIn()
        },
        error: function(error) {
            console.log(error);
        },
        complete: function() {
            $("#checking_loader").fadeOut('#checking_loader', function() {
                if ($('#changes').find('div.listing_container').length !== 0) {
                    $.ajax({
                        url: '/update_favorites',
                        type: 'POST',
                        success: function(response) {
                            $("#favorites").fadeOut('#favorites', function() {
                                $('#favorites').html(response);
                            });
                            $("#favorites").fadeIn();
                        },
                        error: function(error) {
                            console.log(error);
                        }
                    });
                }
            });
        }
    });
});

// ignore change
$(document).on('click', '.index.ignore', function() {
    var query = $(this).attr("value");
    var element = $(this).closest('div');
    $.ajax({
        url: '/ignore_change',
        data: {
            qSet: query
        },
        type: 'POST',
        success: function(response) {
            $(element).fadeOut("normal", function() {
                $(element).remove();
            });
            if ($('#changes').find('div.listing_container').length !== 0) {
                $.ajax({
                    url: '/check_changes',
                    type: 'POST',
                    success: function(response) {
                        $("#changes").fadeOut('normal', function() {
                            $('#changes').html(response);
                        });
                        $("#changes").fadeIn()
                    },
                });
            }
        },
        error: function(error) {
            console.log(error);
        }
    });
});