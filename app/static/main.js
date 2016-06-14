$(function () {
    var files = []
    var pars = []
    $('#fileupload').fileupload({
        autoUpload: false,
        replaceFileInput: false,
        maxChunkSize: 1024 * 1024 * 10,
        add : function(e, data) {
            file = data
            name = e.delegatedEvent.target.name
            files.push(file)
            pars.push(name)
            console.log(name)
        },
        progressall: function (e, data) {
            console.log("load " + data.loaded + ", total " + data.total);
            var progress = parseInt(data.loaded / data.total * 100, 10);
            $('#progress .bar').css(
                'width',
                progress + '%'
            );
        },
        stop : function(e) {
            window.location.href = '/admin/data'
        },
//        chunkalways: function(e, opt) {
//            console.log(opt.jqXHR)
//            console.log(opt.result)
//        },
//        always: function(e, opt) {
//            console.log(opt.jqXHR)
//            console.log(opt.result)
//        },

    })
    $("#submit").on('click', function (e) {
        e.preventDefault();
        var names = ['train', 'test1', 'test2', 'attach']
        var r_f = ['', '', '', '']
        var hash = [false, false, false, false]
        for (var i = pars.length - 1; i >= 0; i--)
        {
            console.log(pars[i])
            for(var j = 0; j< 4; j++){
                if (names[j] == pars[i] && !hash[j]){
                    hash[j] = true
                    r_f[j] = files[i]
                    break;
                }
            }
        }
        for(var i = 0; i < 3; i++)
            if (!hash[i])
            {
                console.log("failed")
                return false
            }
        for (var i = 0; i < 4; i++)
        {
            r_f[i].submit()
        }
        $("#submit").unbind('click')
    });
});
