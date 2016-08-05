var csrftoken = getCookie('csrftoken');

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

//csrfmiddlewaretoken

$('.vote-button').click(function() {
  var id = $(this).data('post-id');
  sendPostVote(id);
  var is_voted_on = $(this).data('post-voted-on');
  var score_element = $(this).find('.postscore');
  var vote_button = $(this).find('.voteicon')

  if (is_voted_on == 'yes') {
    vote_button.css('color', 'black');
    $(this).data('post-voted-on', 'no');
    var score = parseInt(score_element.html());
    score_element.html(score - 1);
  } else {
    vote_button.css('color', 'red');
    $(this).data('post-voted-on', 'yes');
    var score = parseInt(score_element.html());
    score_element.html(score + 1);
  }
});

function sendPostVote(id) {
  $.post( "/ajax/postvote/", {'postid': id, 'csrfmiddlewaretoken': csrftoken}).done(function(data) {

  });
}
