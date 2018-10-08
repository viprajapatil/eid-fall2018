var sensorLib = require("node-dht-sensor");
var temp_array = [];
var hum_array = [];
var avg_temp = 0;
var avg_hum = 0;
var count = 1;
var sensor = {
	sensors: [ {
		name: "DHT22",
		type: 22,
		pin: 4
	} ],
	read: function() {
		for (var a in this.sensors) {
			var b = sensorLib.read(this.sensors[a].type, this.sensors[a].pin);
			console.log(count + "- Temp" +
				b.temperature.toFixed(1) + "°C, " +
				b.humidity.toFixed(1) + "% Hum");
			temp_array.push(b.temperature.toFixed(1));
                        hum_array.push(b.humidity.toFixed(1));
			console.log(temp_array[0]);
			if (count%10 == 0)
			{       avg_temp = 0;
				avg_hum = 0;
				for(var i = 0; i<count; i++)
                        	{
			            avg_temp +=temp_array[i];
                        	}
				avg_temp = avg_temp/count;
				for(var i = 0; i<count; i++)
                                {
                                    avg_hum += hum_array[i];				    }
                                }
			        avg_hum = avg_hum/count;

				console.log("Lowest Temp "+Math.min(...temp_array)+" degC");
                                console.log("Lowest Hum "+Math.min(...hum_array)+" %");
                                console.log("Highest Temp "+Math.max(...temp_array)+" degC");
                                console.log("Highest Hum "+Math.max(...hum_array)+" %");
				console.log("Average Temp "+avg_temp+" degC");
				console.log("Average Hum "+avg_hum+" %");
		        }
              		count++;
		}
		setTimeout(function() {
			sensor.read();
		}, 1000);
	}
};

sensor.read();


