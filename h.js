
    var table = document.getElementById("safe");
    var safeScreen = '';
    var screen = document.getElementById("safescreen");
    var button = document.getElementById('safe-button');
    var answ = false;

        if (table != null) {
            for (var i = 0; i < table.rows.length; i++) {
                for (var j = 0; j < table.rows[i].cells.length; j++)
                    table.rows[i].cells[j].onclick = function () {
        tableText(this);
};
}
}

        function tableText(tableCell) {
            var numb = tableCell.innerHTML;
            if (answ != true) {
                if (safeScreen.length < 5) {
        safeScreen += numb;
    screen.innerHTML = safeScreen;
                } else if (safeScreen.length === 5) {
        safeScreen = '';
    screen.innerHTML = '';
    safeScreen += numb;
    screen.innerHTML = safeScreen;
}
}
}

        function pwr(number) {
            var result = 0
            for (let i = 0; i < number.length; i++) {
                var el = Number(number[i]);
    result += el ** i
}
return result
}
        button.addEventListener('click', function (e) {
        let link = 'pos_work.html'
    var pwd = screen.innerHTML;
            if (answ != true) {
                if (pwr(pwd) === 2470) {
        screen.innerHTML = `<span class="winner">
                    <a href="${link}">ссылка</a></span>`
                    answ = true
                } else {
        screen.innerHTML = '<span class="loser">ПРОВАЛ</span>'
                    safeScreen = '';
}
}
});

