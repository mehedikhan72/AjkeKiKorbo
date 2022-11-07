document.addEventListener('DOMContentLoaded', function() {
    document.querySelector("#add_task_btn").addEventListener('click', function() {
        add_menu = document.getElementById('add_pop_up');
        add_menu.classList.remove("add_task_hidden");
        add_menu.classList.add("add_task_shown");

        disable_view();

    })

    document.querySelector("#cancel_add_task_btn").addEventListener('click', function() {
        task_name = document.getElementById('task_name');
        task_name.value = "";

        add_menu = document.getElementById('add_pop_up');
        add_menu.classList.add("add_task_hidden");
        add_menu.classList.remove("add_task_shown");

        enable_view();
    })

    document.querySelector("#save_add_task_btn").addEventListener('click', function() {
        add_menu = document.getElementById('add_pop_up');
        task_name = document.getElementById('task_name');

        if(task_name !== None){
            add_menu.classList.add("add_task_hidden");
            add_menu.classList.remove("add_task_shown");
        }

        enable_view();

    })
})
// JS for review options!!

document.addEventListener('DOMContentLoaded', function() {
    document.querySelector("#add_review_btn").addEventListener('click', function(){
        review_menu = document.getElementById('review_pop_up');
        review_menu.classList.remove("review_div_hidden");
        review_menu.classList.add("review_div_shown");

        disable_view();

    });

    document.querySelector("#cancel_review_btn").addEventListener('click', function(){
        rev_name = document.getElementById('review_text');
        rev_name.value = "";

        review_menu = document.getElementById('review_pop_up');
        review_menu.classList.add("review_div_hidden");
        review_menu.classList.remove("review_div_shown");

        enable_view();

    });

    document.querySelector("#save_review_btn").addEventListener('click', function(){
        review_menu = document.getElementById('review_pop_up');
        rev_name = document.getElementById('review_text');

        if(rev_name.value == ""){
            alert("Review Must Not Be Empty!");
        }
        else{
            review = rev_name.value;
            fetch('/add_review', {
                method: "POST",
                credentials : 'same-origin',
                headers: {
                    "Accept" : 'application/json',
                    'X-Requested-With'  : 'XMLHttpRequest',
                    'X-CSRFToken' : getCookie("csrftoken"),
                },
                body: JSON.stringify({"review" : review})
            })
            .then(response => {
                console.log(response);
                review_menu.classList.add("review_div_hidden");
                review_menu.classList.remove("review_div_shown");
                rev_name.value = "";
                enable_view();

                
                document.getElementById("review_taken").style.animationPlayState = 'running';
            })
        }
    });
})

function disable_view(){
    body = document.querySelector('.today-page');
    nav = document.querySelector('.nav-data');

    body.classList.remove("today-page");
    body.classList.add("today-page-disabled");

    nav.classList.remove("nav-data");
    nav.classList.add("nav-data-disabled");

}

function enable_view() {
    body = document.querySelector('.today-page-disabled');
    nav = document.querySelector('.nav-data-disabled');

    body.classList.add("today-page");
    body.classList.remove("today-page-disabled");

    nav.classList.add("nav-data");
    nav.classList.remove("nav-data-disabled");
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}