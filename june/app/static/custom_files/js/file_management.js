$(document).ready(function(){

    $("table.dataframe").addClass("table table-responsive");
    $("table.dataframe th").attr("style",'background: #9be327; color:#000000; font-weight:bold;');

    for(i=0;i<wrong_list.length;i++){
        $(".dataframe tr:eq("+(parseInt(wrong_list[i])+1)+")").css({"background-color":"rgba(255, 0, 0, 0.59)", "color":"#FFFFFF"});
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