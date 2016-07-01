var slot = 1
var f = function(){
    slot --
    var status = $(this)
    console.log(status)
    if (status.text() == "queueing..." || status.text() == 'pending') {
        console.log("Yes!!")
        jQuery.getJSON("getstatus/" + status.attr("id"), function(data){
            status.replaceWith ("<td id = "+  status.attr("id")+ ">" + data.status + "</td>")
            if ((data.status == 'queueing...' || data.status == 'pending') && slot <= 0) {
                setTimeout(function(){
                    $("td[id^='status']").each(f)
                }, 500)
                slot++
            }
        })
    }
}
$("td[id^='status']").each(f)