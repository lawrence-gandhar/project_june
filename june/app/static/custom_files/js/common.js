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
			$(".save_button").prop("disabled", true);
		}else{
			
			if(main_passwd.length < 8){
				$("#passwd1_error").text("This password must contain at least 8 characters.");
			}else{
				$("#passwd1_error").text("");		
				$(".save_button").prop("disabled", false);
				$(".error").text("");
			}
		}
	}else{
		$("#passwd_error").text("Confirm Password is required.");
	}
});


//***********************************************************************
// Validate Password
//***********************************************************************
//

$("#id_password1").on("focusout", function(){
	passwd = $(this).val();
	
	if(passwd.length < 8){
		$("#passwd1_error").text("This password must contain at least 8 characters.");
	}else{
		confirm_passwd = $("#id_password2").val();
		main_passwd = $("#id_password1").val();
			
		if(confirm_passwd!=""){
			if(main_passwd !== confirm_passwd){
				$("#passwd_error").text("Password and Confirm Password does not match");
				$(".save_button").prop("disabled", true);
			}else{
				
				if(main_passwd.length < 8){
					$("#passwd1_error").text("This password must contain at least 8 characters.");
				}else{
					$("#passwd1_error").text("");		
					$(".save_button").prop("disabled", false);
					$(".error").text("");
				}
			}
		}else{
			$("#passwd_error").text("Confirm Password is required.");
		}
		
		$("#passwd1_error").text("");	
	}
});


//***********************************************************************
// On Reset Button Click
//***********************************************************************
//

$("form").on("reset", function(){
	$(".error").text("");
});

//***********************************************************************
// Modal Close
//***********************************************************************
//

$('.modal').on('hidden.bs.modal', function(){
	$("input").val("");
	$(".error").text("");
});


//***********************************************************************
// Change Password
//***********************************************************************
//

function change_password(){
	form_d = $("#change_password_form").serialize();
	
	$("#change_password_modal").modal('hide');
	
	$.post("/change_password/",form_d, function(data){
		alert(data);
	});
}




