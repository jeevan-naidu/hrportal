// JavaScript Document
jQuery(document).ready(function($){
	//Put Your Custom Jquery or Javascript Code Here


	// Height script for text section


	heightFunction = function(){
		hgt1=$('.jsh1').css('height');
		$('.jsh2').css('height', hgt1);
	}

	// Height for navbar

	navHeight = function(){
		vph = $(window).height();
		// console.log(vph);
		// vphp = parseInt(vph);
		vph -= 106;
		// console.log(vphp);
		$('.vd_content-wrapper').css('min-height', vph + 'px' );
	}


	extendRibbon = function(){
		$('#oneteam-ribbon').addClass('extended');
	}


	// File Upload Validations (File size and extension)
				var fileExtension = ['jpg', 'csv','png', 'pdf', 'xlsx', 'xls', 'docx', 'doc', 'jpeg', 'eml'];
				$('.filestyle').bind('change', function() {
				if (this.files[0].size > 1000000) {
					alert("File size greater than 1MB not allowed");
					$('.filestyle').val('')
				}
				else
				{
					if ($.inArray($(this).val().split('.').pop().toLowerCase(), fileExtension) == -1) {
                    alert("Allowed file types : "+fileExtension.join(', '));
										$('.filestyle').val('')
                }
				}
				});

	// Function Calls


	navHeight();
	heightFunction();


	$(window).resize(function(){
		navHeight();
		heightFunction();
	})

	$(window).load(function(){
		heightFunction();
		setTimeout(function(){ 
			extendRibbon(); 
		}, 1000);
	})





	
});