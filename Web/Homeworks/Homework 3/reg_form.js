var users = [{ "id": 1, "name": "Leanne Graham", "username": "Bret", "email": "Sincere@april.biz", "address": { "street": "Kulas Light", "suite": "Apt. 556", "city": "Gwenborough", "zipcode": "92998-3874", "geo": { "lat": "-37.3159", "lng": "81.1496" } }, "phone": "1-770-736-8031 x56442", "website": "hildegard.org", "company": { "name": "Romaguera-Crona", "catchPhrase": "Multi-layered client-server neural-net", "bs": "harness real-time e-markets" } }, { "id": 2, "name": "Ervin Howell", "username": "Antonette", "email": "Shanna@melissa.tv", "address": { "street": "Victor Plains", "suite": "Suite 879", "city": "Wisokyburgh", "zipcode": "90566-7771", "geo": { "lat": "-43.9509", "lng": "-34.4618" } }, "phone": "010-692-6593 x09125", "website": "anastasia.net", "company": { "name": "Deckow-Crist", "catchPhrase": "Proactive didactic contingency", "bs": "synergize scalable supply-chains" } }, { "id": 3, "name": "Clementine Bauch", "username": "Samantha", "email": "Nathan@yesenia.net", "address": { "street": "Douglas Extension", "suite": "Suite 847", "city": "McKenziehaven", "zipcode": "59590-4157", "geo": { "lat": "-68.6102", "lng": "-47.0653" } }, "phone": "1-463-123-4447", "website": "ramiro.info", "company": { "name": "Romaguera-Jacobson", "catchPhrase": "Face to face bifurcated interface", "bs": "e-enable strategic applications" } }, { "id": 4, "name": "Patricia Lebsack", "username": "Karianne", "email": "Julianne.OConner@kory.org", "address": { "street": "Hoeger Mall", "suite": "Apt. 692", "city": "South Elvis", "zipcode": "53919-4257", "geo": { "lat": "29.4572", "lng": "-164.2990" } }, "phone": "493-170-9623 x156", "website": "kale.biz", "company": { "name": "Robel-Corkery", "catchPhrase": "Multi-tiered zero tolerance productivity", "bs": "transition cutting-edge web services" } }, { "id": 5, "name": "Chelsey Dietrich", "username": "Kamren", "email": "Lucio_Hettinger@annie.ca", "address": { "street": "Skiles Walks", "suite": "Suite 351", "city": "Roscoeview", "zipcode": "33263", "geo": { "lat": "-31.8129", "lng": "62.5342" } }, "phone": "(254)954-1289", "website": "demarco.info", "company": { "name": "Keebler LLC", "catchPhrase": "User-centric fault-tolerant solution", "bs": "revolutionize end-to-end systems" } }, { "id": 6, "name": "Mrs. Dennis Schulist", "username": "Leopoldo_Corkery", "email": "Karley_Dach@jasper.info", "address": { "street": "Norberto Crossing", "suite": "Apt. 950", "city": "South Christy", "zipcode": "23505-1337", "geo": { "lat": "-71.4197", "lng": "71.7478" } }, "phone": "1-477-935-8478 x6430", "website": "ola.org", "company": { "name": "Considine-Lockman", "catchPhrase": "Synchronised bottom-line interface", "bs": "e-enable innovative applications" } }, { "id": 7, "name": "Kurtis Weissnat", "username": "Elwyn.Skiles", "email": "Telly.Hoeger@billy.biz", "address": { "street": "Rex Trail", "suite": "Suite 280", "city": "Howemouth", "zipcode": "58804-1099", "geo": { "lat": "24.8918", "lng": "21.8984" } }, "phone": "210.067.6132", "website": "elvis.io", "company": { "name": "Johns Group", "catchPhrase": "Configurable multimedia task-force", "bs": "generate enterprise e-tailers" } }, { "id": 8, "name": "Nicholas Runolfsdottir V", "username": "Maxime_Nienow", "email": "Sherwood@rosamond.me", "address": { "street": "Ellsworth Summit", "suite": "Suite 729", "city": "Aliyaview", "zipcode": "45169", "geo": { "lat": "-14.3990", "lng": "-120.7677" } }, "phone": "586.493.6943 x140", "website": "jacynthe.com", "company": { "name": "Abernathy Group", "catchPhrase": "Implemented secondary concept", "bs": "e-enable extensible e-tailers" } }, { "id": 9, "name": "Glenna Reichert", "username": "Delphine", "email": "Chaim_McDermott@dana.io", "address": { "street": "Dayna Park", "suite": "Suite 449", "city": "Bartholomebury", "zipcode": "76495-3109", "geo": { "lat": "24.6463", "lng": "-168.8889" } }, "phone": "(775)976-6794 x41206", "website": "conrad.com", "company": { "name": "Yost and Sons", "catchPhrase": "Switchable contextually-based project", "bs": "aggregate real-time technologies" } }, { "id": 10, "name": "Clementina DuBuque", "username": "Moriah.Stanton", "email": "Rey.Padberg@karina.biz", "address": { "street": "Kattie Turnpike", "suite": "Suite 198", "city": "Lebsackbury", "zipcode": "31428-2261", "geo": { "lat": "-38.2386", "lng": "57.2232" } }, "phone": "024-648-3804", "website": "ambrose.net", "company": { "name": "Hoeger LLC", "catchPhrase": "Centralized empowering task-force", "bs": "target end-to-end models" } }];

var form = document.getElementById('registration-form');
var success = document.getElementById('success');

function showError(fieldId, message) {
    var error = document.getElementById(fieldId + '-error');
    var input = document.getElementById(fieldId);
    error.textContent = message;
    error.classList.add('show');
    input.classList.add('invalid');
}

function clearError(fieldId) {
    var error = document.getElementById(fieldId + '-error');
    var input = document.getElementById(fieldId);
    error.classList.remove('show');
    input.classList.remove('invalid');
}

function clearAllErrors() {
    var errors = document.querySelectorAll('.error');
    var inputs = document.querySelectorAll('input');

    errors.forEach(function (div) {
        div.classList.remove('show');
    });

    inputs.forEach(function (input) {
        input.classList.remove('invalid');
    });

    success.classList.remove('show');
}

function validateUsername(username) {
    if (!username) {
        return 'Потребителското име е задължително';
    }
    if (username.length < 3 || username.length > 10) {
        return 'Потребителското име трябва да е между 3 и 10 символа';
    }
    return null;
}

function validateName(name) {
    if (!name) {
        return 'Името е задължително';
    }
    if (name.length > 50) {
        return 'Името не може да надвишава 50 символа';
    }
    return null;
}

function validateFamilyName(familyName) {
    if (!familyName) {
        return 'Фамилията е задължителна';
    }
    if (familyName.length > 50) {
        return 'Фамилията не може да надвишава 50 символа';
    }
    return null;
}

function validateEmail(email) {
    if (!email) {
        return 'Имейлът е задължителен';
    }
    var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
        return 'Невалиден имейл формат';
    }
    return null;
}

function validatePassword(password) {
    if (!password) {
        return 'Паролата е задължителна';
    }
    if (password.length < 6 || password.length > 10) {
        return 'Паролата трябва да е между 6 и 10 символа';
    }

    var hasUpperCase = /[A-Z]/.test(password);
    var hasLowerCase = /[a-z]/.test(password);
    var hasNumber = /[0-9]/.test(password);

    if (!hasUpperCase || !hasLowerCase || !hasNumber) {
        return 'Паролата трябва да включва главни и малки букви и цифри';
    }
    return null;
}

function validatePostalCode(postalCode) {
    if (!postalCode) {
        return null;
    }

    var format1 = /^\d{5}-\d{4}$/;
    var format2 = /^\d{4}$/;

    if (!format1.test(postalCode) && !format2.test(postalCode)) {
        return 'Пощенският код трябва да е във формат 11111-1111 или 1111';
    }
    return null;
}

form.addEventListener('submit', function (e) {
    e.preventDefault();
    clearAllErrors();

    var username = document.getElementById('username').value.trim();
    var name = document.getElementById('name').value.trim();
    var familyName = document.getElementById('family-name').value.trim();
    var email = document.getElementById('email').value.trim();
    var password = document.getElementById('password').value;
    var street = document.getElementById('street').value.trim();
    var city = document.getElementById('city').value.trim();
    var postalCode = document.getElementById('postal-code').value.trim();

    var isValid = true;

    var usernameError = validateUsername(username);
    if (usernameError) {
        showError('username', usernameError);
        isValid = false;
    }

    var nameError = validateName(name);
    if (nameError) {
        showError('name', nameError);
        isValid = false;
    }

    var familyNameError = validateFamilyName(familyName);
    if (familyNameError) {
        showError('family-name', familyNameError);
        isValid = false;
    }

    var emailError = validateEmail(email);
    if (emailError) {
        showError('email', emailError);
        isValid = false;
    }

    var passwordError = validatePassword(password);
    if (passwordError) {
        showError('password', passwordError);
        isValid = false;
    }

    var postalCodeError = validatePostalCode(postalCode);
    if (postalCodeError) {
        showError('postal-code', postalCodeError);
        isValid = false;
    }

    if (!isValid) {
        return;
    }

    var userExists = users.some(function (user) {
        return user.username === username;
    });

    if (userExists) {
        showError('username', 'Потребител с това име вече съществува');
        return;
    }

    try {
        var newUser = {
            username: username,
            name: name + ' ' + familyName,
            email: email,
            address: {
                street: street,
                city: city,
                zipcode: postalCode
            }
        };

        success.textContent = 'Успешна регистрация! Вашият акаунт беше създаден успешно.';
        success.classList.add('show');
        form.reset();

        console.log('Регистриран потребител:', newUser);
    } catch (error) {
        console.error('Грешка при регистрацията:', error);
    }
});