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

$(function() {
    $('#another_search').click(function() {
        $("#another_search").fadeOut('#another_search', function() {
            $("#search_form").trigger("reset");
            $("#search_submit").fadeIn();
            $("#search_results").fadeOut();
        });
    })
});