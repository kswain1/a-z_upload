

//draw the doughnut
var doughnutArray = [document.getElementById('doughnut').getContext('2d'), document.getElementById('doughnut2').getContext('2d'), document.getElementById('doughnut3').getContext('2d'), document.getElementById('doughnut4').getContext('2d')];
for (var i = 0; i < doughnutArray.length; i++) {
  doughnutArray[i].lineWidth = 5; //thickness of the line
  doughnutArray[i].fillStyle = '#A9A9A9';
  doughnutArray[i].strokeStyle = "#A9A9A9";
  doughnutArray[i].beginPath();
  doughnutArray[i].arc(60, 60, 55, 4.72, 15, false); //.arc(x, y , radius, startAngle, endAngle, anticlockwise)
  doughnutArray[i].stroke();
}
window.onload = function() {
    loadSkills1(htScore);
    loadSkills2(endurance);
    loadSkills3(balance);
    loadSkills4(comfort);
  }

  /*Load skills one function*/
function loadSkills1(htScore) {
  var ctx = document.getElementById('skill1').getContext('2d');
  var al = 0;
  var start = 4.72;
  var cw = ctx.canvas.width;
  var ch = ctx.canvas.height;
  var diff;

  function progressSim() {
    diff = ((al / 100) * Math.PI * 2 * 10).toFixed(2); //change the arc by multiplying .. * Math.PI*2* --> 7.5=75, 5=50 etc.
    ctx.clearRect(0, 0, cw, ch);
    ctx.lineWidth = 5; //thickness of the line
    ctx.fillStyle = '#1e3d60';
    ctx.strokeStyle = "#1e3d60";
    ctx.textAlign = 'center';
    ctx.font = "30px Nucleo Outline";
    ctx.fillText(al + '%', cw * .5 + 2, ch * .5 + 8, cw);
    ctx.beginPath();
    ctx.arc(60, 60, 55, start, diff / 10 + start, false); //.arc(x, y , radius, startAngle, endAngle, anticlockwise)
    ctx.stroke();
    if (al >= htScore[0]) { // stop the recreation at your desired point, i.e change 100 to 75 if you need just 75%.
      clearTimeout(sim);
      // Add scripting here that will run when progress completes
    }
    al++;
  }
  var sim = setInterval(progressSim, 20); //speed
}
/*loadSkills2 function*/
function loadSkills2(endurance) {
  var ctx = document.getElementById('skill2').getContext('2d');
  var al = 0;
  var start = 4.72;
  var cw = ctx.canvas.width;
  var ch = ctx.canvas.height;
  var diff;

  function progressSim() {
    diff = ((al / 100) * Math.PI * 2 * 10).toFixed(2); //change the arc by multiplying .. * Math.PI*2* --> 7.5=75, 5=50 etc.
    ctx.clearRect(0, 0, cw, ch);
    ctx.lineWidth = 5; //thickness of the line
    ctx.fillStyle = "#1e3d60";
    ctx.strokeStyle = "#1e3d60";
    ctx.textAlign = 'center';
    ctx.font = "30px Nucleo Outline";
    ctx.fillText(al + '%', cw * .5 + 2, ch * .5 + 8, cw);
    ctx.beginPath();
    ctx.arc(60, 60, 55, start, diff / 10 + start, false); //.arc(x, y , radius, startAngle, endAngle, anticlockwise)
    ctx.stroke();
    if (al >= endurance[0]) { // stop the recreation at your desired point, i.e change 100 to 75 if you need just 75%.
      clearTimeout(sim);
      // Add scripting here that will run when progress completes
    }
    al++;
  }
  var sim = setInterval(progressSim, 30); //speed
}

/* loadSkill3 function*/
function loadSkills3(balance) {
  var ctx = document.getElementById('skill3').getContext('2d');
  var al = 0;
  var start = 4.72;
  var cw = ctx.canvas.width;
  var ch = ctx.canvas.height;
  var diff;

  function progressSim() {
    diff = ((al / 100) * Math.PI * 2 * 10).toFixed(2); //change the arc by multiplying .. * Math.PI*2* --> 7.5=75, 5=50 etc.
    ctx.clearRect(0, 0, cw, ch);
    ctx.lineWidth = 5; //thickness of the line
    ctx.fillStyle = "#1e3d60";
    ctx.strokeStyle = "#1e3d60";
    ctx.textAlign = 'center';
    ctx.font = "30px Radley";
    ctx.fillText(al + '%', cw * .5 + 2, ch * .5 + 8, cw);
    ctx.beginPath();
    ctx.arc(60, 60, 55, start, diff / 10 + start, false); //.arc(x, y , radius, startAngle, endAngle, anticlockwise)
    ctx.stroke();
    if (al >= balance) { // stop the recreation at your desired point, i.e change 100 to 75 if you need just 75%.
      clearTimeout(sim);
      // Add scripting here that will run when progress completes
    }
    al++;
  }
  var sim = setInterval(progressSim, 40); //speed
}
/* loadSkill4 function*/
function loadSkills4(comfort) {
  var ctx = document.getElementById('skill4').getContext('2d');
  var al = 0;
  var start = 4.72;
  var cw = ctx.canvas.width;
  var ch = ctx.canvas.height;
  var diff;

  function progressSim() {
    diff = ((al / 100) * Math.PI * 2 * 10).toFixed(2); //change the arc by multiplying .. * Math.PI*2* --> 7.5=75, 5=50 etc.
    ctx.clearRect(0, 0, cw, ch);
    ctx.lineWidth = 5; //thickness of the line
    ctx.fillStyle = "#1e3d60";
    ctx.strokeStyle = "#1e3d60";
    ctx.textAlign = 'center';
    ctx.font = "30px Radley";
    ctx.fillText(al + '%', cw * .5 + 2, ch * .5 + 8, cw);
    ctx.beginPath();
    ctx.arc(60, 60, 55, start, diff / 10 + start, false); //.arc(x, y , radius, startAngle, endAngle, anticlockwise)
    ctx.stroke();
    if (al >= comfort[0]) { // stop the recreation at your desired point, i.e change 100 to 75 if you need just 75%.
      clearTimeout(sim);
      // Add scripting here that will run when progress completes
    }
    al++;
  }
  var sim = setInterval(progressSim, 50); //speed
}