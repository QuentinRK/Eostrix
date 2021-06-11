$(document).ready(() => {

    var socket = io();
    
    socket.on('connect', () => {
        socket.emit('client_connected', {data: ' Connected!'});
    
    });
    
    var crypto_list = ["BTCUSDT", "ETHUSDT", "XRPUSDT","LTCUSDT", "XMRUSDT", "BNBUSDT", "XLMUSDT",
                       "ETHBTC", "XRPBTC","LTCBTC", "XMRBTC", "BNBBTC", "XLMBTC"]

    var price_change = [];
    
    socket.on('my_response', (crypto) => {

        price_change.length = 0;

        crypto_list.forEach((data) => {

            var last_price = $("." + `${data}`+ " #" +`${data}`+ "1").text(); 
            var current_price = crypto.data[`${data}`]['price'];
            var percent_change = crypto.data[`${data}`]['price_change'];
            var crypto_class = "." + `${data}`;
            var crypto_id = crypto_class +  " #" +`${data}`+ "1";

            price_change.push(percent_change);

            $(crypto_id).text(current_price);
            $(crypto_id).css("color", "white");
            
            if( parseFloat(last_price) > parseFloat(current_price)){

                $(crypto_class).css("backgroundColor", "red");
            }

            if( parseFloat(last_price) < parseFloat(current_price)){

                $(crypto_class).css("backgroundColor", "green");
            }
        })

        var ctx = document.getElementById('myChart').getContext('2d');

        var myChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: crypto_list,
                datasets: [{
                    label: '24hr Price Change (%)',
                    data: price_change,
                    backgroundColor: [
                      'rgba(255, 99, 132, 1)',
                      'rgba(54, 162, 235, 1)',
                      'rgba(255, 206, 86, 1)',
                      'rgba(75, 192, 192, 1)',
                      'rgba(153, 102, 255, 1)',
                      'rgba(255, 159, 64, 1)'
                    ],
                    borderColor: [
                        'rgba(255, 99, 132, 1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 206, 86, 1)',
                        'rgba(75, 192, 192, 1)',
                        'rgba(153, 102, 255, 1)',
                        'rgba(255, 159, 64, 1)'
                    ],
                    borderWidth: 1,
                    color: ['rgba(255, 255, 255, 255)']

                }]
            },
            options: {
                scales: {
                    y: {
                        // beginAtZero: true
                    }
                }
            }
        });

        
        console.log(price_change);

        
    })
  
})