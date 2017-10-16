$(document).ready(function(){ 

  $("#id_eventStart").datepicker($.datepicker.regional[ "ru" ]);
  $("#id_eventStop").datepicker($.datepicker.regional[ "ru" ]);

 // переменнная для запоминания url элемента
     var url = ''      	
 
// Функция переключения кнопки подсказок
 $(".button_prompt").click(function () { 
 
     var src_1 = '/static/pricemin/image/mob/buttons_mob/Question_on.png';
     var src_2 = '/static/pricemin/image/mob/buttons_mob/Question_off.png';    
     
   if ($(this).attr('src') == src_2) {
     $(this).attr('src', src_1); 
   }
   else {
     $(this).attr('src', src_2);   
   }
 });

 // Функция вызыва подсказки по клику на .before-prompt 
 $(".before_prompt").click(function(){

	 prompt = $(this).attr("prompt");
	 prompt2 = $(this).attr("prompt2");
	 prompt3 = $(this).attr("prompt3");
	 prompt4 = $(this).attr("prompt4");
	 prompt5 = $(this).attr("prompt5");
	 $("#prompt").slideDown();
	 $("#prompt").append("<p id='p_1' class='p_prompt'>");
	 $("#p_1").text(prompt);
	 $("#prompt").append("<p id='p_2' class='p_prompt'>");
	 $("#p_2").text(prompt2);
	 $("#prompt").append("<p id='p_3' class='p_prompt'>");
	 $("#p_3").text(prompt3);
	 $("#prompt").append("<p id='p_4' class='p_prompt'>");
	 $("#p_4").text(prompt4);
	 $("#prompt").append("<p id='p_5' class='p_prompt'>");
	 $("#p_5").text(prompt5);
	 url = $(this).attr('href');
 });

// Функция закрытия подсказки и дальнейшего перехода
 $(".after_prompt").click(function(){

	 location.href = url;
	 
 });


});

