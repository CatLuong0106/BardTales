document.addEventListener("DOMContentLoaded", function() {
    console.log("hello");

    $(document).on("click", "button#playbtn", function(event) {
        event.preventDefault();
        console.log("button clicked");
        // $('audio').prop("src", );
        
        //get me div with id "study-text" and get the text from it
        var text = $('div.content').text();
        //strip the text of any leading or trailing whitespace
        text = text.replace(/(\r\n|\n|\r)/gm, "");
        text = text.trim();

        console.log("text:", text);

        //send the text to the server
        $.ajax({
            url: "/getaudio",
            type: "POST",
            data: JSON.stringify({text: text}),
            contentType: "application/json",
            success: function(data) {
                console.log(data);
                // $('audio #source').attr("src", data);

                $('audio').attr("src", 'mixed.wav');
                // $('audio').load();
                // $('audio').play();

                var aud = document.getElementById('audioplayer');
                aud.play();

                // $('audio').get(0).load();
                // $('audio').get(0).play();



               

            }
        });


        

        // $('audio').load();
        // $('audio').play();

        /*
        $.ajax({
            url: "/getaudio",
            // type: "POST",
            // contentType: false,
            // processData: false,
            success: function(data) {
                // console.log(data);
                // $('audio #source').attr("src", data);

                $('audio').attr("src", data);
                // $('audio').load();
                // $('audio').play();

                aud.play();

                // $('audio').get(0).load();
                // $('audio').get(0).play();
            }
        });
        */

        var audioElement = document.getElementById('audioplayer');
        audioElement.addEventListener('ended', function() {
            console.log("ended");
                this.play();
            }, false);
    });

    $(document).on("click", "a#loadtext", function(event) {
        console.log("link clicked");
        event.preventDefault();
        $('div#modal-inputtext').addClass("active");
    });

    $(document).on("click", "a#modal-close-btn", function(event) {
        $('div#modal-inputtext').removeClass("active");
    });

    $(document).on("click", "button#inputtext-sbmt", function(event) {
        event.preventDefault();
        console.log("text val:", $('textarea#inputtext').val());
        $('div.content').text($('textarea#inputtext').val());
    });

});