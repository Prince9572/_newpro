const btn = document.getElementById("btn");
btn.addEventListener("click", function abc(){
    let count = count++;
    console.log(count);
    document.getElementById("para").textCount = count;
});
