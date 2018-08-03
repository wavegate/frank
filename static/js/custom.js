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