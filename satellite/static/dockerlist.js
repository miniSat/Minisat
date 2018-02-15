$(document).ready(function(){
    getDockerImages();   
});

function getDockerImages()
{
    $("#docker_images").html("");
    var com_name = $("#compute_name").val();
    $.ajax({
        url: 'post_local_images',
        data: {
            'com_name': com_name
        },
        dataType: 'json',
        success: function(vals){
            var myTable = document.getElementById("docker_images");
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
}