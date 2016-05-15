function prob_rank() {
    $.ajax({
        type: "POST",
        url: "/rank/prob",
        dataType: "html",
        error: function(XMLHttpRequest, textStatus, errorThrown) {
            alert(errorThrown);
        },
        success: function(data, status) {
            if ($("#problem").is(":empty")) {
                $("#problem").append(data);
            }
        }
    });
}
$(document).ready(function() {
    prob_rank();
    $("#ptab").click(function() {
        prob_rank();
    });
    $("#htab").click(function() {
        $.ajax({
            type: "POST",
            url: "/rank/home",
            dataType: "html",
            error: function(XMLHttpRequest, textStatus, errorThrown) {
                alert(errorThrown);
            },
            success: function(data, status) {
                if ($("#homework").is(":empty")) {
                    $("#homework").append(data);
                }
            }
        });
    });
    $("#ctab").click(function() {
        $.ajax({
            type: "POST",
            url: "/rank/camp",
            dataType: "html",
            error: function(XMLHttpRequest, textStatus, errorThrown) {
                alert(errorThrown);
            },
            success: function(data, status) {
                if ($("#traincamp").is(":empty")) {
                    $("#traincamp").append(data);
                }
            }
        });
    });
});