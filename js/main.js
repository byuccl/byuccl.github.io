$(".abstract").click(function(event) {
    var description = $(event.target).parent().next();
    description.slideToggle("slow");
});