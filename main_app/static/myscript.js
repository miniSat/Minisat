
$(document).ready(function(e){
     $("#compute_form").submit(function(e){
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

//Toast Msg function

function myFunction() {
    var x = document.getElementById("snackbar")
    x.className = "show";
    setTimeout(function(){ x.className = x.className.replace("show", ""); }, 5000);
}