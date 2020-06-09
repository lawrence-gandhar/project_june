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


/************************************************************/
// CHECK FILE EXTENSION
/************************************************************/

function checkfile(sender) {
  var validExts = new Array(".xlsx", ".xls");
  var fileExt = sender.value;
  fileExt = fileExt.substring(fileExt.lastIndexOf('.'));
  if (validExts.indexOf(fileExt) < 0) {
    alert("Invalid file selected, valid files are of " +
             validExts.toString() + " types.");
    $(sender).val("");
    return false;
  }
  else return true;
}