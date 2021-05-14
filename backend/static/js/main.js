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
	$('.genre-1').hover(function(){
		$('.genre-image-1').css('font-size','xx-large');
	},
	function(){
		$('.genre-image-1').css('font-size','x-large');
	});
	$('.genre-2').hover(function(){
		$('.genre-image-2').css('font-size','xx-large');
	},
	function(){
		$('.genre-image-2').css('font-size','x-large');
	});
	$('.genre-3').hover(function(){
		$('.genre-image-3').css('font-size','xx-large');
	},
	function(){
		$('.genre-image-3').css('font-size','x-large');
	});
	$('.genre-4').hover(function(){
		$('.genre-image-4').css('font-size','xx-large');
	},
	function(){
		$('.genre-image-4').css('font-size','x-large');
	});
	$('.genre-5').hover(function(){
		$('.genre-image-5').css('font-size','xx-large');
	},
	function(){
		$('.genre-image-5').css('font-size','x-large');
	});
	$('.genre-6').hover(function(){
		$('.genre-image-6').css('font-size','xx-large');
	},
	function(){
		$('.genre-image-6').css('font-size','x-large');
	});
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
	});
	$('#star_1').click(function(){
		$('#star_0').attr("src", "../../static/admin_images/rating_fill.png");
		$('#star_1').attr("src", "../../static/admin_images/rating_fill.png");
		$('#star_2').attr("src", "../../static/admin_images/rating.png");
		$('#star_3').attr("src", "../../static/admin_images/rating.png");
		$('#star_4').attr("src", "../../static/admin_images/rating.png");
		$('#ratings').attr("src","../../static/admin_images/unhappy.png");
	});
	$('#star_2').click(function(){
		$('#star_0').attr("src", "../../static/admin_images/rating_fill.png");
		$('#star_1').attr("src", "../../static/admin_images/rating_fill.png");
		$('#star_2').attr("src", "../../static/admin_images/rating_fill.png");
		$('#star_3').attr("src", "../../static/admin_images/rating.png");
		$('#star_4').attr("src", "../../static/admin_images/rating.png");
		$('#ratings').attr("src","../../static/admin_images/ok.png");
	});
	$('#star_3').click(function(){
		$('#star_0').attr("src", "../../static/admin_images/rating_fill.png");
		$('#star_1').attr("src", "../../static/admin_images/rating_fill.png");
		$('#star_2').attr("src", "../../static/admin_images/rating_fill.png");
		$('#star_3').attr("src", "../../static/admin_images/rating_fill.png");
		$('#star_4').attr("src", "../../static/admin_images/rating.png");
		$('#ratings').attr("src","../../static/admin_images/happy.png");
	});
	$('#star_4').click(function(){
		$('#star_0').attr("src", "../../static/admin_images/rating_fill.png");
		$('#star_1').attr("src", "../../static/admin_images/rating_fill.png");
		$('#star_2').attr("src", "../../static/admin_images/rating_fill.png");
		$('#star_3').attr("src", "../../static/admin_images/rating_fill.png");
		$('#star_4').attr("src", "../../static/admin_images/rating_fill.png");
		$('#ratings').attr("src","../../static/admin_images/xtrahappy.png");
	});
	$('#star1_0').click(function(){
		$('#star1_0').attr("src", "../../static/admin_images/rating_fill.png");
		$('#star1_1').attr("src", "../../static/admin_images/rating.png");
		$('#star1_2').attr("src", "../../static/admin_images/rating.png");
		$('#star1_3').attr("src", "../../static/admin_images/rating.png");
		$('#star1_4').attr("src", "../../static/admin_images/rating.png");
		$('#ratings1').attr("src","../../static/admin_images/x_unhappy.png");
	});
	$('#star1_1').click(function(){
		$('#star1_0').attr("src", "../../static/admin_images/rating_fill.png");
		$('#star1_1').attr("src", "../../static/admin_images/rating_fill.png");
		$('#star1_2').attr("src", "../../static/admin_images/rating.png");
		$('#star1_3').attr("src", "../../static/admin_images/rating.png");
		$('#star1_4').attr("src", "../../static/admin_images/rating.png");
		$('#ratings1').attr("src","../../static/admin_images/unhappy.png");
	});
	$('#star1_2').click(function(){
		$('#star1_0').attr("src", "../../static/admin_images/rating_fill.png");
		$('#star1_1').attr("src", "../../static/admin_images/rating_fill.png");
		$('#star1_2').attr("src", "../../static/admin_images/rating_fill.png");
		$('#star1_3').attr("src", "../../static/admin_images/rating.png");
		$('#star1_4').attr("src", "../../static/admin_images/rating.png");
		$('#ratings1').attr("src","../../static/admin_images/ok.png");
	});
	$('#star1_3').click(function(){
		$('#star1_0').attr("src", "../../static/admin_images/rating_fill.png");
		$('#star1_1').attr("src", "../../static/admin_images/rating_fill.png");
		$('#star1_2').attr("src", "../../static/admin_images/rating_fill.png");
		$('#star1_3').attr("src", "../../static/admin_images/rating_fill.png");
		$('#star1_4').attr("src", "../../static/admin_images/rating.png");
		$('#ratings1').attr("src","../../static/admin_images/happy.png");
	});
	$('#star1_4').click(function(){
		$('#star1_0').attr("src", "../../static/admin_images/rating_fill.png");
		$('#star1_1').attr("src", "../../static/admin_images/rating_fill.png");
		$('#star1_2').attr("src", "../../static/admin_images/rating_fill.png");
		$('#star1_3').attr("src", "../../static/admin_images/rating_fill.png");
		$('#star1_4').attr("src", "../../static/admin_images/rating_fill.png");
		$('#ratings1').attr("src","../../static/admin_images/xtrahappy.png");
	});	
});