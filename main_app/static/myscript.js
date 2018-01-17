//$(document).ready(function(){
//    $("#toast_show").hide();
//    $("#compute_submit").submit(function(){
//        $("#toast_show").show();
//    });
//});

$(document).ready(function(e){
     $("form").submit(function(e){
     var ip_addr=$('#ip_add').val();
     if (validateEmail(ip_addr)) {
            }
     else{
        alert('Invalid  IP Address');
        e.preventDefault();
         }
    });
});

function validateEmail(ip_addr) {
    var filter = /^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/;
    if (filter.test(ip_addr)) {
        return true;
    }
    else {
        return false;
    }
}