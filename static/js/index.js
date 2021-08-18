var select_sc = document.querySelector('#sc');
var select_lesson = document.querySelector('#lessons');
var date_input = document.querySelector("#date")

const createSC = () => {
    select_sc.innerHTML = "";
    Object.keys(plan).forEach(key => {
        let option = document.createElement("option");
        option.value = key;
        option.text = key.toUpperCase();
        select_sc.appendChild(option);
    });
}

const createLessons = (weekday) => {
    select_lesson.innerHTML = "";
    let selected = select_sc.options[select_sc.selectedIndex].value;
    let selected_plan = plan[selected];
    let day = selected_plan[weekday];
    day.forEach((lesson_set, index) => {
        lesson_set.forEach((lesson, l_index) => {
            if(lesson != '-'){
                let option = document.createElement('option');
                option.value = index + "." + l_index;
                option.text = lesson;
                select_lesson.appendChild(option);   
            }
        });
    });
}

const getWeekNo = (date) => {
    return Math.ceil((((date.getTime() - (new Date(date.getFullYear(), 0, 1)).getTime())/ 86400000) + 1) / 7)
}

const getWeekNoDifference = (date1, date2) => {
    return Math.abs(getWeekNo(date1) - getWeekNo(date2));
}

const setDLabelText = (date, weekday) => {
    let weekdays = ["Poniedzialek", "Wtorek", "Sroda", "Czwartek", "Piatek", "Sobota", "Niedziela"];
    let dif = getWeekNoDifference(date, new Date());
    let str = "";
    switch(dif){
        case 0:
            str = weekdays[weekday] + " w tym tygodniu";
            break;
        case 1:
            str = weekdays[weekday] + " w nastepnym tygodniu"
            break;
        default:
            str = weekdays[weekday] + " za " + (dif) + " " + getPLEnd("tydzien", dif);
            break;
    }
    let d = new Date();
    d.setUTCHours(0);
    d.setUTCMinutes(0);
    d.setUTCSeconds(0);
    d.setUTCMilliseconds(0);
    if(date.getTime() == d.getTime()){
        str = "Dzisiaj";
    }
    if(date.getTime() < d.getTime()){
        date_input.value = undefined;
        toast("Nie mozesz wybrac tej daty!");
        str = "Wybierz date"
    }
    document.querySelector("#d_label").innerHTML = str;
}

onload = () => {
    createSC();
}

date_input.addEventListener('change', () => {
    let v = date_input.value;
    let d = new Date(v);
    let weekday = d.getDay() - 1;
    if(weekday == -1){
        weekday = 6;
    }
    document.querySelector("#weekday").value = weekday;
    setDLabelText(d, weekday);
    createLessons(weekday);
})