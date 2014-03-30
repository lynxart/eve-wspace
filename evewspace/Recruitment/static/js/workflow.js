$(document).ready(function(){ GetWorkflowList(); });

function GetWorkflowList(){
    $.ajax({
        type: "GET",
        url: "/recruitment/workflow/",
        success: function(data){
            $('#workflow_holder').html(data);
        }
    });
}

function GetAddWorkflowDialog(){
    $.ajax({
        type: "GET",
        url: "/recruitment/workflow/new/",
        success: function(data){
            $('#modalHolder').html(data).modal('show');
        }
    });
}

function SaveNewWorkflowAction() {
    $.ajax({
        type: "POST",
        url: "/recruitment/workflow/new/",
        data: $('#add-workflow-item-form').serialize(),
        success: function(){
            $('#modalHolder').modal('hide');
            GetWorkflowList();
        }
    });
}
