window.requestAnimFrame = (function(){
    return  window.requestAnimationFrame       ||
        window.webkitRequestAnimationFrame ||
        window.mozRequestAnimationFrame    ||
        function( callback ){
            window.setTimeout(callback, 1000 / 60);
        };
})();



$( document ).ready(function() {

//*************************************** HTML-circle progress bar **********************************//

var canvas = document.getElementById("HTML");
var cxtHTML = canvas.getContext('2d');

var width = 300;
var height = 230;
canvas.width = width;
canvas.height = height;

var center = {x: width/2, y: height/2};
var value = .75;
var initialValue = 0;

var rotation =   Math.PI /2;



 function drawHTML(){

    if (Math.abs(initialValue - value) < .0)
        initialValue = value;

    if (initialValue != value) {
        initialValue += (value - initialValue)/50;
        $('.widgetHTML h2').html(Math.round(initialValue * 100) + '%');
    }

		 cxtHTML.clearRect(0,0,width,height);
		 cxtHTML.save();

		 cxtHTML.translate(center.x,center.y);
		 cxtHTML.rotate(rotation);

		 cxtHTML.lineWidth = 18;
		 cxtHTML.beginPath();
		 cxtHTML.arc(0,  0, 100, 0, Math.PI*2, false);
		 cxtHTML.strokeStyle ='#dadada';
		 cxtHTML.shadowBlur = 10;
		 cxtHTML.shadowColor="rgba(0,0,0,.5)";
		 cxtHTML.shadowOffsetX = 0;
		 cxtHTML.shadowOffsetY = 4;
		 cxtHTML.stroke();

		 cxtHTML.beginPath();
		 cxtHTML.arc(0, 0, 100, rotation, Math.PI * 2 * initialValue + rotation, false);
		 cxtHTML.strokeStyle = '#1300BE';
		 cxtHTML.shadowBlur = 10;
		 cxtHTML.shadowColor="rgba(0,0,0,.5)";
		 cxtHTML.shadowOffsetX = 0;
		 cxtHTML.shadowOffsetY = 4;
		 cxtHTML.stroke();

		 cxtHTML.restore();
		 requestAnimFrame(drawHTML);
};

//*************************************** CSS-circle progress bar **********************************//

    var canvasCSS = document.getElementById("CSS");
    var cxtCSS = canvasCSS.getContext('2d');
    canvasCSS.width = width;
    canvasCSS.height = height;
    var valueCSS = .80;
    var initialValueCSS = 0;

function drawCSS(){

    if (Math.abs(initialValueCSS - valueCSS) < .0)
        initialValueCSS = valueCSS;

    if (initialValueCSS != valueCSS) {
        initialValueCSS += (valueCSS - initialValueCSS)/50;
        $('.widgetCSS h2').html(Math.round(initialValueCSS * 100) + '%');
    }

		cxtCSS.clearRect(0,0,width,height);
		cxtCSS.save();

		cxtCSS.translate(center.x,center.y);
		cxtCSS.rotate(rotation);

		cxtCSS.lineWidth = 18;
		cxtCSS.beginPath();
		cxtCSS.arc(0,  0, 100, 0, Math.PI*2, false);
		cxtCSS.strokeStyle ='#dadada';
		cxtCSS.shadowBlur = 10;
		cxtCSS.shadowColor="rgba(0,0,0,.5)";
		cxtCSS.shadowOffsetX = 0;
		cxtCSS.shadowOffsetY = 4;
		cxtCSS.stroke();

		cxtCSS.beginPath();
		cxtCSS.arc(0, 0, 100, rotation, Math.PI * 2 * initialValueCSS + rotation, false);
		cxtCSS.strokeStyle = '#1300BE';
		cxtCSS.shadowBlur = 10;
		cxtCSS.shadowColor="rgba(0,0,0,.5)";
		cxtCSS.shadowOffsetX = 0;
		cxtCSS.shadowOffsetY = 4;
		cxtCSS.stroke();

		cxtCSS.restore();
		requestAnimFrame(drawCSS);
};


//*************************************** WP-circle progress bar **********************************//


    var canvasWP = document.getElementById("WP");
    var cxtWP = canvasWP.getContext('2d');
    canvasWP.width = width;
    canvasWP.height = height;
    var valueWP = .70;
    var initialValueWP = 0;

    function drawWP(){

        if (Math.abs(initialValueWP - valueWP) < .0)
            initialValueWP = valueWP;

        if (initialValueWP != valueWP) {
            initialValueWP += (valueWP - initialValueWP)/50;
            $('.widgetWP h2').html(Math.round(initialValueWP * 100) + '%');
        }

			 cxtWP.clearRect(0,0,width,height);
			 cxtWP.save();

			 cxtWP.translate(center.x,center.y);
			 cxtWP.rotate(rotation);

			 cxtWP.lineWidth = 18;
			 cxtWP.beginPath();
			 cxtWP.arc(0,  0, 100, 0, Math.PI*2, false);
			 cxtWP.strokeStyle ='#dadada';
			 cxtCSS.shadowBlur = 10;
			 cxtWP.shadowColor="rgba(0,0,0,.5)";
			 cxtWP.shadowOffsetX = 0;
			 cxtWP.shadowOffsetY = 4;
			 cxtWP.stroke();

			 cxtWP.beginPath();
			 cxtWP.arc(0, 0, 100, rotation, Math.PI * 2 * initialValueWP + rotation, false);
			 cxtWP.strokeStyle = '#1300BE';
			 cxtWP.shadowBlur = 10;
			 cxtWP.shadowColor="rgba(0,0,0,.5)";
			 cxtWP.shadowOffsetX = 0;
			 cxtWP.shadowOffsetY = 4;
			 cxtWP.stroke();

			 cxtWP.restore();
			 requestAnimFrame(drawWP);
    };

//*************************************** SEO-circle progress bar **********************************//


    var canvasSEO = document.getElementById("SEO");
    var cxtSEO = canvasSEO.getContext('2d');
    canvasSEO.width = width;
    canvasSEO.height = height;
    var valueSEO = .85;
    var initialValueSEO = 0;

    function drawSEO(){

        if (Math.abs(initialValueSEO - valueSEO) < .0)
            initialValueSEO = valueSEO;

        if (initialValueSEO != valueSEO) {
            initialValueSEO += (valueSEO - initialValueSEO)/50;
            $('.widgetSEO h2').html(Math.round(initialValueSEO * 100) + '%');
        }

			 cxtSEO.clearRect(0,0,width,height);
			 cxtSEO.save();

			 cxtSEO.translate(center.x,center.y);
			 cxtSEO.rotate(rotation);

			 cxtSEO.lineWidth = 18;
			 cxtSEO.beginPath();
			 cxtSEO.arc(0,  0, 100, 0, Math.PI*2, false);
			 cxtSEO.strokeStyle ='#dadada';
			 cxtSEO.shadowBlur = 10;
			 cxtSEO.shadowColor="rgba(0,0,0,.5)";
			 cxtSEO.shadowOffsetX = 0;
			 cxtSEO.shadowOffsetY = 4;
			 cxtSEO.stroke();

			 cxtSEO.beginPath();
			 cxtSEO.arc(0, 0, 100, rotation, Math.PI * 2 * initialValueSEO + rotation, false);
			 cxtSEO.strokeStyle = '#1300BE';
			 cxtSEO.shadowBlur = 10;
			 cxtSEO.shadowColor="rgba(0,0,0,.5)";
			 cxtSEO.shadowOffsetX = 0;
			 cxtSEO.shadowOffsetY = 4;
			 cxtSEO.stroke();

			 cxtSEO.restore();
			 requestAnimFrame(drawSEO);
    };

	drawHTML();
	drawCSS();
	drawWP();
	drawSEO();

});