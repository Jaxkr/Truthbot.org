var csrftoken = getCookie('csrftoken');

$('.voting .vote-up').click(function() {
  var score_element = $(this).closest('p').find('.review-score')
  score_element.css("color", "red");
  var score = parseInt(score_element.html());
  score_element.html(score + 1);

  var url = $(this).attr('data-voteurl');

  $.post(url, {csrfmiddlewaretoken: csrftoken}, function(data) {
  });
});
$('.voting .vote-down').click(function() {
  var score_element = $(this).closest('p').find('.review-score')
  score_element.css("color", "blue");
  var score = parseInt(score_element.html());
  score_element.html(score - 1);

  var url = $(this).attr('data-voteurl');

  $.post(url, {csrfmiddlewaretoken: csrftoken}, function(data) {
  });
});

function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var cookie = jQuery.trim(cookies[i]);
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
