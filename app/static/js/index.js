var select_school_class = document.querySelector('#sc');
var select_lesson = document.querySelector('#lessons');
var date_input = document.querySelector("#date")
var tasks_div = document.querySelector("#tasks")

var selected_school_class = undefined;

const createSchoolClassesOptions = () => {
    select_school_class.innerHTML = "";
    Object.keys(plans).forEach(school_plan_name => {
        let option_node = document.createElement("option");
        option_node.value = school_plan_name;
        option_node.text = school_plan_name.toUpperCase();
        option_node.onselect = () => {
            selected_school_class = option.text.toLowerCase();
        }
        select_school_class.appendChild(option_node);
    });
}

const zfill = (str, size) => {
    str = "" + str
    while(str.length < size) str = "0" + str;
    return str;
}

const formateDate = (date) => {
    let minute = date.getMinutes();
    let hour = date.getHours();
    let day = date.getDate();
    let month = date.getMonth() + 1;
    let year = date.getFullYear();
    
    return zfill(hour, 2) + ":" + zfill(minute, 2) + " " + zfill(day, 2) + "." + zfill(month, 2) + "." + year
}

const createTasksView = () => {
    tasks_div.innerHTML = "";
    console.log(tasks);
    Object.keys(tasks).forEach(task => {
        console.log(task);
        tasks[task].forEach(task_element => {
            let p_node = document.createElement("p");
            let date = new Date(0);
            date.setUTCSeconds(task_element[0]);
            p_node.innerText = task + " - " + formateDate(date) + " - " + task_element[1];
            tasks_div.appendChild(p_node);
        });
    })
}

const createLessons = (weekday) => {
    select_lesson.innerHTML = "";
    let selected_lesson = select_school_class.options[select_school_class.selectedIndex].value;
    let selected_plan = plans[selected_lesson];
    let selected_day = selected_plan[weekday];
    selected_day.forEach((lesson_set, index) => {
        lesson_set.forEach((lesson, lesson_index) => {
            if(lesson != '-'){
                let option = document.createElement('option');
                option.value = index + "." + lesson_index;
                option.text = lesson;
                select_lesson.appendChild(option);   
            }
        });
    });
}

const getWeekNumber = (date) => {
    return Math.ceil((((date.getTime() - (new Date(date.getFullYear(), 0, 1)).getTime())/ 86400000) + 1) / 7)
}

const getWeekNumbersDifference = (date1, date2) => {
    return Math.abs(getWeekNumber(date1) - getWeekNumber(date2));
}

const setDateLabelText = (date, weekday) => {
    let weekdays_names = ["Poniedzialek", "Wtorek", "Sroda", "Czwartek", "Piatek", "Sobota", "Niedziela"];
    let difference = getWeekNumbersDifference(date, new Date());
    let str = "";
    switch(difference){
        case 0:
            str = weekdays_names[weekday] + " w tym tygodniu";
            break;
        case 1:
            str = weekdays_names[weekday] + " w nastepnym tygodniu"
            break;
        default:
            str = weekdays_names[weekday] + " za " + (difference) + " " + getPLEnd("tydzien", difference);
            break;
    }
    let current_date = new Date();
    current_date.setUTCHours(0);
    current_date.setUTCMinutes(0);
    current_date.setUTCSeconds(0);
    current_date.setUTCMilliseconds(0);
    if(current_date.getTime() == date.getTime()){
        str = "Dzisiaj";
    }
    if(date.getTime() < current_date.getTime()){
        date_input.value = undefined;
        toast("Nie mozesz wybrac tej daty!");
        str = "Wybierz date"
    }
    document.querySelector("#d_label").innerHTML = str;
}

date_input.addEventListener('change', () => {
    let selected_value = date_input.value;
    let date = new Date(selected_value);
    let weekday = date.getDay() - 1;
    if(weekday == -1){
        weekday = 6;
    }
    document.querySelector("#weekday").value = weekday;
    setDateLabelText(date, weekday);
    createLessons(weekday);
})

onload = () => {
    createSchoolClassesOptions();
    createTasksView();
}


