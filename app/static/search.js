function loading_animation() {
    $("#search_submit").fadeOut('#search_submit', function() {
        $("#loading").fadeIn();
    });
    $("#search_results").fadeOut();
}

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

$(document).ready(function() {
    $(document).on('click', '.index_fav', function() {
        var query = $(this).attr("value");
        $.ajax({
            url: '/add_to_favorites',
            data: {
                qSet: query
            },
            type: 'POST',
            success: function(response) {
                $("#loading").fadeOut('#loading', function() {
                    $('#favorites').html(response);
                });
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});