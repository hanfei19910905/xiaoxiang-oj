var slot = 1
var f = function(){
    slot --
    var status = $(this)
    id = status.attr("id").substring(7)
    if (status.text() == "queueing..." || status.text() == 'pending') {
        jQuery.getJSON("getstatus/" + id, function(data){
            status.replaceWith ("<td id = "+  status.attr("id")+ ">" + data.status + "</td>")
            id = status.attr("id").substring(7)
            score = $("#score_" + id)
            console.log(data.score)
            console.log(score)
            score.replaceWith("<td id = "+  score.attr("id")+ ">" + data.score + "</td>")
            if ((data.status == 'queueing...' || data.status == 'pending') && slot <= 0) {
                setTimeout(function(){
                    $("td[id^='status']").each(f)
                }, 1000)
                slot++
                console.log("set")
            }
        })
    }
}
$("td[id^='status']").each(f)
