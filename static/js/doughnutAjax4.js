/* loadSkill4 function*/
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
    clearTimeout(sim4);
    // Add scripting here that will run when progress completes
  }
  al++;
}
var sim4 = setInterval(progressSim, 20); //speed