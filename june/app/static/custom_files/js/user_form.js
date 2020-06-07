$(document).ready(function(){
	
	if($("#id_usertype").val()!="0"){
		$("#id_grant_all").prop("checked",false).prop("disabled",true);
	}
	
});


//***********************************************************************
// Check Confirm Password
//***********************************************************************
//

$("#id_password2").on("focusout", function(){
	
	confirm_passwd = $(this).val();
	
	if(confirm_passwd!=""){
		match_fields_data($(this),$("#id_password1"));
	}
});

//***********************************************************************
// Check Usertype
//***********************************************************************
//

$("#id_usertype").on("change", function(){
	if($(this).val()!="0"){
		$("#id_grant_all").prop("checked",false).prop("disabled",true);
	}else{
		$("#id_grant_all").prop("checked",false).prop("disabled",false);
	}
});


function delete_user(ids){
	$.get("/delete_user/"+ids, function(data){
		if(data==1) alert("Error Occurred");
		else{ 
			alert("User Deleted Successfully");
			location.reload();
		}
	});
}






