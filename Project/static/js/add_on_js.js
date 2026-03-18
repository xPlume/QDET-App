(function ($) {
	"use strict";
	
	
	// Initialize the WOW if screen is larger than 992px (Bootstrap's lg breakpoint)
	document.addEventListener("DOMContentLoaded", function () {
		if (window.innerWidth >= 992) {
			new WOW().init();
		}
	});
	
	
	
	// Facts counter
	$('[data-toggle="counter-up"]').counterUp({
		delay: 10,
		time: 1000
	});
	
	
	
})(jQuery);

