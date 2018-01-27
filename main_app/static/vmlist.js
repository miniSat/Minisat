$(document).ready(function(){
    $.ajax({
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
                ele.innerHTML=str;
                myTable.appendChild(ele);
            }
        }
    });
});