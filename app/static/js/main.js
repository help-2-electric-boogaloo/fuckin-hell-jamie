$(document).ready(function(){

	$('i.like').click(function(e) {
		
		e.stopPropagation();
		e.preventDefault();

		var like 		= $(this).hasClass('far');
		var image_id 	= $(this).data('image');
		var _this 		= $(this);

		$.getJSON(
			$SCRIPT_ROOT + '/like',

			{
				like: like,
				image_id: image_id
			}, 
			function(result) {
				if (like) {
					_this.removeClass('far');
					_this.addClass('fas');
				} else {
					_this.removeClass('fas');
					_this.addClass('far');
				}
				
			}
		);
	});

	var $grid = $('.grid').masonry({
		gutter: 30
	});


	$('.grid-item figure').click(function(){
		var image_data = $(this).closest('.grid-item').data(image);
		var image = image_data.image;
		var description = `<p>${image.description}</p>`;
		var title = `<h5 class="modal-title">${image.name}<i class="fa fa-times" data-dismiss="modal" aria-label="Close" aria-hidden="true"></i></h5>`;
		var img = ` <figure class="filter-${image.filter}">
						<img class="modal-img" src="${image.upload_location}" alt="${image.name},${image.description}">
					</figure>`;
		$('#image-modal .modal-body').html(img + title + description);
		$('.modal').modal('show');
	});	

	
	if ($('#filter-select').length > 0 ) {
		var filter = $('#filter-select').data('filter');
		$('#filter-select').val(filter);
	}
	
	if ($('#category').length > 0 ) {
		var category = $('#category').data('category');
		$('#category').val(category);
	}
	
	$('#filter-select').change(function(e) {
		var new_filter = 'filter-' + this.value;
		$('#image figure').removeClass();
		$('#image figure').addClass(new_filter);
	});
});


