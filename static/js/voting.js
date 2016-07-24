function init_thread_voting() {
    function process_vote(vote_button, vote_type) {
        var post_url = vote_button.parent().parent().data("update-url") + "vote/";

        $.post(post_url, { }, function(data, status) {
            if(status == "success") {
                vote_button.siblings().filter("span.vote-number").text(data.votes);
                vote_button.addClass("disabled");
                vote_button.siblings("a").removeClass("disabled");
            }
        });
    }

    $("a.vote-up-button").click(function() { process_vote($(this), "up"); });
    $("a.vote-down-button").click(function() { process_vote($(this), "down"); });
}
