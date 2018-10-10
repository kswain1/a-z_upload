       type: 'bar',
              data: {
                labels: ["Risk Areas"],
                datasets: [
                {
                  label: "Low",
                  // borderColor: chartColor,
                  // pointBorderColor: chartColor,
                  // pointBackgroundColor: "#1e3d60",
                  // pointHoverBackgroundColor: "#1e3d60",
                  // pointHoverBorderColor: chartColor,
                  // pointBorderWidth: 1,
                  // pointHoverRadius: 7,
                  // pointHoverBorderWidth: 2,
                  // pointRadius: 5,
                  // fill: true,
                  // backgroundColor: gradientFill,
                  // borderWidth: 2,
                  "data": [{{ data.tib_anterior_rle[0] }}],
                   "backgroundColor":'#EBCCD1' , //red
                  },
                  {
                    "label": "Medium",
                    "data": [{{ data.tib_anterior_rle[1] }}],
                     "backgroundColor":'#FAEBCC' , //yellow
                }]
              },
              options: {
                layout: {
                  padding: {
                    left: 20,
                    right: 20,
                    top: 0,
                    bottom: 0
                  }
                },
                maintainAspectRatio: false,
                tooltips: {
                  backgroundColor: '#fff',
                  titleFontColor: '#333',
                  bodyFontColor: '#666',
                  bodySpacing: 4,
                  xPadding: 12,
                  mode: "nearest",
                  intersect: 0,
                  position: "nearest"
                },
                legend: {
                  position: "bottom",
                  fillStyle: "#FFF",
                  display: false
                },
                scales: {
                  yAxes: [{
                    stacked: true,
                    ticks: {
                      fontColor: "rgba(255,255,255,0.4)",
                      fontStyle: "bold",
                      beginAtZero: true,
                      maxTicksLimit: 5,
                      padding: 10,

                    },
                    gridLines: {
                      drawTicks: true,
                      drawBorder: false,
                      display: true,
                      color: "rgba(255,255,255,0.1)",
                      zeroLineColor: "transparent"
                    }

                  }],
                  xAxes: [{
                    stacked: true,
                    gridLines: {
                      zeroLineColor: "transparent",
                      display: false,

                    },
                    ticks: {
                      padding: 10,
                      fontColor: "rgba(255,255,255,0.4)",
                      fontStyle: "bold"
                    }
                  }]
                }
              }
            });


            var myChart = new Chart(ctx, {
              type: 'line',
              data: {
                labels: ["Anterior Direction", "Post Medial Direction", "Post Lateral Direction", "Composite Score"],
                datasets: [
                {
                    label:"Left Lower Extremity"
                    borderColor: chartColor,
                    pointBorderColor: chartColor,
                    pointBackgroundColor: "#1e3d60",
                    pointHoverBackgroundColor: "#1e3d60",
                    pointHoverBorderColor: chartColor,
                    pointBorderWidth: 1,
                    pointHoverRadius: 7,
                    pointHoverBorderWidth: 2,
                    pointRadius: 5,
                    fill: true,
                    backgroundColor: gradientFill,
                    borderWidth: 2,
                    data: [56, 94, 94, 80.36],
                  },
                  {
                    label:"Right Lower Extremity"
                    borderColor: chartColor,
                    pointBorderColor: chartColor,
                    pointBackgroundColor: "#1e3d60",
                    pointHoverBackgroundColor: "#1e3d60",
                    pointHoverBorderColor: chartColor,
                    pointBorderWidth: 1,
                    pointHoverRadius: 7,
                    pointHoverBorderWidth: 2,
                    pointRadius: 5,
                    fill: true,
                    backgroundColor: gradientFill,
                    borderWidth: 2,
                    data: [56, 94, 92, 79.41],
                }]
              },
              options: {
                layout: {
                  padding: {
                    left: 20,
                    right: 20,
                    top: 0,
                    bottom: 0
                  }
                },
                maintainAspectRatio: false,
                tooltips: {
                  backgroundColor: '#fff',
                  titleFontColor: '#333',
                  bodyFontColor: '#666',
                  bodySpacing: 4,
                  xPadding: 12,
                  mode: "nearest",
                  intersect: 0,
                  position: "nearest"
                },
                legend: {
                  position: "bottom",
                  fillStyle: "#FFF",
                  display: false
                },
                scales: {
                  yAxes: [{
                    stacked: true,
                    ticks: {
                      fontColor: "rgba(255,255,255,0.4)",
                      fontStyle: "bold",
                      beginAtZero: true,
                      maxTicksLimit: 5,
                      padding: 10,

                    },
                    gridLines: {
                      drawTicks: true,
                      drawBorder: false,
                      display: true,
                      color: "rgba(255,255,255,0.1)",
                      zeroLineColor: "transparent"
                    }

                  }],
                  xAxes: [{
                    stacked: true,
                    gridLines: {
                      zeroLineColor: "transparent",
                      display: false,

                    },
                    ticks: {
                      padding: 10,
                      fontColor: "rgba(255,255,255,0.4)",
                      fontStyle: "bold"
                    }
                  }]
                }
              }
            });