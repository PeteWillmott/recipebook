var cards = document.querySelectorAll('#cards .card');
var currentCard = 0;

var next = document.getElementById('next');
var previous = document.getElementById('previous');

function nextCard() {
    goToCard(currentCard + 1);
}

function previousCard() {
    goToCard(currentCard - 1);
}

function goToCard(n) {
    cards[currentCard].className = 'card';
    currentCard = (n + cards.length) % cards.length;
    cards[currentCard].className = 'card  top';
}

next.onclick = function() {
    nextCard();
};
previous.onclick = function() {
    previousCard();
};
