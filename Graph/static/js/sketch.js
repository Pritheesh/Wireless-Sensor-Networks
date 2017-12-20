

var s = function(p) {

    p.setup = function () {
        var can = p.createCanvas(800, 800);
        can.parent('my-canvas-nodes');
        p.background(0);
        var json = JSON.parse(global.global2);
        var min_and_max = JSON.parse(global.global1);
        // var adj_list = JSON.parse(global.global4);
        // console.log(min_and_max);
        var factor = min_and_max['factor'];
        delete json.Promise;

        p.fill(255, 255, 0);


        for (var key in json) {
            if (json.hasOwnProperty(key)) {
                // var values = json[key];
                var point1 = json[key];

                p.ellipse(point1[0] * factor, point1[1] * factor, 3, 3);
                // for (var i = 1; i < values.length; i++) {
                //     stroke(255, 255, 255, 50);
                //     var value = values[i].toString();
                //     line(point1[0] * factor, point1[1] * factor, json[value][0][0] * factor, json[value][0][1] * factor);
                // }
            }
        }

        // var max_array = min_and_max["max"];
        // var min_array = min_and_max["min"];
        // for(var i = 0; i <  max_array.length; i++) {
        //     var max_point = max_array[i];
        //     var values = json[max_point.toString()];
        //     max_point = values[0]
        //     for(var j =1; j < values.length; j++) {
        //         var value = values[j].toString();
        //         stroke(255, 0, 0);
        //         line(max_point[0] * factor, max_point[1] * factor, json[value][0][0] * factor, json[value][0][1] * factor);
        //     }
        // }
        // for(var i = 0; i < min_array.length; i++) {
        //     var min_point = min_array[i];
        //     var values = json[min_point.toString()];
        //     min_point = values[0];
        //     for(var j =1; j < values.length; j++) {
        //         var value = values[j].toString();
        //         stroke(0, 0, 255);
        //         line(min_point[0] * factor, min_point[1] * factor, json[value][0][0] * factor, json[value][0][1] * factor);
        //     }
        // }


    }

    function draw() {
    }
}

var newp5 = new p5(s);

var t = function(p) {
    p.setup = function () {
        var can = p.createCanvas(800, 800);
        can.parent('my-canvas-edges');
        p.background(0, 0, 0, 0);
        var json = JSON.parse(global.global2);
        var min_and_max = JSON.parse(global.global1);
        var adj_list = JSON.parse(global.global4);
        console.log(min_and_max);
        var factor = min_and_max['factor'];

        p.fill(255, 255, 0);


        for (var key in json) {
            if (json.hasOwnProperty(key)) {
                var values = adj_list[key];
                var point1 = json[key];

                // p.ellipse(point1[0] * factor, point1[1] * factor, 3, 3);
                for (var i = 0; i < values.length; i++) {
                    p.stroke(255, 255, 255, 50);
                    var value = values[i].toString();
                    p.line(point1[0] * factor, point1[1] * factor, json[value][0] * factor, json[value][1] * factor);
                }
            }
        }

    }

    function draw() {
    }
}

var edgep5 = new p5(t);

var u = function(p) {
    p.setup = function () {
        var can = p.createCanvas(800, 800);
        can.parent('my-canvas-minmax');
        p.background(0, 0, 0, 0);
        var json = JSON.parse(global.global2);
        var min_and_max = JSON.parse(global.global1);
        var adj_list = JSON.parse(global.global4);
        // console.log(min_and_max);
        var factor = min_and_max['factor'];

        p.fill(255, 255, 0);


        // for (var key in json) {
        //     if (json.hasOwnProperty(key)) {
        //         var values = json[key];
        //         var point1 = json[key][0];
        //
        //         // p.ellipse(point1[0] * factor, point1[1] * factor, 3, 3);
        //     }
        // }
        var max_array = min_and_max["max"];
        var min_array = min_and_max["min"];
        for(var i = 0; i < min_array.length; i++) {
            var min_point = min_array[i];
            var values = adj_list[min_point.toString()];
            min_point = json[min_point.toString()];
            for(var j = 0; j < values.length; j++) {
                var value = values[j].toString();
                p.stroke(0, 0, 255);
                p.line(min_point[0] * factor, min_point[1] * factor, json[value][0] * factor, json[value][1] * factor);
            }
        }

        for(var i = 0; i <  max_array.length; i++) {
            var max_point = max_array[i];
            var values = adj_list[max_point.toString()];
            max_point = json[max_point.toString()];
            for(var j =0; j < values.length; j++) {
                var value = values[j].toString();
                // console.log(json[value]);
                p.stroke(255, 0, 0);
                p.line(max_point[0] * factor, max_point[1] * factor, json[value][0] * factor, json[value][1] * factor);
            }
        }

    }

    function draw() {
    }
}

var minmaxp5 = new p5(u);

var v = function(p) {

    p.setup = function () {
        p.noStroke();
        var can = p.createCanvas(800, 800);
        can.parent('my-canvas-smallest');
        p.background(0, 0, 0, 0);
        var json = JSON.parse(global.global2);
        var min_and_max = JSON.parse(global.global1);
        var colors = JSON.parse(global.global3);
        var factor = min_and_max['factor'];

        // p.fill(255, 255, 0);


        for (var key in json) {
            if (json.hasOwnProperty(key)) {
                // var values = json[key];
                var point1 = json[key];
                // console.log(color[key]);

                var color = colors[key];
                p.fill(color[0], color[1], color[2]);
                p.ellipse(point1[0] * factor, point1[1] * factor, 8, 8);
                // for (var i = 1; i < values.length; i++) {
                //     stroke(255, 255, 255, 50);
                //     var value = values[i].toString();
                //     line(point1[0] * factor, point1[1] * factor, json[value][0][0] * factor, json[value][0][1] * factor);
                // }
            }
        }
    }
}

var smallest_lastp5 = new p5(v);

var b1 = function (p) {
    p.setup = function () {
        p.noStroke();
        var can = p.createCanvas(800, 800);
        can.parent('my-canvas-backbone1');
        p.background(0);
        var edges = JSON.parse(global.edges1);
        var colors = JSON.parse(global.global3);
        var min_and_max = JSON.parse(global.global1);
        var factor = min_and_max['factor'];
        var json = JSON.parse(global.global2);



        for(var key in edges) {
            if (edges.hasOwnProperty(key)) {
                var point1 = edges[key];
                var color = colors[key];
                p.fill(color[0], color[1], color[2]);
                p.ellipse(json[key][0] * factor, json[key][1] * factor, 8, 8);

                for (var i = 0; i < point1.length; i++) {
                    p.stroke(255, 255, 255, 50);
                    var value = point1[i];
                    p.line(json[key][0] * factor, json[key][1] * factor, json[value][0] * factor, json[value][1] * factor);
                }
            }
        }
    }
}

var backbone1 = new p5(b1);

var b2 = function (p) {
    p.setup = function () {
        p.noStroke();
        var can = p.createCanvas(800, 800);
        can.parent('my-canvas-backbone2');
        p.background(0);
        var edges = JSON.parse(global.edges2);
        var colors = JSON.parse(global.global3);
        var min_and_max = JSON.parse(global.global1);
        var factor = min_and_max['factor'];
        var json = JSON.parse(global.global2);



        for(var key in edges) {
            if (edges.hasOwnProperty(key)) {
                var point1 = edges[key];
                var color = colors[key];
                p.fill(color[0], color[1], color[2]);
                p.ellipse(json[key][0] * factor, json[key][1] * factor, 8, 8);

                for (var i = 0; i < point1.length; i++) {
                    p.stroke(255, 255, 255, 50);
                    var value = point1[i];
                    p.line(json[key][0] * factor, json[key][1] * factor, json[value][0] * factor, json[value][1] * factor);
                }
            }
        }
    }
}

var backbone1 = new p5(b2);
