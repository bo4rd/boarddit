function init_thread_voting() {
    init_voting("thread");
}

function init_comment_voting() {
    init_voting("comment");
}

function init_voting(entity_type) {
    function process_vote(vote_button, vote_type) {
        var post_url = vote_button.parent().parent().data("update-url");

        $.post(post_url, { }, function(data, status) {
            if(status == "success") {
                vote_button.siblings().filter("span.vote-number").text(data.votes);
                vote_button.addClass("disabled");
                vote_button.siblings("a").removeClass("disabled");
            }
        });
    }

    $("a.vote-up-" + entity_type).click(function() { process_vote($(this), "up"); });
    $("a.vote-down-" + entity_type).click(function() { process_vote($(this), "down"); });
}
