$(document).ready(function(){
    var vm_id = $("#vm_id").text().trim();
    var compute_ip = $("#compute_ip").text().trim();
    compute_ip = compute_ip.replace(/\./g,'-');
    $("#vm-packages-spinner").show();
    $("#vm-info-spinner").show();
    $.ajax({
        url: '/get_vm_facts/'+compute_ip+'/'+vm_id,
        dataType: 'json',
        success: function(facts){
            var facts_str = ""
            var index = 1;
            $("#head_vm_name").html(facts["Name"]);
            for (var fact in facts)
            {
                $("#vm_info_font").append("<label id="+index+">"+fact+" : "+facts[fact]+"</label><br>");
                index+=1;
            }
            $("#vm-info-spinner").hide();
            free_memory = parseInt(facts["Free Memory"].split(" ")[0]);
            total_memory = parseInt(facts["Total Allocated Memory"].split(" ")[0]);
            used_memory = total_memory-free_memory;
            var ctxD = document.getElementById("doughnutChart")
            var ChartDetail = new Chart(ctxD, {
                type: 'doughnut',
                data: {
                    labels: ["Free","Used"],
                    datasets: [
                        {
                            data: [free_memory, used_memory],
                            backgroundColor: ["#46BFBD", "#FDB45C"],
                            hoverBackgroundColor: ["#5AD3D1", "#FFC870"],
                            borderWidth: 2
                        }
                    ],
                },
                options: {

                    cutoutPercentage: 75,
                    responsive: true

                },
            });
            get_packages()
        }
    });
});

function get_packages()
{
    var raw_vm_ip = $("#7").text();
    var raw_vm_name = $("#2").text();
    var raw_compute_name=$("#9").text();
    vm_ip = raw_vm_ip.split(":")[1].split("/")[0].trim();
    vm_ip = vm_ip.replace(/\./g,'-');
    compute_ip = raw_compute_name.split("(")[1].split(")")[0].trim();
    compute_ip = compute_ip.replace(/\./g,'-');
    compute_name = raw_compute_name.split(":")[1].split("(")[0].trim();
    vm_name = raw_vm_name.split(":")[1].trim();

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
}

function get_chart_details()

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