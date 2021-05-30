function starBars(five_star_content, four_star_content, three_star_content, two_star_content, one_star_content, five_star_condition, four_star_condition, three_star_condition, two_star_condition, one_star_condition, votes_for_content, votes_for_condition)
{
	var content_5_width = (five_star_content/votes_for_content)*100+'%';
	var content_4_width = (four_star_content/votes_for_content)*100+'%';
	var content_3_width = (three_star_content/votes_for_content)*100+'%';
	var content_2_width = (two_star_content/votes_for_content)*100+'%';
	var content_1_width = (one_star_content/votes_for_content)*100+'%';

	var condition_5_width = (five_star_condition/votes_for_condition)*100+'%';
	var condition_4_width = (four_star_condition/votes_for_condition)*100+'%';
	var condition_3_width = (three_star_condition/votes_for_condition)*100+'%';
	var condition_2_width = (two_star_condition/votes_for_condition)*100+'%';
	var condition_1_width = (one_star_condition/votes_for_condition)*100+'%';

	document.querySelector('.content_5_star_inner').style.width = content_5_width;
	document.querySelector('.content_4_star_inner').style.width = content_4_width;
	document.querySelector('.content_3_star_inner').style.width = content_3_width;
	document.querySelector('.content_2_star_inner').style.width = content_2_width;
	document.querySelector('.content_1_star_inner').style.width = content_1_width;

	document.querySelector('.condition_5_star_inner').style.width = condition_5_width;
	document.querySelector('.condition_4_star_inner').style.width = condition_4_width;
	document.querySelector('.condition_3_star_inner').style.width = condition_3_width;
	document.querySelector('.condition_2_star_inner').style.width = condition_2_width;
	document.querySelector('.condition_1_star_inner').style.width = condition_1_width;
}