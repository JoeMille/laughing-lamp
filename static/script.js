// Initiate the script


var elements = document.getElementsByClassName('index-welcome');

for(var i = 0; i < elements.length; i++) {
    elements[i].addEventListener('mouseover', function() {
        this.classList.add('shake');
    });

        elements[i].addEventListener('mouseout', function() {
            this.classList.remove('shake');
        });
}

console.log('Hello from script.js');