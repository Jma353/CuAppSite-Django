$(document).ready(function() {


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

	$('.core-team-form').on('submit', function(e) {
		e.preventDefault(); 
		var data = $(this).serialize(); 

		console.log(data); 

		
	}); 



}); 