ClassicEditor
.create( document.querySelector( '#editor' ) )
.then( editor => {
	console.log( editor );
} )
.catch( error => {
	console.error( error );
} );

$(function(){ 
	$('form').attr('autocomplete','off');
	$('[data-toggle="tooltip"]').tooltip();
	$('.datepick').datetimepicker();
	moment().format();
	$('.page-alert').slideDown();
});

$.extend(true, $.fn.datetimepicker.defaults, {
	icons: {
		time: 'far fa-clock',
		date: 'far fa-calendar',
		up: 'fas fa-arrow-up',
		down: 'fas fa-arrow-down',
		previous: 'fas fa-chevron-left',
		next: 'fas fa-chevron-right',
		today: 'fas fa-calendar-check',
		clear: 'far fa-trash-alt',
		close: 'far fa-times-circle'
	}
});

$("#view_stashed").click(function() {
	if ($(this).hasClass('fa-chevron-circle-down')) {
		$(this).removeClass('fa-chevron-circle-down');
		$(this).addClass('fa-chevron-circle-up');
		$('html, body').animate({
			scrollTop: $("#scrollToLocation").offset().top
		}, 400);
	} else {
		$(this).removeClass('fa-chevron-circle-up');
		$(this).addClass('fa-chevron-circle-down');
		$('html, body').animate({
			scrollTop: 0
		}, 400);
	}
});

(function ($) {
	jQuery.expr[':'].Contains = function(a,i,m){
		return (a.textContent || a.innerText || "").toUpperCase().indexOf(m[3].toUpperCase())>=0;
	};

	function listFilter(header, list) {
		input = $(".filterinput");
		$(input)
		.change( function () {
			var filter = $(this).val();
			if(filter) {
				$(list).find("#checker:not(:Contains(" + filter + "))").slideUp();
				$(list).find("#checker:Contains(" + filter + ")").slideDown();
			} else {
				$(list).find("#checker:not(:Contains(" + filter + "))").slideDown();
				$(list).find("#checker:Contains(" + filter + ")").slideDown();
			}
			return false;
		}
)		.keyup( function () {
			$(this).change();
		});
	}
	
	$(function () {
		listFilter($("#header"), $(".searchable"));
	});
}(jQuery));