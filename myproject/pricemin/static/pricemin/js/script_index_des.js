$(document).ready(function(){

    var url = '';

    $(".rules").click(function () {

        $("#prompt").slideDown();
        $("#prompt_text").append("<span class='prompt1 text_x-large'>");
        $(".prompt1").text("Правила использования сервиса Pricemin. ");
        $("#prompt_text").append("<br>");
        $("#prompt_text").append("<span class='prompt2 text_left text_large'>");
        $(".prompt2").text("Редко кто вникает в условия использования программных продуктов. " +
         "Чаще люди, не читая, прокручивают страницу вниз, отмечают пункт «Согласен», " +
         "и беззаботно пользуются программой.");
        $("#prompt_text").append("<br>");
        $("#prompt_text").append("<span class='prompt3 text_large'>");
        $(".prompt3").text(" По этой причине в настоящих правилах пока только несколько пунктов:");
        $("#prompt_text").append("<br>");
        $("#prompt_text").append("<span class='prompt4 text_large'>");
        $(".prompt4").text("1. Отказ от ответственности. Ни кто не гарантирует достоверности используемой информации. ");
        $("#prompt_text").append("<br>");
        $("#prompt_text").append("<span class='prompt5 text_large'>");
        $(".prompt5").text("2. Запрещено любое оскорбление (в том числе нецензурная лексика), заведомо ложная информация, " +
         "a так же любые действия влекущие вред другим участникам или нарушение действующего законодательства. ");
        $("#prompt_text").append("<br>");
        $("#prompt_text").append("<span class='prompt7 text_large'>");
        $(".prompt7").text(    "3. Каждый вошедший в систему пользователь обязан выполнять данные правила и в случае их нарушения подлежит блокированию аккаунта. ");
        $("#prompt_text").append("<br>");
        $("#prompt_text").append("<span class='prompt8 text_large'>");
        $(".prompt8").text(    "4. Каждый пользователь имеет право сообщить о нарушениях, предложить улучшения, " +
           "или просто оставить комментарий отправив письмо администратору на");
        $("#prompt_text").append("<br>");
        $("#prompt_text").append("<span class='prompt9 text_x-large'>");
        $(".prompt9").text("e-mail: pricemin@mail.ru");
        url = $(this).attr('href');
    });




// Функция закрытия подсказки и дальнейшего перехода
    $( ".button" ).click(function(){

       location.href = url;
	 
    });
});
