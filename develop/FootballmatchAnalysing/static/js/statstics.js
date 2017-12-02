window.onload = function(){ 
	var host_recent_odd_result=new Array();
	var host_recent_daxiao=new Array();
	var away_recent_odd_result=new Array();
	var away_recent_daxiao=new Array();
	var host_recent_same_odd_result=new Array();
	var host_recent_same_daxiao=new Array();
	var away_recent_same_odd_result=new Array();
	var away_recent_same_daxiao=new Array();
　　$("#host_rencent_match > tbody > tr").each(function(i, n){ 
　　    if (i > 1 && i < 12){
			host_recent_odd_result.push($(n).find('td:eq(6)')[0].innerHTML);
			host_recent_daxiao.push($(n).find('td:eq(7)')[0].innerHTML);
		}
	});
	$("#away_rencent_match > tbody > tr").each(function(i, n){ 
　　    if (i > 1 && i < 12){
			away_recent_odd_result.push($(n).find('td:eq(6)')[0].innerHTML);
			away_recent_daxiao.push($(n).find('td:eq(7)')[0].innerHTML);
		}
	});
	$("#host_rencent_same_match > tbody > tr").each(function(i, n){ 
　　    if (i > 1 && i < 12){
			host_recent_same_odd_result.push($(n).find('td:eq(6)')[0].innerHTML);
			host_recent_same_daxiao.push($(n).find('td:eq(7)')[0].innerHTML);
		}
	});
	$("#away_rencent_same_match > tbody > tr").each(function(i, n){ 
　　    if (i > 1 && i < 12){
			away_recent_same_odd_result.push($(n).find('td:eq(6)')[0].innerHTML);
			away_recent_same_daxiao.push($(n).find('td:eq(7)')[0].innerHTML);
		}
	});
	var count = 0;
	for(var i=0;i<host_recent_odd_result.length;i++){
		if(host_recent_odd_result[i] == '赢'){
			count++;
		}
	}
	var host_recent_odd_result_str = '赢盘率：'+count+'0.0%   ';
	count = 0;
	for(var i=0;i<host_recent_daxiao.length;i++){
		if(host_recent_daxiao[i] == '大'){
			count++;
		}
	}
	var host_recent_daxiao_str = '大球率：'+count+'0.0%   ';
	$('#host_recent_match_summary').html(host_recent_odd_result_str + host_recent_daxiao_str);
	count = 0;
	for(var i=0;i<away_recent_odd_result.length;i++){
		if(away_recent_odd_result[i] == '赢'){
			count++;
		}
	}
	var away_recent_odd_result_str = '赢盘率：'+count+'0.0%   ';
	count = 0;
	for(var i=0;i<away_recent_daxiao.length;i++){
		if(away_recent_daxiao[i] == '大'){
			count++;
		}
	}
	var away_recent_daxiao_str = '大球率：'+count+'0.0%   ';
	$('#away_recent_match_summary').html(away_recent_odd_result_str + away_recent_daxiao_str);
	count = 0;
	for(var i=0;i<host_recent_same_odd_result.length;i++){
		if(host_recent_same_odd_result[i] == '赢'){
			count++;
		}
	}
	var host_recent_same_odd_result_str = '赢盘率：'+count+'0.0%   ';
	count = 0;
	for(var i=0;i<host_recent_same_daxiao.length;i++){
		if(host_recent_same_daxiao[i] == '大'){
			count++;
		}
	}
	var host_recent_same_daxiao_str = '大球率：'+count+'0.0%   ';
	$('#host_recent_match_same_summary').html(host_recent_same_odd_result_str + host_recent_same_daxiao_str);
	count = 0;
	for(var i=0;i<away_recent_same_odd_result.length;i++){
		if(away_recent_same_odd_result[i] == '赢'){
			count++;
		}
	}
	var away_recent_same_odd_result_str = '赢盘率：'+count+'0.0%   ';
	count = 0;
	for(var i=0;i<away_recent_same_daxiao.length;i++){
		if(away_recent_same_daxiao[i] == '大'){
			count++;
		}
	}
	var away_recent_same_daxiao_str = '大球率：'+count+'0.0%   ';
	$('#away_recent_match_same_summary').html(away_recent_same_odd_result_str + away_recent_same_daxiao_str);
	count = 0;
}