$(document).ready(function() {
  $("input#comment-submit-btn").click(function(event) {
    event.preventDefault();
    var post_url = "/comment/add/" + $("input#comment-submit-btn").data("id");
    var data = { content: $("textarea#new-comment").val() }
    if ($("textarea#new-comment").val() != "") {
      $.ajax({
        type: "POST",
        contentType: "application/json; charset=utf-8",
        url: post_url,
        data: JSON.stringify({content: $("textarea#new-comment").val() }),
        success: function(data) {
            update_comments(data.comments);
        },
        dataType: "json"
      });
    }
  });
});

var update_comments = function(comments) {
  var new_html = "";
  for (var i = 0; i < comments.length; i++) {
    var comment = comments[i];
    new_html += "<div class='comment'>";
    new_html += comment.content;
    new_html += "<br><span class='comment-date'>";
    new_html += comment.created;
    new_html += "</span></div>"
  }
  $("div.comments").html(new_html);
  $("textarea#new-comment").val("");
}
