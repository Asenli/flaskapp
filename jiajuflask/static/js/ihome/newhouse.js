function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function(){
    // $('.popup_con').fadeIn('fast');
    // $('.popup_con').fadeOut('fast');
})

$.get('/house/area_facility/',function (msg) {
    if (msg.code == '200'){
        area_str = ''
        for(var i=0; i <msg.areas.length; i++){
           console.log(msg.areas[i].name);
            area_option = '<option value=' + msg.areas[i].id +'>'
+ msg.areas[i].name +'</option>';
            area_str += area_option
        }
        $('#area-id').html(area_str);

        for(var j=0; j<msg.facility.length; j++){
            facility_li = '<li><div class="checkbox"><label>';
            facility_li += '<input type="checkbox" name="facility" value="'+msg.facility[j].id+ '">'+ msg.facility[j].name;
            facility_li += '</label></div></li>';
            facility_str += facility_li
        }

        $('.house-facility-list').html(facility_str)
    }
});