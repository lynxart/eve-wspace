function GetApplication(app_id){
    $.ajax({
        type: "GET",
        url: '/recruitment/application/' + app_id + '/edit/',
        success: function(data){
            $('#app' + app_id).html(data);
        },
        error: function(error){
            alert('Unable to load application: \n\n' + error.responseText);
        }
    });
}

function UpdateApplication(app_id){
    $.ajax({
        type: "POST",
        url: '/recruitment/application/' + app_id + '/edit/',
        data: $('#app'+app_id+'Form').serialize(),
        success: function(data){
            GetApplication(app_id);
        },
        error: function(error){
            alert('Unable to save application: \n\n' + error.responseText);
        }
    });
}

function UpdateApplicationStage(app_id, stage_id){
    $.ajax({
        type: "GET",
        url: '/recruitment/application/' + app_id + '/stage/' + stage_id + '/edit/',
        success: function(data){
            $('#stage'+stage_id).html(data);
        },
        error: function(error){
            alert('Unable to load the application stage: \n\n' + error.responseText);
        }
    });
}

function EditApplicationStageInfo(app_id, stage_id){
    $.ajax({
        type: "POST",
        url: '/recruitment/application/' + app_id + '/stage/' + stage_id + '/edit/',
        data: $('#stage'+stage_id+'Form').serialize(),
        success: function(data){
            GetApplicationStage(app_id, stage_id);
        },
        error: function(error){
            alert('Unable to save application stage: \n\n' + error.responseText);
        }
    });
}

function GetQuestionEditDialog(app_id, stage_id, question_id){
    $.ajax({
        type: "GET",
        success: function(data){
            $('#modalHolder').html(data).modal('show');
        },
        error: function(error){
            alert('Unable to load the quesiton form: \n\n' + error.responseText);
        }
    });

}

function SaveQuestion(app_id, stage_id, question_id){
    $.ajax({
        type: "POST",
        url: '/recruitment/application/' + app_id + '/stage/' + stage_id + '/question/' + question_id + '/',
        data: $('#question'+question_id+'Form').serialize(),
        success: function(data){
            GetApplicationStage(app_id, stage_id);
        },
        error: function(error){
            alert('Unable to save the question: \n\n' + error.responseText);
        }
    });
}
