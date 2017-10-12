function setup() {
    createCanvas(1000, 1000);
    background(0);
    var count = 0;
    // var json = document.getElementById("myVar").value;
    var json = JSON.parse(global.global2);
    var min_and_max = JSON.parse(global.global1);
    delete json.Promise;
    // console.log(json);

    var max_point = json[min_and_max['max'].toString()][0];
    // console.log(max_point);
    // fill(255, 0, 0, 100);
    // ellipse(max_point[0] * 1000, max_point[1] * 1000, 10, 10);
    //
    var min_point = json[min_and_max['min'].toString()][0];
    // console.log(min_point);
    // fill(0, 255, 0, 100);
    // ellipse(min_point[0] * 1000, min_point[1] * 1000, 10, 10);

    for (var key in json) {
        // console.log("key = ",key);
        if( json.hasOwnProperty(key)) {
            var values = json[key];
            // console.log(values);
            // var key1 = JSON.parse(key);
            // console.log(key);
            // console.log("key1 = ",json[key1]);
            var point1 = json[key][0];
            // console.log("point = ", point1[0]);
            fill(255, 155, 64, 100);
            stroke(0, 150, 0);

            ellipse(point1[0] * 1000, point1[1] * 1000, 4, 4);
            if((point1[0] == max_point[0]) || (point1[0] == min_point[0])){
                continue;
            }
            for (var i = 1; i < values.length; i++) {
                // count++;
                var value = values[i].toString();
                line(point1[0] * 1000, point1[1] * 1000, json[value][0][0] * 1000, json[value][0][1] * 1000);
                // console.log("plotted = ", point1, "and ", json[value][0]);
            }
        }
    }

    var point1 = max_point;
    var values = json[min_and_max['max'].toString()];
    stroke(255, 0, 0);
    for(var i = 0; i < 2; i++) {
        for(var j =1; j < values.length; j++) {
            var value = values[j].toString();
            console.log(value);
            line(point1[0] * 1000, point1[1] * 1000, json[value][0][0] * 1000, json[value][0][1] * 1000);
        }
        stroke(0, 0, 255);
        point1 = min_point;
        values = json[min_and_max['min'].toString()];
    }

}

function draw() {
    // console.log("Get lost please");
}