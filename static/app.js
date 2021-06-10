$(document).ready(() => {

    var socket = io();
    
    socket.on('connect', () => {
        socket.emit('client_connected', {data: ' Connected!'});
    
    });
    

    var crypto_list = ["BTCUSDT", "ETHUSDT", "XRPUSDT","LTCUSDT", "XMRUSDT","ETHBTC", "XRPBTC","LTCBTC", "XMRBTC"]

    
    socket.on('my_response', (crypto) => {

        crypto_list.forEach((data) => {

            var last_price = $("." + `${data}`+ " #" +`${data}`+ "1").text(); 
            var current_price = crypto.data[`${data}`]['Price']

            $("." + `${data}`+ " #" +`${data}`+ "1").text(current_price);
            $("." + `${data}`+ " #" +`${data}`+ "1").css("color", "white");
            
            if( parseFloat(last_price) > parseFloat(current_price)){

                $("." + `${data}`).css("backgroundColor", "red");
            }

            if( parseFloat(last_price) < parseFloat(current_price)){

                $("." + `${data}`).css("backgroundColor", "green");
            }

        })

    })

});