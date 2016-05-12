$(function () {
    $('#fileupload').fileupload({
        autoUpload: false,
        replaceFileInput: false,
        maxChunkSize: 1000000,
        add : function(e, data) {
            $("#submit").on('click', function () {
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