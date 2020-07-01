$(document).ready(function(){
	
	if($("#id_usertype").val()!="0"){
		$("#id_grant_all").prop("checked",false).prop("disabled",true);
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

//***********************************************************************
// Delete User
//***********************************************************************
//

function delete_user(ids){
	$.get("/delete_user/"+ids, function(data){
		if(data==1) alert("Error Occurred");
		else{ 
			alert("User Deleted Successfully");
			location.reload();
		}
	});
}

//***********************************************************************
// Reset Password
//***********************************************************************
//

function reset_password(id){
	$.get("/reset_password/"+id+"/", function(data){
		console.log(data);
		
		$("#reset_password").modal('show');
		$("#reset_password_data").empty().text(data);
	});
}





