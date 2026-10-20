// Get DOM elements
const likeButton = document.getElementById('btn');
const likeCountElement = document.getElementById('like-count');

let isLiked = false;
let likeCount = 0;
likeButton.addEventListener('click', () => {
    isLiked = !isLiked;

    if (isLiked) {
        likeCount++;
        likeButton.textContent = 'Liked ❤️';
        likeButton.classList.add('liked');
    } else {
        likeCount--;
        likeButton.textContent = 'Like';
        likeButton.classList.remove('liked');
    }
    likeCountElement.textContent = likeCount;
});