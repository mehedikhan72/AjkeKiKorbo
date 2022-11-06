document.addEventListener('DOMContentLoaded', function() {
    document.querySelector("#add_task_btn").addEventListener('click', function() {
        add_menu = document.getElementById('add_pop_up');
        add_menu.classList.remove("add_task_hidden");
        add_menu.classList.add("add_task_shown");

        body = document.querySelector('.today-page');
        nav = document.querySelector('.nav-data');

        body.classList.remove("today-page");
        body.classList.add("today-page-disabled");

        nav.classList.remove("nav-data");
        nav.classList.add("nav-data-disabled");

    })

    document.querySelector("#cancel_add_task_btn").addEventListener('click', function() {
        task_name = document.getElementById('task_name');
        task_name.value = ""

        add_menu = document.getElementById('add_pop_up');
        add_menu.classList.add("add_task_hidden");
        add_menu.classList.remove("add_task_shown");

        body = document.querySelector('.today-page-disabled');
        nav = document.querySelector('.nav-data-disabled');

        body.classList.add("today-page");
        body.classList.remove("today-page-disabled");

        nav.classList.add("nav-data");
        nav.classList.remove("nav-data-disabled");
    })

    document.querySelector("#save_add_task_btn").addEventListener('click', function() {
        add_menu = document.getElementById('add_pop_up');

        task_name = document.getElementById('task_name');

        if(task_name !== None){
            add_menu.classList.add("add_task_hidden");
            add_menu.classList.remove("add_task_shown");
        }

        body = document.querySelector('.today-page-disabled');
        nav = document.querySelector('.nav-data-disabled');

        body.classList.add("today-page");
        body.classList.remove("today-page-disabled");

        nav.classList.add("nav-data");
        nav.classList.remove("nav-data-disabled");
    })
})