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
	$('[data-confirm=confirmation]').confirmation({
		rootSelector: '[data-confirm=confirmation]',
			  // other options
			});
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
	} else {
		$(this).removeClass('fa-chevron-circle-up');
		$(this).addClass('fa-chevron-circle-down');
	}
	$('html, body').animate({
		scrollTop: $("#scrollToLocation").offset().top
	}, 400);
});
