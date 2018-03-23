function host_group_change(){
    var host_group = $("#select_host_group").val();

    $.get("host_group_data", { host_group: host_group }).done(function(data){

        $('[name=select_compute] option').filter(function() {
            return ($(this).text() == data.compute);
        }).prop('selected', true);

        $('[name=activation_name] option').filter(function() {
            return ($(this).text() == data.activation_key);
        }).prop('selected', true);

        $('[name=select_vm_profile] option').filter(function() {
            return ($(this).text() == data.profile);
        }).prop('selected', true);

        $('[name=vm_os] option').filter(function() {
            return ($(this).text() == data.operating_system);
        }).prop('selected', true);
    });
}