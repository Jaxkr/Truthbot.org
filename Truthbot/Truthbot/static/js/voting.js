$('.voting .vote-up').click(function() {
  $(this).closest('p').find('.review-score').css("color", "red");
});
