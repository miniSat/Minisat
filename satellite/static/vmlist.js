$(document).ready(function(){
    ajax_containers()
    ajax_vm()
});

function start_vm(name,compute_name)
{
    $("#action_"+name).prop("disabled", true);
    $("#vm-spinner").show();
    $.ajax({
        url: 'vm_start',
        data: {
            'vm_name':name,
            'compute_name':compute_name
        },
        dataType: 'json',
        success: function(vals){
            $("#dash_vms "+"#"+vals.vm_name+" .vm_status").html("<p style='color:green'>Running</p>");
            $("#vm-spinner").hide();
            $("#action_"+name).prop("disabled", false);
        }
    });
}


function pause_vm(name,compute_name)
{
    $("#action_"+name).prop("disabled", true);
    $("#vm-spinner").show();
    $.ajax({
        url: 'vm_pause',
        data: {
            'vm_name':name,
            'compute_name':compute_name
        },
        dataType: 'json',
        success: function(vals){
            $("#dash_vms "+"#"+vals.vm_name+" .vm_status").html("<p style='color:red'>Shutdown</p>");
            $("#vm-spinner").hide();
            $("#action_"+name).prop("disabled", false);
        }
    });
}

function start_docker_cont(cont_name, compute_name)
{
    $("#action_"+name).prop("disabled", true);
    $("#cont-spinner").show();
    $.ajax({
        url: '/containers/start_container/',
        dataType: 'json',
        data: {
            'cont_name': cont_name,
            'compute_name': compute_name
        },
        success: function(vals){
            console.log(vals);
            $("#dash_cont "+"#"+vals.cont_name+" .cont_status").html("<p style='color:green'>Running</p>");
            $("#cont-spinner").hide();
            $("#action_"+name).prop("disabled", false);
        }
    });
}


function pause_docker_cont(cont_name, compute_name)
{
    $("#action_"+name).prop("disabled", true);
    $("#cont-spinner").show();
    console.log(cont_name+" "+compute_name);
    $.ajax({
        url: '/containers/pause_container/',
        dataType: 'json',
        data: {
            'cont_name': cont_name,
            'compute_name': compute_name
        },
        success: function(vals){
            console.log(vals);
            $("#dash_cont "+"#"+vals.cont_name+" .cont_status").html("<p style='color:red'>Paused</p>");
            $("#cont-spinner").hide();
            $("#action_"+name).prop("disabled", false);
        }
    });
}



function ajax_vm(){
    $("#vm-spinner").show();
    $.ajax({
        url: 'get_virtual_mc',
        cache: false,
        dataType: 'json',
        success: function (vals) {
            var myTable = document.getElementById("vm_table");
            "error" in vals
            {
                for (var err in vals['error'])
                {
                    $("#error-vm").html(vals['error'][err]);
                    $("#error-box-vm").show();
                }
                delete vals['error']
            }
            for (var newitem in vals)
            {
                var ele = document.createElement("tr");
                each_vm = vals[newitem].toString().split(",");
                ele.setAttribute("id",each_vm[1]);
                var str = "";
                str= str+"<td class='vm_id'><a href='"+each_vm[3]+"/"+each_vm[0]+"' >"+each_vm[0]+"</a></td>";
                str= str+"<td class='vm_name'>"+each_vm[1]+"</td>";
                str= str+"<td class='vm_status'>"+each_vm[2]+"</td>";
                str= str+"<td class='vm_compute'>"+each_vm[3]+' ('+each_vm[4]+' )'+"</td>";
                str=str+'<td><div class="dropdown">'+
                    '<button class="btn btn-default dropdown-toggle" type="button" id="action_'+each_vm[1]+'" data-toggle="dropdown">Action'+
                    '<span class="caret"></span></button>'+
                    '<ul class="dropdown-menu" role="menu" aria-labelledby="action">'+
                    '<li role="presentation"><a role="menuitem" tabindex="-1" class="start_'+each_vm[1]+'" onclick="start_vm(\''+each_vm[1]+'\',\''+each_vm[3]+'\')">Start</a></li>'+
                    '<li role="presentation"><a role="menuitem" tabindex="-1" class = "pause_'+each_vm[1]+'" onclick="pause_vm(\''+each_vm[1]+'\',\''+each_vm[3]+'\')">Shutdown</a></li>'+
                    '</ul></div></td>'
//                $("#this-"+each_vm[0]).attr("href","vm_info/"+each_vm[0]);
                ele.innerHTML=str;
                myTable.appendChild(ele);
            }
             $('#vm_table td.vm_status').each(function(){
                if ($(this).text() == 'running') {
                    $(this).css('color','green');
                    $(this).text("Running");
                }
                else {
                    $(this).css('color','red');
                    $(this).text("Shutdown");
                }
            });
            $("#vm-spinner").hide();
        }
    });
}
function ajax_containers() {
    $("#cont-spinner").show();
    $.ajax({
        url: 'get_running_containers',
        dataType: 'json',
        cache: false,
        success: function (vals) {
            var myTable = document.getElementById("docker_table");
            "error" in vals
            {
                for (var err in vals['error'])
                {
                    $("#error-cont").html(vals['error'][err]);
                    $("#error-box-cont").show();
                }
                delete vals['error']
            }
            for (var newitem in vals)
            {
                var ele = document.createElement("tr");
                each_cont = vals[newitem].toString().split(",");
                ele.setAttribute("id",each_cont[0]);
                var str = "";
                str= str+"<td class='cont_name'>"+each_cont[0]+"</td>";
                str= str+"<td class='cont_repo'>"+each_cont[1]+"</td>";
                str= str+"<td class='cont_port'>"+each_cont[2]+"</td>";
                str= str+"<td class='cont_compute'>"+each_cont[3]+' ('+each_cont[6]+' )'+"</td>";
                str= str+"<td class='cont_status'>"+each_cont[4]+"</td>";
                str=str+'<td><div class="dropdown">'+
                    '<button class="btn btn-default dropdown-toggle" type="button" id="action_'+each_cont[1]+'" data-toggle="dropdown">Action'+
                    '<span class="caret"></span></button>'+
                    '<ul class="dropdown-menu" role="menu" aria-labelledby="action_docker">'+
                    '<li role="presentation"><a role="menuitem" tabindex="-1" id="docker_start" onclick="return start_docker_cont(\''+each_cont[0]+'\',\''+each_cont[3]+'\')">Start</a></li>'+
                    '<li role="presentation"><a role="menuitem" tabindex="-1" id = "docker_pause" onclick="return pause_docker_cont(\''+each_cont[0]+'\',\''+each_cont[3]+'\')">Pause</a></li>'+
                    '</ul></div></td>'
                ele.innerHTML=str;
                myTable.appendChild(ele);
            }
            $('#docker_table td.cont_status').each(function(){
                if ($(this).text() == 'Paused') {
                    $(this).css('color','red');
                }
                else {
                    $(this).css('color','Green');
                    $(this).text("Running");
                }
            });
            $("#cont-spinner").hide();
        }
    });
}

