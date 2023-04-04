$(document).ready(function(){
    alert("We are all set!");

    $('#id_total_d').keyup(function(){
        var days = $('#id_total_d').val();
//        var s_name = $('#id_service').val();
//        if(s_name == "Swimming Pool")
//            var amount = 850*days
//        else if(s_name == "Community Hall")
//            var amount = 7000*days
//        else if(s_name == "Picnic Spot")
            var amount = 1000*days
        
        $('#id_total_price').val(amount);
    });
});