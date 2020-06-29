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
	main_passwd = $("#id_password1").val();
		
	if(confirm_passwd!=""){
		if(main_passwd !== confirm_passwd){
			$("#passwd_error").text("Password and Confirm Password does not match");
			$("#id_password2").focus();
			$(".save_button").prop("disabled", true);
		}else{
			$(".save_button").prop("disabled", false);
		}
	}else{
		$("#passwd_error").text("confirm Password is required.");
		$("#id_password2").focus();
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






