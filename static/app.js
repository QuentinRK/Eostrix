$(document).ready(() => {

    var socket = io();
    
    socket.on('connect', () => {
        socket.emit('client_connected', {data: ' Connected!'});
    
    });
    
    var crypto_list = ["BTCUSDT", "ETHUSDT", "XRPUSDT","LTCUSDT", "XMRUSDT", "BNBUSDT", "XLMUSDT",
                       "ETHBTC", "XRPBTC","LTCBTC", "XMRBTC", "BNBBTC", "XLMBTC"]

    var price_change = [];
    var symbol_list = []

    
    socket.on('my_response', (crypto) => {

        crypto_list.forEach((data) => {

            symbol = `${data}`;
            var last_price = $("." + symbol+ " #" +symbol + "1").text(); 
            var current_price = crypto.data[symbol]['price'];
            var percent_change = crypto.data[symbol]['price_change'];
            var crypto_class = "." + symbol;
            var crypto_id = crypto_class +  " #" + symbol + "1";


            $(crypto_id).text(current_price);
            $(crypto_id).css("color", "white");
            
            if( parseFloat(last_price) > parseFloat(current_price)){

                $(crypto_class).css("backgroundColor", "red");
            }

            if( parseFloat(last_price) < parseFloat(current_price)){

                $(crypto_class).css("backgroundColor", "green");
            }

            
            if((price_change.length < 13) && (percent_change != null)){

                price_change.push(percent_change)
                symbol_list.push(symbol)
                addData(myChart, price_change, symbol_list)

            }
        })
        
        
    })

    var ctx = document.getElementById('myChart').getContext('2d');

    var myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: symbol_list,
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
        }
    });


    function addData(chart, data, labels){
        chart.data.labels = labels
        chart.data.datasets[0].data = data;
        chart.update()
    }
  
})