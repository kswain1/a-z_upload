gradientChartOptionsConfigurationWithNumbersAndGrid = {
    maintainAspectRatio: false,
    legend: {
      display: true
    },
    tooltips: {
      bodySpacing: 4,
      mode: "nearest",
      intersect: 0,
      position: "nearest",
      xPadding: 10,
      yPadding: 20,
      caretPadding: 5
    },
    responsive: true,
    scales: {
      yAxes: [{
        gridLines: 0,
        gridLines: {
          zeroLineColor: "transparent",
          drawBorder: false
        }
      }],
      xAxes: [{
        display: 0,
        gridLines: 0,
        //labels: true,
        // ticks: {
        //   display: true
        // },
        // gridLines: {
        //   zeroLineColor: "transparent",
        //   drawTicks: true,
        //   display: true,
        //   drawBorder: false
        // }
      }]
    },
    layout: {
      padding: {
        left: 0,
        right: 0,
        top: 15,
        bottom: 5
      }
    }
  };

var cardStatsMiniLineColor = "#fff",
cardStatsMiniDotColor = "#fff";

ctx = document.getElementById('comfortChart').getContext("2d");

            gradientStroke = ctx.createLinearGradient(500, 0, 100, 0);
            gradientStroke.addColorStop(0, '#18ce0f');
            gradientStroke.addColorStop(1, chartColor);

            gradientFill = ctx.createLinearGradient(0, 170, 0, 50);
            gradientFill.addColorStop(0, "rgba(128, 182, 244, 0)");
            gradientFill.addColorStop(1, hexToRGB('#18ce0f', 0.4));

            myChart = new Chart(ctx, {
              type: 'bar',
              responsive: true,
              data: {
                labels: productNameList,
                datasets: [{
                  label: "Comfort Scores ",
                  borderColor: "#18ce0f",
                  pointBorderColor: "#FFF",
                  pointBackgroundColor: "#18ce0f",
                  pointBorderWidth: 2,
                  pointHoverRadius: 4,
                  pointHoverBorderWidth: 1,
                  pointRadius: 4,
                  fill: true,
                  backgroundColor: gradientFill,
                  borderWidth: 2,
                  data: comfort
                }]
              },
              options: gradientChartOptionsConfigurationWithNumbersAndGrid
            });
