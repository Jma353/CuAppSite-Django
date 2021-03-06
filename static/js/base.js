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



	$('.footer-form').on('submit', function(e) {
		e.preventDefault(); 
		var data = $(this).serialize(); 
		var url = "/"

		console.log(data); 
		
		$.ajax({
			url: url,
			dataType: "JSON",
			method: "POST",
			data: data,
			success: function(json) {

				if (json.success) {
					console.log("This was successful"); 
					$('.footer-enter-email').animo({ animation: "fadeOutUp", duration: 0.75, keep: true }, function() {
						$('.footer-enter-email').css("display", "none"); 
						var resultText = $('.FooterEmailResult'); // Result div 
						resultText.text(json['success']); // Extract success message 
						resultText.animo( { animation: "fadeInDown", duration: 0.75 }); 
					}); 
				} else {
					console.log("This was not successful"); 
					var resultText = $('.FooterEmailResult'); // Result div 
					console.log(json);
					var newJSON = $.parseJSON(json); 
					console.log(newJSON); 
					console.log(newJSON['email'][0]['message']); 
					resultText.text(newJSON['email'][0]['message']); // Extract success message 
					resultText.animo( { animation: "fadeInDown", duration: 0.75 }); 
				}
				
			},
			error: function(xhr, errmsg, err) {
				console.log(xhr.status + ": " + xhr.responseText); 
			},
			complete: function() {
				setTimeout(function(){
					$('.footer-email-input').val(''); 
				}, 2000); 
			}

 		}); 
	}); 	



}); 