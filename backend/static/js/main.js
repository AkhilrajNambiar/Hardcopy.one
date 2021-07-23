$(document).ready(function(){
	$('#tap-link1').hover(function(){
		$('#tap1').css("display","inline-block");
	},
	function(){
		$('#tap1').css("display","none");
	});
	$('#tap-link2').hover(function(){
		$('#tap2').css("display","inline-block");
	},
	function(){
		$('#tap2').css("display","none");
	});
	$('#tap-link3').hover(function(){
		$('#tap3').css("display","inline-block");
	},
	function(){
		$('#tap3').css("display","none");
	});
	$('#tap-link4').hover(function(){
		$('#tap4').css("display","inline-block");
	},
	function(){
		$('#tap4').css("display","none");
	});
	$('#tap-link5').hover(function(){
		$('#tap5').css("display","inline-block");
	},
	function(){
		$('#tap5').css("display","none");
	});
	$('#tap-link6').hover(function(){
		$('#tap6').css("display","inline-block");
	},
	function(){
		$('#tap6').css("display","none");
	});

	$('#cap-link1').hover(function(){
		$('#cap1').css("display","inline-block");
	},
	function(){
		$('#cap1').css("display","none");
	});
	$('#cap-link2').hover(function(){
		$('#cap2').css("display","inline-block");
	},
	function(){
		$('#cap2').css("display","none");
	});
	$('#cap-link3').hover(function(){
		$('#cap3').css("display","inline-block");
	},
	function(){
		$('#cap3').css("display","none");
	});
	$('#cap-link4').hover(function(){
		$('#cap4').css("display","inline-block");
	},
	function(){
		$('#cap4').css("display","none");
	});
	$('#cap-link5').hover(function(){
		$('#cap5').css("display","inline-block");
	},
	function(){
		$('#cap5').css("display","none");
	});

	$('#map-link1').hover(function(){
		$('#map1').css("display","inline-block");
	},
	function(){
		$('#map1').css("display","none");
	});
	$('#map-link2').hover(function(){
		$('#map2').css("display","inline-block");
	},
	function(){
		$('#map2').css("display","none");
	});
	$('#login').click(function(){
		$('#Loginmodal').modal('show');
	});
	$('#king').click(function(){
		$('#Loginmodal').modal('hide');
		$('#signupmodal').modal('show');
	});
	$('#algore').click(function(){
		$('#signupmodal').modal('hide');
		$('#Loginmodal').modal('show');
	});
	$('.contributor').click(function(){
		$('#contributemodal').modal('show');
	});
	$('.contorreq').click(function(){
		$('#communitymodal').modal('show');
	});
	// $('.genre-1').hover(function(){
	// 	$('.genre-image-1').css('font-size','xx-large');
	// },
	// function(){
	// 	$('.genre-image-1').css('font-size','x-large');
	// });
	// $('.genre-2').hover(function(){
	// 	$('.genre-image-2').css('font-size','xx-large');
	// },
	// function(){
	// 	$('.genre-image-2').css('font-size','x-large');
	// });
	// $('.genre-3').hover(function(){
	// 	$('.genre-image-3').css('font-size','xx-large');
	// },
	// function(){
	// 	$('.genre-image-3').css('font-size','x-large');
	// });
	// $('.genre-4').hover(function(){
	// 	$('.genre-image-4').css('font-size','xx-large');
	// },
	// function(){
	// 	$('.genre-image-4').css('font-size','x-large');
	// });
	// $('.genre-5').hover(function(){
	// 	$('.genre-image-5').css('font-size','xx-large');
	// },
	// function(){
	// 	$('.genre-image-5').css('font-size','x-large');
	// });
	// $('.genre-6').hover(function(){
	// 	$('.genre-image-6').css('font-size','xx-large');
	// },
	// function(){
	// 	$('.genre-image-6').css('font-size','x-large');
	// });
	$('#edit_profile').click(function(){
		$('#edit_profile').css('display','none');
		$('.updating_form').css('display','block');
		$('.error_msg').css('display','none');
	});
	$('.cancel_btn').click(function(){
		$('#edit_profile').css('display','inline-block');
		$('.updating_form').css('display','none');
	});
	$('#genre_id').change(function(){
		if($(this).val() == 'Non-fiction'){
			$('#sub_genre_id').css('display','block');
		}
		else{
			$('#sub_genre_id').css('display','none');
		}
	});
	$('#star_0').click(function(){
		$('#star_0').attr("src", "../../static/admin_images/rating_fill.png");
		$('#star_1').attr("src", "../../static/admin_images/rating.png");
		$('#star_2').attr("src", "../../static/admin_images/rating.png");
		$('#star_3').attr("src", "../../static/admin_images/rating.png");
		$('#star_4').attr("src", "../../static/admin_images/rating.png");
		$('#ratings').attr("src","../../static/admin_images/x_unhappy.png");
		$('#rating_content').attr('value','1');
	});
	$('#star_1').click(function(){
		$('#star_0').attr("src", "../../static/admin_images/rating_fill.png");
		$('#star_1').attr("src", "../../static/admin_images/rating_fill.png");
		$('#star_2').attr("src", "../../static/admin_images/rating.png");
		$('#star_3').attr("src", "../../static/admin_images/rating.png");
		$('#star_4').attr("src", "../../static/admin_images/rating.png");
		$('#ratings').attr("src","../../static/admin_images/unhappy.png");
		$('#rating_content').attr('value','2');
	});
	$('#star_2').click(function(){
		$('#star_0').attr("src", "../../static/admin_images/rating_fill.png");
		$('#star_1').attr("src", "../../static/admin_images/rating_fill.png");
		$('#star_2').attr("src", "../../static/admin_images/rating_fill.png");
		$('#star_3').attr("src", "../../static/admin_images/rating.png");
		$('#star_4').attr("src", "../../static/admin_images/rating.png");
		$('#ratings').attr("src","../../static/admin_images/ok.png");
		$('#rating_content').attr('value','3');
	});
	$('#star_3').click(function(){
		$('#star_0').attr("src", "../../static/admin_images/rating_fill.png");
		$('#star_1').attr("src", "../../static/admin_images/rating_fill.png");
		$('#star_2').attr("src", "../../static/admin_images/rating_fill.png");
		$('#star_3').attr("src", "../../static/admin_images/rating_fill.png");
		$('#star_4').attr("src", "../../static/admin_images/rating.png");
		$('#ratings').attr("src","../../static/admin_images/happy.png");
		$('#rating_content').attr('value','4');
	});
	$('#star_4').click(function(){
		$('#star_0').attr("src", "../../static/admin_images/rating_fill.png");
		$('#star_1').attr("src", "../../static/admin_images/rating_fill.png");
		$('#star_2').attr("src", "../../static/admin_images/rating_fill.png");
		$('#star_3').attr("src", "../../static/admin_images/rating_fill.png");
		$('#star_4').attr("src", "../../static/admin_images/rating_fill.png");
		$('#ratings').attr("src","../../static/admin_images/xtrahappy.png");
		$('#rating_content').attr('value','5');
	});
	$('#star1_0').click(function(){
		$('#star1_0').attr("src", "../../static/admin_images/rating_fill.png");
		$('#star1_1').attr("src", "../../static/admin_images/rating.png");
		$('#star1_2').attr("src", "../../static/admin_images/rating.png");
		$('#star1_3').attr("src", "../../static/admin_images/rating.png");
		$('#star1_4').attr("src", "../../static/admin_images/rating.png");
		$('#ratings1').attr("src","../../static/admin_images/x_unhappy.png");
		$('#rating_condition').attr('value','1');
	});
	$('#star1_1').click(function(){
		$('#star1_0').attr("src", "../../static/admin_images/rating_fill.png");
		$('#star1_1').attr("src", "../../static/admin_images/rating_fill.png");
		$('#star1_2').attr("src", "../../static/admin_images/rating.png");
		$('#star1_3').attr("src", "../../static/admin_images/rating.png");
		$('#star1_4').attr("src", "../../static/admin_images/rating.png");
		$('#ratings1').attr("src","../../static/admin_images/unhappy.png");
		$('#rating_condition').attr('value','2');
	});
	$('#star1_2').click(function(){
		$('#star1_0').attr("src", "../../static/admin_images/rating_fill.png");
		$('#star1_1').attr("src", "../../static/admin_images/rating_fill.png");
		$('#star1_2').attr("src", "../../static/admin_images/rating_fill.png");
		$('#star1_3').attr("src", "../../static/admin_images/rating.png");
		$('#star1_4').attr("src", "../../static/admin_images/rating.png");
		$('#ratings1').attr("src","../../static/admin_images/ok.png");
		$('#rating_condition').attr('value','3');
	});
	$('#star1_3').click(function(){
		$('#star1_0').attr("src", "../../static/admin_images/rating_fill.png");
		$('#star1_1').attr("src", "../../static/admin_images/rating_fill.png");
		$('#star1_2').attr("src", "../../static/admin_images/rating_fill.png");
		$('#star1_3').attr("src", "../../static/admin_images/rating_fill.png");
		$('#star1_4').attr("src", "../../static/admin_images/rating.png");
		$('#ratings1').attr("src","../../static/admin_images/happy.png");
		$('#rating_condition').attr('value','4');
	});
	$('#star1_4').click(function(){
		$('#star1_0').attr("src", "../../static/admin_images/rating_fill.png");
		$('#star1_1').attr("src", "../../static/admin_images/rating_fill.png");
		$('#star1_2').attr("src", "../../static/admin_images/rating_fill.png");
		$('#star1_3').attr("src", "../../static/admin_images/rating_fill.png");
		$('#star1_4').attr("src", "../../static/admin_images/rating_fill.png");
		$('#ratings1').attr("src","../../static/admin_images/xtrahappy.png");
		$('#rating_condition').attr('value','5');
	});	
	if($('.searchbox').css('display','none')){
		$('#search').click(function(){
			$('.searchbox').css("display","inline");
			$('#search').css('display','none');
		});
	}
	$('.search_close').click(function(){
		$('.searchbox').css('display','none');
		$('#search').css('display','inline');
	});
	$('.address_update').click(function(){
		$('#update_my_address').css('display','block');
		$('.address_update').css('display','none');
	});
	$('.cancel_address_change').click(function(){
		$('#update_my_address').css('display','none');
		$('.address_update').css('display','inline');
	});
	$('#upload_form').on('submit', function(event){
		event.preventDefault();

		var formData = new FormData($('#upload_form')[0]);

		$.ajax({
			xhr: function(){
				var xhr = new window.XMLHttpRequest();
				xhr.upload.addEventListener('progress', function(e){
					if(e.lengthComputable){
						console.log('Bytes Loaded: ' + e.loaded);
						console.log('Total size ' + e.total);
						console.log('Percentage loaded' + (e.loaded/e.total));

						var percent = Math.round((e.loaded/e.total)*100);

						$('#progressBar').attr('aria-valuenow', percent).css('width', percent+'%').text(percent+'%');
					}
				});
				return xhr;
			},
			type: 'POST',
			url: '/upload',
			data: formData,
			processData: false,
			contentType: false,
			success: function(data){
				if(data["status"] == "1"){
					alert("Your book was successfully uploaded!");
					window.location.href = '/home';
				}
			}
		});
	});
});