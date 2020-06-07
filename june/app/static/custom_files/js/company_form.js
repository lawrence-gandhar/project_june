$(document).ready(function(){});

function delete_company(ids){
    $.get("/delete_company/"+ids,function(data){
		
		if(data==0){ alert("Error Occurred"); }
		else{
			alert("Company and all its data is deleted");
			location.reload();
		}
	});
}

function delete_company_folder(ids){
	$.get("/delete_company_folder/"+ids,function(data){
		
		if(data==0){ alert("Error Occurred"); }
		else{
			alert("Company Folder Removed");
			location.reload();
		}
	});
}