document.addEventListener("DOMContentLoaded", function() {
    console.log("hello");

    $(document).on("click", "button#playbtn", function(event) {
        event.preventDefault();
        console.log("button clicked");
        // $('audio').prop("src", );

        $('audio').attr("src", 'sample-file-4.wav');

        var aud = document.getElementById('audioplayer');
        aud.play();

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
});