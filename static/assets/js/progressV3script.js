let number = document.getElementById('number')
let counter = 0

setInterval(()=> {
if(counter == 100){
clearInterval;

}
else{
    counter += 1
    number.innerHTML = `${counter}%`
    if(counter == 100)
    number.innerHTML = `Done!`
    
}

},45);