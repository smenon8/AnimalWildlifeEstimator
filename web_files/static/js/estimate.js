$(function() {
    $('#btnEstimate').click(function() {

        $.ajax({
            url: '/estimation',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                $('#result').html(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});