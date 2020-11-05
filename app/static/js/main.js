$(document).ready(function(){

	$('i.like').click(function(e) {
		/*This listens for a click on a like icon. Upon click, the image ID (associated with whichever like icon was clicked) is placed into the user's 
		'liked images' or 'unliked images' list within the DB. It also allows the appearance of the like button to be changed upon click, as the displayed class of the 
		button's appearance changes to the other possible class value. */
		
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
		/*This function listens for a user click on an image defined within the 'grid item' class. Upon click, the modal class of the image is displayed, 
		along with all of the previously created variables defined for values such as: name, description, etc.  */ 

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


	/* This displays the selected filter on the associated image.*/ 
	if ($('#filter-select').length > 0 ) {
		var filter = $('#filter-select').data('filter');
		$('#filter-select').val(filter);
	}
	/* Allows a catergory to be selected for the associated image, allowing it to be displayed in its specific catergory along with other images which have the same catergory.*/ 
	if ($('#category').length > 0 ) {
		var category = $('#category').data('category');
		$('#category').val(category);
	}
	/* Allows the filter of an image to be changed to another filter*/
	$('#filter-select').change(function(e) {
		var new_filter = 'filter-' + this.value;
		$('#image figure').removeClass();
		$('#image figure').addClass(new_filter);
	});
});


