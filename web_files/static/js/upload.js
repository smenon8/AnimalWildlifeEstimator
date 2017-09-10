$(function() {
    $('#btnUpload').submit(function() {

        $.ajax({
            url: '/upload',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                $('#uploadResponse').html(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});