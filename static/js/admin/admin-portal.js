
// Indicates whether an applicant is currently selected 
var applicantSelected = null; 



function applicantClicked(e, thisClicked, typeOfApp) {

	console.log('applicant selected');
	thisClicked.addClass('applicantSelected'); 

	if (applicantSelected != null) {
		applicantSelected.removeClass('applicantSelected'); 
	}

	applicantSelected = thisClicked; 
	var text = applicantSelected.text(); 
	text = text.split('|')[1].trim().split('-')[0].trim(); 
	console.log(text); 	
	var url = '/api/applicant/' + text + '.json'
	console.log(url); 

	$.ajax({
		url: url, 
		type: 'GET',
		dataType: 'JSON',
		success: function(json) {
	
			console.log("Got here as well"); 
			console.log(json); // JSON
			$('.field').remove(); 
			$('.sub-title').remove(); 

			// Headline 
			$('.info-section').append('<h2 class="field"><strong>' + typeOfApp.toUpperCase() +' Application</strong></h2>'); 

			// Full name 
			$('.info-section').append('<h4 class="field light-face">Name: ' 
													+ json['first_name'] + ' ' + json['last_name'] + '</h4>')

			// Email 
			$('.info-section').append('<h4 class="field light-face">Email: '
																+ json['email'] + '</h4>')

			// Year 
			$('.info-section').append('<h4 class="field light-face">Year: ' 
																+ json['year'] + '</h4>')

			// Major 
			$('.info-section').append('<h4 class="field light-face">Major: '  
																+ json['major'] + '</h4>')

			if (typeOfApp == 'candidate') {
				// Role 
				$('.info-section').append('<h4 class="field light-face">Role: '
														+ json[typeOfApp]['role'] + '</h4>')
			} else { // 'trainee'
				// Highest CS Course 
				$('.info-section').append('<h4 class="field light-face">Highest CS Course: '
														+ json[typeOfApp]['highest_cs_course'] + '</h4>')
			}

			// Essay 
			$('.info-section').append('<h4 class="field light-face">Essay: </h4>')
			$('.info-section').append('<p class="field light-face essay">' + json[typeOfApp]['essay'] + '</p>')

			// Portfolio Link 
			$('.info-section').append('<h4 class="field light-face">Portfolio Link: </h4>')
			$('.info-section').append('<p class="field light-face essay">' + json[typeOfApp]['portfolio_link'] + '</p>')

			// Resume Link
			$('.info-section').append('<h4 class="field light-face">Resume Link: </h4>')
			$('.info-section').append('<p class="field light-face essay">' + json[typeOfApp]['resume_link'] + '</p>')


			// Score input 
			$('.info-section').append('<h4 class="field light-face">Score: <input class="form-control score" type="number" min="0" max="10" value="' 
																					+ json[typeOfApp]['score'] + '"></input></h4>'); 

			// Status textarea 
			$('.info-section').append('<h4 class="field light-face">Status: </h4>'); 
			$('.info-section').append('<textarea class="form-control field status" maxlength="255"></textarea>'); 
			$('.status').val(json[typeOfApp]['status']); 

			// Button to change score/status 
			$('.info-section').append('<button class="red-link edit-' + typeOfApp + '-app field">Edit score/status</button>'); 

			// On-click function to submit data 
			$('.edit-' + typeOfApp + '-app').on('click', function(e) {

				e.preventDefault(); 
				

				var text = applicantSelected.text(); 
				var email = text.split('|')[1].trim().split('-')[0].trim(); 

				console.log('Score: ' + $('.score').val()); 

				console.log('Status: ' + $('.status').val()); 

				var myJSON = {
												'app': typeOfApp,
												'email': email,
												'score': $('.score').val(),
												'status': $('.status').val()
										 }; 

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



		}, 


		error: function(xhr, err, errmsg) {
			console.log("ERROR"); 
		}

	});

}




// Handles CSRF TOKEN STUFF + LOGOUT; event handlers added via inline html 
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








}); 