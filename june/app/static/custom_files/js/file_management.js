$(document).ready(function(){

	var row_list = Object.keys(wrong_list);	

    $("table.dataframe").addClass("table table-responsive");
	$("table.dataframe").css("font-size","11px");
    $("table.dataframe th").attr("style",'background: #000000; opacity:0.7; color:#FFFFFF; padding:10px; font-weight:bold;');

    for(i=0;i<row_list.length;i++){
        $(".dataframe tr:eq("+(parseInt(row_list[i])+1)+")").css({"background-color":"rgba(255, 0, 0, 0.2)", "color":"#000000"});
		
		row_index = parseInt(row_list[i])+1;
		
		for( x=0; x < wrong_list[parseInt(row_list[i])].length; x++){
			
			col_index = parseInt(wrong_list[parseInt(row_list[i])][x])
			
			$('.dataframe tr:eq('+(row_index)+') td:eq('+col_index+')').css({"background-color":"rgba(255, 0, 0)", "color":"#000000"});
		}	
	}
});

function show_errors(){
    $(".dataframe tr").hide();

    $(".dataframe tr:eq(0)").show(); 
    for(i=0;i<wrong_list.length;i++){
        $(".dataframe tr:eq("+(parseInt(wrong_list[i])+1)+")").show(); 
    }

    $("#show_errors, #hide_errors").hide();
    $("#show_data").show();
}

function show_data(){
    $(".dataframe tr").show();

    $("#show_errors, #hide_errors").show();
    $("#show_data").hide();
}

function hide_errors(){
    $(".dataframe tr").show();

    $(".dataframe tr:eq(0)").show(); 
    for(i=0;i<wrong_list.length;i++){
        $(".dataframe tr:eq("+(parseInt(wrong_list[i])+1)+")").hide(); 
    }

    $("#show_errors, #hide_errors").hide();
    $("#show_data").show();
}