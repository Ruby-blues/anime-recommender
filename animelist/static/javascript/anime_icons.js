function later(mal_id, type) {
    console.log("Adding to watch later:", mal_id);
    var csrftoken = getCookie('csrftoken');
    // Send mal_id to your Django view to add to watch later list
    $.ajax({
      url: "{% url 'aurora' %}",
      type: "POST",
      headers: { "X-CSRFToken": csrftoken },
      data: {'mal_id': mal_id, 'status': 'later', 'type': type},
      success: function(response) {
        let image = document.getElementById(`laterImg-${mal_id}`);
        if (response.later) {
          image.src = '/static/icons/tag (1).png';
        }
        else {
          image.src = '/static/icons/tag.png';
        }
        // Handle success response if needed
      },
      error: function(xhr, errmsg, err) {
        console.log(xhr.status + ": " + xhr.responseText);
        // Handle error if needed
      }
    });
  }

  function like(mal_id, type) {
    console.log("Liking:", mal_id);
    var csrftoken = getCookie('csrftoken');
    // Send mal_id to your Django view to like the anime
    $.ajax({
      url: "{% url 'aurora' %}",
      type: "POST",
      headers: { "X-CSRFToken": csrftoken },
      data: {'mal_id': mal_id, 'status': 'like', 'type': type},
      success: function(response) {
        console.log(response);
        let image = document.getElementById(`likedImg-${mal_id}`);
        if (response.like) {
          console.log(response);
            image.src = '/static/icons/favourite (1).png';
          }
          else {
            image.src = '/static/icons/favourite.png';
          }
          // Handle success response if needed
        },
        error: function(xhr, errmsg, err) {
          console.log(xhr.status + ": " + xhr.responseText);
          // Handle error if needed
        }
    });
  }

  // Function to get CSRF cookie
  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
        var cookie = cookies[i].trim();
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
