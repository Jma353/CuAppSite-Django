$(document).ready(function(){
	console.log("Hello world!"); 



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




	// TO LOGOUT 
	$('.logout').on('click', function(e) {
		e.preventDefault(); 

		var myJSON = {'logout': true }; 
		console.log(JSON.stringify(myJSON)); 
		var url = window.location.pathname; 

		$.ajax({
			url: url, 
			type: 'POST',
			data: JSON.stringify(myJSON),
			contentType: 'application/JSON; charset=utf-8',
			dataType: 'JSON',
			success: function(json) {
				console.log("got here!"); 
				if(json['redirect']) {
					window.location.pathname = json['redirect']
				}

			}


		}); 

	}); 


	// Indicates whether an applicant is currently selected 
	var applicantSelected = false; 

	// To display when someone is not selected 
	if (applicantSelected == false) {
		$('.info-section').append("<h2>Please select an applicant</h2>"); 
	}



	// On selection of a trainee 
	$('.trainee').on("click", function(e) {
		var text = $(this).text(); 
		text = text.split('|')[1].trim(); 
		text = text.split('-')[0].trim(); 
		console.log(text); 
	}); 







}); 