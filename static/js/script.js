const text = document.querySelector('#text');
const doc = document.querySelector('#doc');
const link = document.querySelector('#web-link');
const submit3 = document.querySelector("#submission3");
const submit1 = document.querySelector("#submission1");
const clear1 = document.querySelector("#clear1");
const clear3 = document.querySelector("#clear3");
const loader = document.querySelector(".loaders");
const all = document.querySelector("#all-content");

loader.style.display = "none";
document.querySelector('.box1').style.display = "none";
document.querySelector('.box3').style.display = "none";
document.querySelector('.box2').style.display = "none";
document.querySelector('#output').style.display = "none";

function checkTime(i) {
    if (i < 10) {
        i = "0" + i;
    }
    return i;
}

setInterval(function() {
    const clock = document.querySelector(".display");
    let time = new Date();
    let sec = time.getSeconds();
    let min = time.getMinutes();
    let hr = time.getHours();
    let day = 'AM';
    if (hr > 12) {
        day = 'PM';
        hr = hr - 12;
    }
    if (hr == 0) {
        hr = 12;
    }
    if (sec < 10) {
        sec = '0' + sec;
    }
    if (min < 10) {
        min = '0' + min;
    }
    if (hr < 10) {
        hr = '0' + hr;
    }
    clock.textContent = hr + ':' + min + ':' + sec + " " + day;
});


text.addEventListener('click', (e) => {
    document.querySelector('#output').style.display = "none";
    document.querySelector('.box1').style.display = "block";
    document.querySelector('.box3').style.display = "none";
    document.querySelector('.box2').style.display = "none";
})

doc.addEventListener('click', (e) => {
    document.querySelector('#output').style.display = "none";
    document.querySelector('.box1').style.display = "none";
    document.querySelector('.box3').style.display = "none";
    document.querySelector('.box2').style.display = "block";
})

link.addEventListener('click', (e) => {
    document.querySelector('#output').style.display = "none";
    document.querySelector('.box1').style.display = "none";
    document.querySelector('.box2').style.display = "none";
    document.querySelector('.box3').style.display = "block";
})

clear1.addEventListener('click', () => {
    document.querySelector('#text-box1').value = null;
    document.querySelector("#output").style.display = "none";
    document.getElementById("message1").value = null;
})

clear2.addEventListener('click', () => {
    document.getElementById("file1").value = null;
    document.querySelector("#output").style.display = "none";
})

clear3.addEventListener('click', () => {
    document.getElementById("name").value = null;
    document.getElementById("message2").value = null;
    document.querySelector("#output").style.display = "none";
})

document.getElementById("back-top").addEventListener("click", function() {
    var elmntToView = document.getElementById("first");
    elmntToView.scrollIntoView();

})

submit1.addEventListener("click", submit_entry1);

function submit_entry1() {
    const name = document.getElementById("text-box1");
    var message = document.getElementById("message1");

    if (name.value == "" || message.value == "") {
        alert("Enter both details");
        return;
    }

    all.style.display = "none";
    loader.style.display = "block";

    l_time(59); // calling loading timer function

    var entry = {
        name: name.value,
        message: message.value
    };

    // console.log(entry);

    fetch(`${window.origin}/text-op`, {
        method: "POST",
        credentials: "include",
        body: JSON.stringify(entry),
        cache: "no-cache",
        headers: new Headers({
            "content-type": "application/json"
        })
    })

    .then(function(response) {

        if (response.status != 200) {

            console.log(`Status not 200 : ${response.status}`);
            return;
        }

        response.json().then(function(data) {
            // console.log(data.message);
            document.getElementById("info").innerHTML = data.message;

        })

    })

    setTimeout(() => {
        document.getElementById("output").style.top = "150%";
        all.style.display = "block";
        loader.style.display = "none";
        document.getElementById("output").style.display = "block";
        var elmntToView = document.getElementById("output");
        elmntToView.scrollIntoView();
        calcRT();
    }, 60000);

}

// for submission-2

$(function() {
    $('#submission2').click(function() {

        if (document.getElementById("file1").value == "") {
            alert("Upload the file first");
            return;
        }

        all.style.display = "none";
        l_time(59); // calling loading timer function
        loader.style.display = "block";

        var form_data = new FormData($('#upload-file')[0]);
        $.ajax({
                type: 'POST',
                url: '/uploadajax',
                data: form_data,
                contentType: false,
                cache: false,
                processData: false,
                // success: function(data) {
                //     console.log('Success!');
                // },
            })
            .then(function(response) {
                document.getElementById("info").innerHTML = response;
            })

        setTimeout(() => {

            document.getElementById("output").style.top = "125%";
            all.style.display = "block";
            loader.style.display = "none";
            document.getElementById("output").style.display = "block";
            var elmntToView = document.getElementById("output");
            elmntToView.scrollIntoView();
            calcRT();
        }, 60000);
    });
});

submit3.addEventListener("click", submit_entry3);

function submit_entry3() {
    const name = document.getElementById("name");
    var message = document.getElementById("message2");

    if (name.value == "" || message.value == "") {
        alert("Enter both details");
        return;
    }

    all.style.display = "none";
    loader.style.display = "block";
    flag = 1;

    l_time(6); // calling loading timer function

    var entry = {
        name: name.value,
        message: message.value
    };

    fetch(`${window.origin}/create`, {
        method: "POST",
        credentials: "include",
        body: JSON.stringify(entry),
        cache: "no-cache",
        headers: new Headers({
            "content-type": "application/json"
        })
    })

    .then(function(response) {

        if (response.status != 200) {

            console.log(`Status not 200 : ${response.status}`);
            return;
        }

        response.json().then(function(data) {
            // console.log(data.message);
            document.getElementById("info").innerHTML = data.message;
        })

    })

    setTimeout(() => {
        document.getElementById("output").style.top = "120%";
        all.style.display = "block";
        loader.style.display = "none";
        document.getElementById("output").style.display = "block";
        var elmntToView = document.getElementById("output");
        elmntToView.scrollIntoView();
        calcRT();
    }, 7000);


}

function calcRT() {
    const wordsPerMinute = 200; // Average case.
    let result;

    var text = document.getElementById("output-text").innerText;

    if (text == "") {
        // console.log("Break");
        text = document.getElementById("text-box1").value; // Takes text from 1st box otherwise
    }

    // Initialize the word counter
    var textLength = 0;

    // Loop through the text 
    // and count spaces in it  
    for (var i = 0; i < text.length; i++) {
        var currentCharacter = text[i];

        // Check if the character is a space 
        if (currentCharacter == " ") {
            textLength += 1;
        }
    }

    // Add 1 to make the count equal to 
    // the number of words  
    // (count of words = count of spaces + 1) 
    textLength += 1;

    if (textLength > 0) {
        let value = Math.ceil(textLength / wordsPerMinute);
        result = `~${value} min read`;
    }
    document.getElementById("readingTime").innerText = result;
}

function l_time(timeleft) {
    // var timeleft = 10;
    var downloadTimer = setInterval(function() {
        if (timeleft <= 0) {
            clearInterval(downloadTimer);
        } else {
            document.querySelector("#loading_time").innerHTML = timeleft + " seconds remaining";
        }
        timeleft -= 1;
    }, 1000);
}