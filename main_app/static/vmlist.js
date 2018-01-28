$(document).ready(function(){
$.when(
    $.ajax({ // First Request
        url: 'get_virtual_mc',
        dataType: 'json',
        success: function (vals) {
            var myTable = document.getElementById("vm_table");
            for (var newitem in vals)
            {
                var ele = document.createElement("tr");
                each_vm = vals[newitem].toString().split(",");
                var str = "";
                for (var item in each_vm)
                {
                    str= str+"<td>"+each_vm[item]+"</td>";
                }
                str=str+'<td><div class="dropdown">'+
                    '<button class="btn btn-default dropdown-toggle" type="button" id="action" data-toggle="dropdown">Action'+
                    '<span class="caret"></span></button>'+
                    '<ul class="dropdown-menu" role="menu" aria-labelledby="action">'+
                    '<li role="presentation"><a role="menuitem" tabindex="-1" id="start" onclick="start_vm(\''+each_vm[1]+'\',\''+each_vm[3]+'\')">Start</a></li>'+
                    '<li role="presentation"><a role="menuitem" tabindex="-1" id = "pause" onclick="pause_vm(\''+each_vm[1]+'\',\''+each_vm[3]+'\')">Pause</a></li>'+
                    '</ul></div></td>'
                ele.innerHTML=str;
                myTable.appendChild(ele);
            }
        }
    }),
    
    $.ajax({ //Seconds Request
        url: 'get_running_containers',
        dataType: 'json',
        success: function (vals) {
            var myTable = document.getElementById("docker_table");
            for (var newitem in vals)
            {
                var ele = document.createElement("tr");
                each_vm = vals[newitem].toString().split(",");
                var str = "";
                for (var item in each_vm)
                {
                    str= str+"<td>"+each_vm[item]+"</td>";
                }
                ele.innerHTML=str;
                myTable.appendChild(ele);
            }
        }           
    })
).then(function() {
    $("#spinner").html("");
});
});

function start_vm(name,compute_name)
{
alert('Start '+name);
$.ajax({
    url: 'vm_start',
    data: {
        'vm_name':name,
        'compute_name':compute_name
    },
    dataType: 'json',
    success: function(vals){
        alert(vals.status);
    }
});
}


function pause_vm(name,compute_name)
{
alert('Pause '+name);
$.ajax({
    url: 'vm_pause',
    data: {
        'vm_name':name,
        'compute_name':compute_name
    },
    dataType: 'json',
    success: function(vals){
        alert(vals.status);
    }
});
}
