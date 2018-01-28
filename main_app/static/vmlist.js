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
                    '<li role="presentation"><a role="menuitem" tabindex="-1" id="start" onclick="return start_vm()">Start</a></li>'+
                    '<li role="presentation"><a role="menuitem" tabindex="-1" id = "pause" onclick="return pause_vm()">Pause</a></li>'+
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
                str=str+'<td><div class="dropdown">'+
                    '<button class="btn btn-default dropdown-toggle" type="button" id="action_docker" data-toggle="dropdown">Action'+
                    '<span class="caret"></span></button>'+
                    '<ul class="dropdown-menu" role="menu" aria-labelledby="action_docker">'+
                    '<li role="presentation"><a role="menuitem" tabindex="-1" id="docker_start" onclick="return start_docker()">Start</a></li>'+
                    '<li role="presentation"><a role="menuitem" tabindex="-1" id = "docker_pause" onclick="return pause_docker()">Pause</a></li>'+
                    '</ul></div></td>'
                ele.innerHTML=str;
                myTable.appendChild(ele);
            }
        }
    })
).then(function() {
    $("#spinner").html("");
});
});

function start_vm()
{
alert('Start Vm');
}


function pause_vm()
{
alert('Pause Vm');
}

function start_docker()
{
alert('Start Docker Container');
}


function pause_docker()
{
alert('Pause Docker Container');
}
