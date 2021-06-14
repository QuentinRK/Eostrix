const CronJob = require('cron').CronJob;

$(document).ready(() => {

    // Initialising the websocket connection to the server 
    var socket = io();
    
    socket.on('connect', () => {
        socket.emit('client_connected', {data: ' Connected!'});
    
    });
    

    var crypto_list = ["BTCUSDT", "ETHUSDT", "XRPUSDT","LTCUSDT", "XMRUSDT", "BNBUSDT", "XLMUSDT",
                       "ETHBTC", "XRPBTC","LTCBTC", "XMRBTC", "BNBBTC", "XLMBTC"]

    // Variables that hold data for the chart 
    var price_change = [];
    var symbol_list = []

    
    socket.on('my_response', (crypto) => {

        /* 
            In response to crypto data being sent from the server, 
            the program iterates through each currency pair in the crypto list 
            to gather the corresponding data such as price and price change. 
        */ 
        crypto_list.forEach((data) => {

            // Gather the text of the currency pair that is dynamically generated in html 
            var symbol = `${data}`;
            var last_price = $("." + symbol+ " #" +symbol + "1").text();

            // Extract the data from the Json Object 
            var current_price = crypto.data[symbol]['price'];
            var percent_change = crypto.data[symbol]['price_change'];

            var crypto_class = "." + symbol;
            var crypto_id = crypto_class +  " #" + symbol + "1";

            // Change the text to the current price 
            $(crypto_id).text(current_price);
            $(crypto_id).css("color", "white");
            
            if(parseFloat(last_price) > parseFloat(current_price)){

                // If the last price was greater then change the color of the row to red 
                $(crypto_class).css("backgroundColor", "red");
            }

            if( parseFloat(last_price) < parseFloat(current_price)){

                $(crypto_class).css("backgroundColor", "green");
            }

           
            /*
                This if statement is reponsible for populating the price_change array.
                The symbol list is populated at the same time so both the price and symbol
                have the same index in both arrays.
            */
            if((price_change.length < 13) && (percent_change != null)){

                if(!symbol_list.includes(symbol)){

                    price_change.push(percent_change)
                    symbol_list.push(symbol) 
                }
                // Update the chart
                addData(myChart, price_change, symbol_list)

            }
        })
        
        
    })

    // Setup for Chart.js
    var ctx = document.getElementById('myChart').getContext('2d');

    var myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: symbol_list,
            datasets: [{
                label: '24hr Price Change (%)',
                data: price_change,
                backgroundColor: [
                  'rgba(54, 162, 235, 1)',
                ],
                borderWidth: 1,
                color: ['rgba(54, 162, 235, 1)']

            }]
    
        }
    });


    // Function responsible for updating the chart 
    function addData(chart, data, labels){
        chart.data.labels = labels
        chart.data.datasets[0].data = data;
        chart.update()
    }

    /*
        The price change and symbol list are cleared every 24 hours.
        This is because the API that the data is being taken from updates,
        the information at this rate (24hr Ticker).
    */
    const job = new CronJob('0 0 */23 * * *', function() {

        socket.emit('ticker_update', {percentage: price_change,
                                      crypto: symbol_list})
        price_change.length = 0;
        symbol_list.length = 0;
        
    });

    job.start()

})




