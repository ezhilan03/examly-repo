$(document).ready(function(){
    $('[data-trigger="dropdown1"]').on('click',function(){
        $('.profile_trigger_dropdown').addClass('active');

        $('[data-trigger="dropdown1"]').on('click',function(){
            $('.profile_trigger_dropdown').removeClass('active');
        });
    });

    $('[data-trigger="dropdown2"]').on('focusin',function(){
        $('.profile_trigger_dropdown2').addClass('active');     
        $('[data-trigger="dropdown2"]').on('focusout',function(){
            $('.profile_trigger_dropdown2').removeClass('active');
        });
    });

    $('[data-trigger="dropdown2"]').on('click',function(event){
        $('.unread_count').remove();
        $.post( "/postmethod", {
            javascript_data: 'yes'
        });
    });
});