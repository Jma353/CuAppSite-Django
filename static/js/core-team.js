$(document).ready(function() {


	// Deals with CSRF resolution on AJAX request 
	var csrftoken = Cookies.get('csrftoken'); // Received from the CSRF 
	
	function csrfSafeMethod(method) {
  	// these HTTP methods do not require CSRF protection
  	return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
	}

	$.ajaxSetup({
  	beforeSend: function(xhr, settings) {
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
          xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
  	}	
	});



	// This handles limiting the response characters of the essay for the 
	// team application 
	$('.essay').on('keyup', function(e) {
		
		var size = $.trim(this.value).length ? this.value.match(/\S+/g).length : 0; 
		// Essentially, if the trim is successful, match the spaces on the inside
		if(size > 300) {
			var original = $(this).val().split(/s+/g, 300).join(" ");
			$(this).val(original); 
		} else {
			$('.word-count').text(300-size);
		}


	});


	$('.form-group input').on('keydown', function(e) {
		console.log("hello world"); 
		var parent = $(this).closest('.form-group'); 
		parent.removeClass('has-error');
		parent.children('.error-message').children('ul').empty(); 
	}); 










}); 