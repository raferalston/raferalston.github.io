function pwr(number) {
    var result = 0
    for (let i = 0; i < number.length; i++) {
        var el = Number(number[i]);
        result += el ** i
    }
    return result
}

let b = document.querySelector('body')

let password = document.createElement('div')
password.classList = 'pass'
password.textContent = 'Enter password:'

let input_t = document.createElement('input')
let input_b = document.createElement('input')

input_t.setAttribute('type', 'password')
input_t.setAttribute('placeholder', 'password')
input_b.setAttribute('type', 'submit')
input_b.setAttribute('value', 'enter')

password.append(input_t)
password.append(input_b)

b.append(password)

input_b.addEventListener('click', (e) => {
    e.preventDefault();
    let value = input_t.value
    if (!(pwr(value) == 56)) {
        b.remove()
    } else {
        password.remove()
    };
})