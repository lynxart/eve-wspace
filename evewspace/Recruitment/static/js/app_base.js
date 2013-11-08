function UpdateApplicantAPIKeys(app_id){
    $.ajax({
        type: "GET",
        url: '/recruitment/application/' + app_id + '/api/',
        success: function(data){
            $('#api_keys_on_file').html(data);
        },
        error: function(error){
            alert('Unable to get the API key list: \n\n' + error.responseText);
        }
    });
}

function ApplicantAddAPI(app_id){
    $('#api_key_add_btn').prop("disabled", true);
    $('#api_key_add_btn').html('Validating...');
    var data = {
        'key_id': $('#api_key_id').prop('value'),
        'vcode': $('#api_key_vcode').prop('value'),
    };
    $.ajax({
        url: '/recruitment/application/' + app_id + '/api/',
        type: "POST",
        data: data,
        success: function(){
            $('#api_key_add_btn').prop("disabled", false);
            $('#api_key_add_btn').html('Add Key');
            UpdateApplicantAPIKeys(app_id);
        },
        error: function(error){
           var text = '<div class="alert alert-block alert-error"><button type="button" class="close" data-dismiss="alert">&times;</button><strong>Failed:</strong><br />' + error.responseText + '</div>';
            $('#api_alert_placeholder').html(text);
            $('#api_key_add_btn').prop("disabled", false);
            $('#api_key_add_btn').html('Add Key');
        }
    });
}

function ApplicantRemoveAPIKey(key_id, app_id){
    $.ajax({
        url: '/api/key/' + key_id + '/delete/',
        type: 'POST',
        success: function(){
            UpdateApplicantAPIKeys(app_id);
        },
        error: function(error){
            var text = '<div class="alert alert-block alert-error"><button type="button" class="close" data-dismiss="alert">&times;</button><strong>Failed:</strong><br />' + error.responseText + '</div>';
            $('#api_alert_placeholder').html(text);
        }
    });
    return false;
}
