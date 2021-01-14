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
                $("#loading_search").fadeOut('slow', function() {
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
    $("#follow_submit").fadeOut()
    $("#search_submit").fadeOut('slow', function() {
        $("#loading_search").fadeIn();
    });
    $("#search_results").fadeOut();
}

// trigger another search
$(function() {
    $('#another_search').click(function() {
        $("#another_search").fadeOut('slow', function() {
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
$(document).on('click', '.index.favorites.rm', function() {
    var element = $(this).closest('div');
    $.ajax({
        url: '/remove_from_favorites',
        data: { id: $(this).attr("id") },
        type: 'POST',
        success: function(response) {
            $(element).fadeOut('slow', function() {
                $(element).remove();
            });
            if ($('#favorites').find('div.listing_container').length !== 0) {
                $.ajax({
                    url: '/load_favorites',
                    type: 'POST',
                    success: function(response) {
                        $("#favorites").fadeOut('slow', function() {
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

// ignore change
$(document).on('click', '.index.chg.ignore', function() {
    var query = $(this).attr("value");
    var element = $(this).closest('div');
    $.ajax({
        url: '/ignore_change',
        data: {
            qSet: query
        },
        type: 'POST',
        success: function(response) {
            $(element).fadeOut('slow', function() {
                $(element).remove();
            });
            if ($('#changes').find('div.listing_container').length !== 0) {
                $.ajax({
                    url: '/check_changes',
                    type: 'POST',
                    success: function(response) {
                        $("#changes").fadeOut('slow', function() {
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

// follow search parameters
$(function() {
    $('#follow_submit').click(function() {
        var form_data = $('#search_form').serialize();
        $("#search_form").trigger("reset");
        $.ajax({
            url: '/add_follow',
            data: form_data,
            type: 'POST',
            success: function(response) {
                $("#following").fadeOut('slow', function() {
                    $('#following').html(response);
                });
                $("#following").fadeIn();
            }
        });
    });
});

// check for changes, new followed listings, update the database
$(document).ready(function() {
    // followed
    $.ajax({
        url: '/fetch_followed',
        type: 'POST',
        success: function(response) {
            $("#following").fadeOut('slow', function() {
                $('#following').html(response);
            });
            $("#following").fadeIn()
        },
    });
    // changes
    $.ajax({
        url: '/check_changes',
        type: 'POST',
        success: function(response) {
            $("#changes").fadeOut('slow', function() {
                $('#changes').html(response);
            });
            $("#changes").fadeIn()
        },
        error: function(error) {
            console.log(error);
        },
        complete: function() {
            $("#changes_loader").fadeOut('slow', function() {
                if ($('#changes').find('div.listing_container').length !== 0) {
                    $.ajax({
                        url: '/update_favorites',
                        type: 'POST',
                        success: function(response) {
                            $("#favorites").fadeOut('slow', function() {
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

// remove item from following
$(document).on('click', '.index.follow.rm', function() {
    var element = $(this).closest('div').parent('div');
    $.ajax({
        url: '/remove_from_following',
        data: { id: $(this).attr("id") },
        type: 'POST',
        success: function(response) {
            $(element).fadeOut('slow', function() {
                $(element).remove();
            });
            if ($('#following').find('div.follow_container').length == 0) {
                $.ajax({
                    url: '/fetch_followed',
                    type: 'POST',
                    success: function(response) {
                        $("#following").fadeOut('slow', function() {
                            $('#following').html(response);
                        });
                        $("#following").fadeIn()
                    },
                });
            }
        },
        error: function(error) {
            console.log(error);
        }
    });
});

// ignore follow result
$(document).on('click', '.index.follow.ignore, .index.follow.fav', function() {
    var query = $(this).attr("ignore");
    var element = $(this).closest('div');
    $.ajax({
        url: '/ignore_follow_result',
        data: {
            qSet: query
        },
        type: 'POST',
        success: function(response) {
            $(element).fadeOut('slow', function() {
                $(element).remove();
            });
            if ($('#following').find('div.follow_container').length == 0) {
                $.ajax({
                    url: '/fetch_followed',
                    type: 'POST',
                    success: function(response) {
                        $("#following").fadeOut('slow', function() {
                            $('#following').html(response);
                        });
                        $("#following").fadeIn()
                    },
                });
            }
        },
        error: function(error) {
            console.log(error);
        }
    });
});