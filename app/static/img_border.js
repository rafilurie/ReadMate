$(document).ready(function() {
    $("img").click(function() {
        $("img.selected").removeClass("selected");
        $(this).addClass("selected");
    });

    $("button#help-btn").click(function() {
        if ($("img.selected").length == 1) {
            var detailUrl = $("img.selected").first().data("detail");
            window.location.replace(detailUrl);
        }
    });

    $("button#download-pdf").click(function() {
        var name = $("input#full-name").val();
        if (name == "") { name = "No Name" }
        var id = $("input#full-name").data("perp");
        var pdfUrl = "/pdf/" + id + "/" + name;
        window.location.replace(pdfUrl);
    });
});
