// execute search
$(function() {
    $('#search_submit').click(function() {
        loading_animation()
        $.ajax({
            url: '/search',
            data: $('#search_form').serialize(),
            type: 'POST',
            success: function(response) {
                $("#loading").fadeOut('#loading', function() {
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
        $("#loading").fadeIn();
    });
    $("#search_results").fadeOut();
}

// trigger another search
$(function() {
    $('#another_search').click(function() {
        $("#another_search").fadeOut('#another_search', function() {
            $("#search_form").trigger("reset");
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
        },
        error: function(error) {
            console.log(error);
        }
    });
});

$(document).ready(function() {
    var element = $(this).closest('div');
    $.ajax({
        url: '/check_changes',
        type: 'POST',
        success: function(response) {
            $('#changes').html(response);
            $("#changes").fadeIn()
        },
        error: function(error) {
            console.log(error);
        },
        complete: function() {
            if ($('#changes').find('div.listing_container').length !== 0) {
                var data = [];
                $('#changes').children('div').each(function() {
                    data.push({
                        item: $(this).attr('item'),
                        value: $(this).attr('value')
                    });
                });
                $.ajax({
                    url: '/update_database_changes',
                    data: {
                        data
                    },
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
        }
    });
});