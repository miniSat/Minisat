$(document).ready(function(e){
     $(document).on('submit','#compute_form',function(e){
     var ip_addr=$('#id_ip_address').val();
     result = validateIP(ip_addr);
     if (result == true) {
        e.preventDefault();
        $.ajax({
            type: 'POST',
            dataType: 'json',
            url: 'post_data',
            data: {
                'name': $("#id_name").val(),
                'ip_address': $("#id_ip_address").val(),
                'root_password': $("#id_root_password").val(),
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
            },
            success: function(data){
                if(Object.keys(data).length == 0)
                {
                    $("#results").html(
                        '<div id="success-div" class="alert alert-success alert-dismissable fade in">\
                        <a href="#" class="close" data-dismiss="alert" aria-label="close">&times;</a>\
                        <strong id="success-box">Successfully Added compute resource</strong>\
                        </div>'
                    );
                }
                else
                {
                    var result = "";
                    for (var each in data){
                        result = result + data[each] + "<br>"
                    }
                    console.log(result);
                    $("#results").html(
                        '<div id="error-div" class="alert alert-danger alert-dismissable fade in">\
                        <a href="#" class="close" data-dismiss="alert" aria-label="close">&times;</a>\
                        <strong id="error-box"></strong>\
                        </div>'
                    );
                    $("#error-box").html(result);
                }
            }
        });
    }
    else if(result == 0){
        $("#results").html(
            '<div class="alert alert-danger alert-dismissable fade in">\
            <a href="#" class="close" data-dismiss="alert" aria-label="close">&times;</a>\
            <strong>'+"Cannot add localhost as compute resource"+'</strong>\
            </div>'
        );
        e.preventDefault();
    }
    else{
        alert('Invalid  IP Address');
        e.preventDefault();
    }
    });

});

function validateIP(ip_addr) {
    var filter = /^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/;
    if (filter.test(ip_addr)) {
        if(ip_addr != "127.0.0.1")
        {
            return true;
        }
        else
        {
            return 0;
        }
    }
    else {
        return false;
    }
}