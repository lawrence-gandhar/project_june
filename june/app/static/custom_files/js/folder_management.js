$(document).ready(function(){});

/************************************************************/
// ON FOLDER HOVER
/************************************************************/

$(".folder-item").hover(
  function() {
    $(this).find(".settings_icon").show();	
  }, function() {
    $(".settings_icon").hide();
  }
);

/************************************************************/
// DELETE FOLDER
/************************************************************/

function delete_folder(ids){
	$.get("/delete_folder/"+ids+"/",function(data){
		if(data==1) location.reload();
		else alert("Unknown Error Code");
	});
}