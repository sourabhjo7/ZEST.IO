const startMin = 1.5;
let time = startMin * 60;

const con = $(".timeCon");

setInterval(countDown, 1000);

function countDown(){

    if(time === 0){
        window.location.replace("/results");
    }else{
        const min = Math.floor(time / 60);
        let sec = time % 60;

        console.log(sec);

        if(sec < 10){
            con.html(min + ":0" + sec);
        }else{
            con.html(min + ":" + sec);
        }
        time--;
    }
}