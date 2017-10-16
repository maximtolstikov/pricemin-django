$(document).ready(function () {
    var intervalIDbutton;
    var intervalIDblock;
    var i = 0;
    var click_count = 0;
    //переберает блоки в списке и меняет их вид на первой странице
    function light_block() {
        if (i>9) {
            clearInterval(intervalIDblock);
        } else {
            $('div.block').eq(i).css({
                         'border-left': '2px solid white',
                         'border-top': '2px solid white',
                         'border-right': '2px solid white',
                         'border-bottom': '4px solid white',
                         'background-color':'#9db8d2'
                         });
            $('div.block').eq(i-1).css({
                         'border-left': '1px solid grey',
                         'border-top': '1px solid grey',
                         'border-right': '1px solid grey',
                         'border-bottom': '3px solid grey',
                          });
            i++;
        }                   
    }
    //управление сменой страниц и выполнение на них анимации
    $('.button_right').click(function (event) {
        event.preventDefault();
        if (click_count==0) {
            $('#start_text').fadeOut('slow');
//            $('.buttons_panel').fadeOut('fast');
            $('.colon_left').fadeIn('slow');
            $('.colon_right').fadeIn('slow');
            $('#block_text_left').text('');
            $('#block_text_right').css(
               {'padding-top':'10%'}).text('Это список с которым мы будем работать.');
            $('.button_right').text('Далее');
            $('.list').fadeIn('slow');
            $('.button_right').css({'bottom':'5px', 'right':'5px', 'padding':'2%'});
            $('.button_left').css({'bottom':'5px', 'left':'5px', 'padding':'2%'});
             intervalIDblock = setInterval(light_block, 50); 
             click_count++;
        } else if (click_count==1) {
           $('#block_text_right').text('Это кнопки управления списком. Покликайте по ним, что бы узнать для чего они.');
           $('.div_list').fadeOut('slow');  
           $('.buttons_panel').fadeIn('slow'); 
   //        intervalIDbutton = setInterval(visual_button, 200);
           click_count++;
        } else if (click_count==2) {
            button_count = 0
            $('#block_text_left').text('Шаг 1');
            $('#block_text_right').text('Когда откроется подобный список, Вы сможете выбрать свой регион. Пока это просто demo-версия.');
            $('.div_list').fadeIn('slow').removeClass('div_list_border');
            $('.buttons_panel').removeClass('buttons_panel_border');
            $('.block').css('background-color','white');
            $('.b1').text('23 Краснодарский край');  
            $('.b2').text('24 Красноярский край');
            $('.b3').text('25 Приморский край');
            $('.b4').text('26 Ставропльский край');
            $('.b5').text('27 Хабаровский край');
            $('.b6').text('28 Амурская область');
            $('.b7').text('29 Архангельская область');
            $('.b8').text('30 Астраханская область');
            $('.b9').text('31 Белгородская область');
            click_count++;    
        } else if (click_count==3) {
            $('#block_text_left').text('Шаг 2');
            $('#block_text_right').css(
               {'padding-top':'10%'}).text('По аналогии с региональным списком, здесь Вам потребуется выбрать свой город. Если Вашего города, вдруг, не окажется, Вы всегда сможете его добавить далее, в основной программе, с помощью одноименной кнопки.');
            $('.div_list').css({'padding-top':'33%'});
            $('.b1').text('27 Хабаровскй край').css(
                            {'background-color':'blue', 'color':'white'});
            $('.b2').text('Амурск');  
            $('.b3').text('Комсомольск-на-Амуре');
            $('.b4').text('Хабаровск');
            $('.b5').fadeOut(10);
            $('.b6').fadeOut(10);
            $('.b7').fadeOut(10);
            $('.b8').fadeOut(10);
            $('.b9').fadeOut(10);
            click_count++;    
        } else if (click_count==4) {
            $('#block_text_left').text('Шаг 3');
            $('#block_text_right').css({'padding-top':'10%'}).text('Так будет выглядеть домашняя страница города. Незабудте закрепить её в закладки браузера, что-бы в дальнейшем избегать повторного выбора.');
            $('.b1').text('Хабаровск').css(
                            {'background-color':'blue', 'color':'white'});
            $('.b2').text('Цены в магазине').css(
                            {'background-color':'orange'});  
            $('.b3').text('Цены в городе').css(
                            {'background-color':'aqua'});
            $('.b4').text('События').css(
                            {'background-color':'lightgreen'});
            click_count++;    
        } else if (click_count==5) {
            $('#block_text_left').text('Цены добавляются в магазине.');
            $('#block_text_right').css({'padding-top':'10%'}).text('Выбрать или добавить новый магазин Вы сможете далее в программе.');
            $('.b1').text('').css({'background-color':''});
            $('.b2').text('Цены в магазине').css({'background-color':'orange'});  
            $('.b3').text('').css({'background-color':''});
            $('.b4').text('').css({'background-color':''});
            click_count++;    
        } else if (click_count==6) {
            $('#block_text_left').text('Что бы узнать какие есть цены в городе:');
            $('#block_text_right').text('В программе будет предусмотрен такой поиск.');
            $('.b2').text('').css({'background-color':''});  
            $('.b3').text('Цены в городе').css({'background-color':'aqua'});
            $('.button_right').text('Пробуйте');
            click_count++;    
        } else if (click_count==7) {
             //Переход             
              $(location).attr('href', 'http://pricemin.ru/des');
        }                                                        
    });
    // Если на второй странице навести курсор на кнопки то отобразится
    // название кнопки
    $('.img_home').click(function(){
        $('#block_text_left').text('Домой').append($('<p style="font-style: italic; font-size: x-large">').text('- будет возвращать Вас на домашнюю страницу города'));
    });
    $('.img_up').click(function(){
        $('#block_text_left').text('Назад').append($('<p style="font-style: italic; font-size: x-large">').text('- возвращает на предыдущую позицию. Конечно, можно использовать кнопки браузера, но при этом данные не станут обновлятся. Лучше использовать программные кнопки.'));
    });
    $('.img_add').click(function(){
        $('#block_text_left').text('Добавить').append($('<p style="font-style: italic; font-size: x-large">').text('- необходима когда требуется что-то добавить.'));
    });
    $('.img_find').click(function(){
        $('#block_text_left').text('Найти').append($('<p style="font-style: italic; font-size: x-large">').text('- запускает поиск.'));
    });
}); 
