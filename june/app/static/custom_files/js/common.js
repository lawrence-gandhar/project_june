$(document).ready(function(){
	$("input").each(function(){
		if(!$(this).hasClass("form-control")){
			$(this).addClass("form-control");
		}
	});
});


//***********************************************************************
// Match Two Strings
//***********************************************************************
//

function match_fields_data(input1, input2, elem=null){
	
	var field1 = $(input1).val();
	var field2 = $(input2).val();
	
	if(field1 !== field2){		
		if(elem) $(elem).text("Both fields should match. It is case-sensitive");
		$(input1).addClass("is-invalid");
		$(input2).addClass("is-invalid");
		alert("Did not match");
	}else{
		$(input1).removeClass("is-invalid");
		$(input2).removeClass("is-invalid");
	}
}