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
});