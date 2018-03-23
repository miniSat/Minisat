function enable_repo(compute_ip, vm_ip, repo_id, vm_name)
{
    $("#action_"+repo_id).prop("disabled", true);
    $.ajax({
        url: '/change_repo_state/'+compute_ip+'/'+vm_ip+'/'+repo_id+'/enable/'+vm_name,
        dataType: 'json',
        success: function(result){
            $("#action_"+repo_id).prop("disabled", false);
        }
    });
}

function disable_repo(compute_ip, vm_ip, repo_id, vm_name)
{
    $("#action_"+repo_id).prop("disabled", true);
    $.ajax({
        url: '/change_repo_state/'+compute_ip+'/'+vm_ip+'/'+repo_id+'/disable/'+vm_name,
        dataType: 'json',
        success: function(result){
            $("#action_"+repo_id).prop("disabled", false);
        }
    })
}


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
            var raw_vm_name = $("#2").text();
            vm_name = raw_vm_name.split(":")[1].trim();
            var raw_vm_ip = $("#7").text();
            vm_ip = raw_vm_ip.split(":")[1].split("/")[0].trim();
            vm_ip = vm_ip.replace(/\./g,'-');
            $.ajax({
                url: '/get_vm_status/'+compute_ip+'/'+vm_name+'/'+vm_ip,
                dataType: 'json',
                success: function(result){
                    if(result["status"]=="running")
                    {
                        $("#card-vm-packages").show()
                        $("#card-vm-repos").show()
                        get_packages()
                        get_added_repo(compute_ip)
                    }
                    else if(result["status"]=="initializing")
                    {
                        $("#head_vm_name").append(" (Preparing VM)")
                    }
                    else if(result["status"]=="shutdown")
                    {
                        $("#head_vm_name").append(" (Turn on VM to browse details)")
                    }
                }
            });
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

function get_added_repo(compute_ip, vm_id)
{
    var raw_vm_ip = $("#7").text();
    vm_ip = raw_vm_ip.split(":")[1].split("/")[0].trim();
    vm_ip = vm_ip.replace(/\./g,'-');
    var raw_vm_name = $("#2").text();
    vm_name = raw_vm_name.split(":")[1].trim();
    $.ajax({
        url: '/get_added_repo/'+compute_ip+'/'+vm_ip+'/'+vm_name,
        dataType: 'json',
        success: function(result){
            var table = document.getElementById("vm_repo_table")
            repo_str = ""
            for (var repo_id in result["enabled"])
            {
                var ele = document.createElement("tr");
                repo_str = repo_str +"<td>"+result["enabled"][repo_id][0]+"</td>"+"<td>"+"Enabled"+"</td>"+"<td>"+result["enabled"][repo_id][1]+"</td>"
                repo_str=repo_str+'<td><div class="dropdown">'+
                    '<button class="btn btn-default dropdown-toggle" type="button" id="action+'+repo_id+'" data-toggle="dropdown">Action'+
                    '<span class="caret"></span></button>'+
                    '<ul class="dropdown-menu" role="menu" aria-labelledby="action">'+
                    '<li role="presentation"><a role="menuitem" tabindex="-1" class="enable_'+repo_id+'" onclick="enable_repo(\''+compute_ip+'\',\''+vm_ip+'\',\''+repo_id+'\',\''+vm_name+'\')">Enable</a></li>'+
                    '<li role="presentation"><a role="menuitem" tabindex="-1" class = "disable_'+repo_id+'" onclick="disable_repo(\''+compute_ip+'\',\''+vm_ip+'\',\''+repo_id+'\',\''+vm_name+'\')">Disable</a></li>'+
                    '</ul></div></td>'

                ele.innerHTML=repo_str
                vm_repo_table.appendChild(ele)
                repo_str=""
            }
            repo_str = ""
            for (var repo_id in result["disabled"])
            {
                var ele = document.createElement("tr");
                repo_str = repo_str +"<td>"+result["disabled"][repo_id]+"</td>"+"<td>"+"Disabled"+"</td>"+"<td>"+"-"+"</td>"
                repo_str=repo_str+'<td><div class="dropdown">'+
                    '<button class="btn btn-default dropdown-toggle" type="button" id="action+'+repo_id+'" data-toggle="dropdown">Action'+
                    '<span class="caret"></span></button>'+
                    '<ul class="dropdown-menu" role="menu" aria-labelledby="action">'+
                    '<li role="presentation"><a role="menuitem" tabindex="-1" class="enable_'+repo_id+'" onclick="enable_repo(\''+compute_ip+'\',\''+vm_ip+'\',\''+repo_id+'\',\''+vm_name+'\')">Enable</a></li>'+
                    '<li role="presentation"><a role="menuitem" tabindex="-1" class = "disable_'+repo_id+'" onclick="disable_repo(\''+compute_ip+'\',\''+vm_ip+'\',\''+repo_id+'\',\''+vm_name+'\')">Disable</a></li>'+
                    '</ul></div></td>'

                ele.innerHTML=repo_str
                vm_repo_table.appendChild(ele)
                repo_str=""
            }
            $("#vm-repo-spinner").hide();
        }
    });
}

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