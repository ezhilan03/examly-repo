$(document).ready(function(){
    var dropdown1_flag = 0;
    var dropdown2_flag = 0;
    $('[data-trigger="dropdown1"]').on('click',function(){
        if(dropdown1_flag==0){
            $('.profile_trigger_dropdown').addClass('active');
            dropdown1_flag=1;
        }
        else if(dropdown1_flag==1){
            $('.profile_trigger_dropdown').removeClass('active');
            dropdown1_flag=0;
        }
    });

    $('[data-trigger="dropdown2"]').on('click',function(){
        if(dropdown2_flag==0){
            $('.profile_trigger_dropdown2').addClass('active');
            dropdown2_flag=1;
        }
        else if(dropdown2_flag==1){
            $('.profile_trigger_dropdown2').removeClass('active');
            dropdown2_flag=0;
        }
    });

    $('[data-trigger="dropdown2"]').on('click',function(event){
        if($('.unread_count')['length'] > 0){
            var name_value = $('.name_value').html();
            $('.unread_count').remove();
            $.post( "/unread_to_read", {
                javascript_data: name_value
            });
        }

    });

    $('.new a').on('click',function(event){
        if($(this).find("span").length==1){
            $(this).find("span").remove();
            $.post( "/to_clicked", {
                javascript_data: $(this).data('message-id')
            }); 
        }
    
    });

    $('.older a').on('click',function(event){
        if($(this).find("span").length==1){
            $(this).find("span").remove();
            $.post( "/to_clicked", {
                javascript_data: $(this).data('message-id')
            }); 
        }
    });
});