$(function () {
    $('#fileupload').fileupload({
        autoUpload: false,
        replaceFileInput: false,
        add : function(e, data) {
            $("#submit").off('click').on('click', function () {
                data.submit();
            });
        },
        progressall: function (e, data) {
            console.log("load " + data.loaded + ", total " + data.total);
            var progress = parseInt(data.loaded / data.total * 100, 10);
            $('#progress .bar').css(
                'width',
                progress + '%'
            );
        }
    })
});