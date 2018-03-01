$(document).ready(function(){
    var raw_vm_ip = $("#7").text();
    var raw_compute_ip = $("#10").text();
    var raw_vm_name = $("#2").text();
    var compute_name=$("#10").text();
    vm_ip = raw_vm_ip.split(":")[1].split("/")[0].trim();
    vm_ip = vm_ip.replace(/\./g,'-');
    compute_ip = raw_compute_ip.split("(")[1].split(")")[0].trim();
    compute_ip = compute_ip.replace(/\./g,'-');
    compute_name = compute_name.split(":")[1].split("(")[0].trim();
    vm_name = raw_vm_name.split(":")[1].trim();
    $("#vm-packages-spinner").show();
    $.ajax({
        url: '/get_vm_packages/'+compute_ip+'/'+compute_name+'/'+vm_ip+'/'+vm_name,
        dataType: 'json',
        success: function(result){
            var package_table=document.getElementById("vm_packages_table");
            var package_rows = "";
            for (var each in result['packages'])
            {
                var ele = document.createElement("tr");
                package_rows=package_rows+"<td>"+result['packages'][each]+"</td>";
                ele.innerHTML=package_rows;
                package_table.appendChild(ele);
                package_rows = "";
            }
            $("#vm-packages-spinner").hide();
        }
    });
});

function myFunction() {
    var input, filter, table, tr, td, i;
    input = document.getElementById("myInput");
    filter = input.value.toUpperCase();
    table = document.getElementById("myPackages");
    tr = table.getElementsByTagName("tr");
    for (i = 0; i < tr.length; i++) {
      td = tr[i].getElementsByTagName("td")[0];
      if (td) {
        if (td.innerHTML.toUpperCase().indexOf(filter) > -1) {
          tr[i].style.display = "";
        } else {
          tr[i].style.display = "none";
        }
      }
    }
  }