$(document).ready(function(){ 
 
   $("#id_eventStart").datepicker($.datepicker.regional[ "ru" ]);
  $("#id_eventStop").datepicker($.datepicker.regional[ "ru" ]);
  
 // Функция переключения кнопки подсказок
 $(".button_prompt").click(function () { 
 
     var src_1 = '/static/pricemin/image/mob/buttons_mob/Question_on.png';
     var src_2 = '/static/pricemin/image/mob/buttons_mob/Question_off.png';    
     
   if ($(this).attr('src') == src_1) {
     $(this).attr('src', src_2); 
   }
   else {
     $(this).attr('src', src_1);   
   }
 });


// Функция закрытия подсказки и дальнейшего перехода
 $(".after_prompt").click(function(){

	 location.href = url;
	 
 }); 

});
