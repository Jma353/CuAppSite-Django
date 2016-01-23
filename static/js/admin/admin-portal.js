
// Indicates whether an applicant is currently selected 
var applicantSelected = null; 


function traineeClicked(e, thisClicked) {

	console.log('applicant selected'); 
	thisClicked.addClass('applicantSelected'); 

	if (applicantSelected != null) {
		applicantSelected.removeClass('applicantSelected'); 
	}

	applicantSelected = thisClicked; 
	var text = applicantSelected.text(); 
	text = text.split('|')[1].trim().split('-')[0].trim(); 
	console.log(text); 
	var myJSON = { 'trainee-email': text }; 
	var url = window.location.pathname; 

	$.ajax({
		url: url, 
		type: 'POST',
		data: JSON.stringify(myJSON),
		contentType: 'applicantion/JSON; charset=utf-8',
		dataType: 'JSON',
		success: function(json) {
			console.log("Got here as well"); 
			$('.field').remove(); 
			$('.sub-title').remove(); 
			$('.info-section').append('<h4 class="field light-face">Name: ' 
													+ json['first_name'] + ' ' + json['last_name'])
		}
	}); 
}



function candidateClicked(e, thisClicked) {

	console.log('applicant selected');
	thisClicked.addClass('applicantSelected'); 

	if (applicantSelected != null) {
		applicantSelected.removeClass('applicantSelected'); 
	}

	applicantSelected = thisClicked; 
	var text = applicantSelected.text(); 
	text = text.split('|')[1].trim().split('-')[0].trim(); 
	console.log(text); 
	var myJSON = { 'candidate-email': text }; 	
	var url = window.location.pathname; 

	$.ajax({
		url: url, 
		type: 'POST',
		data: JSON.stringify(myJSON),
		contentType: 'application/JSON; charset=utf=8',
		dataType: 'JSON',
		success: function(json) {
			$('.field').remove(); 
			$('.sub-title').remove(); 
			$('.info-section').append('<h4 class="field light-face">Name: ' 
													+ json['first_name'] + ' ' + json['last_name'])
		}
	});

}


$(document).ready(function(){
	


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




	// On selection of a trainee 
	$('.trainee').on("click", function(e) {
		traineeClicked(e, $(this)); 
	}); 



	// On selection of a candidate
	$('.candidate').on("click", function(e) {
		candidateClicked(e, $(this)); 
	});




}); 