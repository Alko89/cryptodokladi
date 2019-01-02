<template>
  <div>
    <!--Stats cards-->
    <div class="row">
      <div class="col-md-6 col-xl-3" v-for="stats in statsCards" :key="stats.title">
        <stats-card>
          <div class="icon-big text-center" :class="`icon-${stats.type}`" slot="header">
            <i :class="stats.icon"></i>
          </div>
          <div class="numbers" slot="content">
            <p>{{stats.title}}</p>
            {{stats.value}}
          </div>
          <div class="stats" slot="footer">
            <i :class="stats.footerIcon"></i> {{stats.footerText}}
          </div>
        </stats-card>
      </div>
    </div>

    <!--Charts-->
    <div class="row">
      <div class="col-md-6 col-12">
        <card>
          <template slot="header">
            <h4 class="card-title">
              <slot name="title">PIVX</slot>
            </h4>
            <p class="card-category">
              <slot name="subTitle">All Time</slot>
            </p>
          </template>
          <apexcharts type="area" height="245" :options="chartOptions" :series="series"/>
        </card>
      </div>

      <div class="col-md-6 col-12">
        <card>
          <template slot="header">
            <h4 class="card-title">
              <slot name="title">Rewards distribution</slot>
            </h4>
            <p class="card-category">
              <slot name="subTitle">All Time</slot>
            </p>
          </template>
          <apexcharts type="pie" height="245" :options="rewardsDistribution.options" :series="rewardsDistribution.series"/>
        </card>
      </div>
    </div>
  </div>
</template>
<script>
import { StatsCard } from "@/components/index";
import VueApexCharts from "vue-apexcharts";

import axios from "axios";

export default {
  mounted() {
    axios.get("/api/tokens").then(response => {
      this.tokens = response.data;

      // this.tokens.forEach(token => {

      // });
    });

    axios.get("/api/transactions/" + this.user.name + "/PIVX").then(response => {
      this.transactions.token = "PIVX";
      this.transactions.transactions = response.data;

      var series = [];
      var labels = [];
      var value = 0;
      response.data.forEach(transaction => {
        value += transaction.value;
        labels.push(transaction.timestamp);
        series.push(value);
      });

      this.chartOptions = {
        colors: ['purple'],
        dataLabels: {
          enabled: false
        },
        stroke: {
          curve: "smooth"
        },

        xaxis: {
          type: "datetime",
          categories: labels
        },
        tooltip: {
          x: {
            format: "dd/MM/yy HH:mm"
          }
        }
      }
      this.series = [
        {
          name: "PIVX",
          data: series
        }
      ];

      axios.get("/api/ticker/PIVX").then(response => {
        this.statsCards[1].footerText = (value * response.data[0].price_eur).toFixed(2);
        this.statsCards[1].value = value.toFixed(2) + "PIV";

        axios.get("/api/token/PIVX").then(response => {
          var total = response.data.total;
          var ratio = 100 * value / total;
          this.rewardsDistribution.series = [ ratio, 100 - ratio ];
        });
      });
    });
  },
  components: {
    StatsCard,
    apexcharts: VueApexCharts
  },
  /**
   * Chart data used to render stats, charts. Should be replaced with server data
   */
  data() {
    return {
      user: this.$store.getters.getUserData,
      series: [
        {
          name: "series1",
          data: [31, 40, 28, 51, 42, 109, 100]
        }
      ],
      chartOptions: {
        colors: ['purple'],
        dataLabels: {
          enabled: false
        },
        stroke: {
          curve: "smooth"
        },

        xaxis: {
          // type: "datetime",
          categories: [
            "2018-01-19 00:00:00",
            "2018-03-19 01:30:00",
            "2018-05-19 02:30:00",
            "2018-07-19 03:30:00",
            "2018-09-19 04:30:00",
            "2018-11-19 05:30:00",
            "2018-12-19 06:30:00"
          ]
        },
        tooltip: {
          x: {
            format: "dd/MM/yy HH:mm"
          }
        }
      },
      rewardsDistribution: {
        series: [50, 50],
        options: {
          labels: ['Owned', 'Rest'],
          theme: {
            palette: 'palette10'
          },
          responsive: [{
            breakpoint: 480,
            options: {
              chart: {
                width: 200
              },
              legend: {
                position: 'bottom'
              }
            }
          }]
        }
      },

      tokens: [
        {
          name: "",
          token: ""
        }
      ],
      transactions: [
        {
          token: "",
          transactions: [
            {
              id: 0,
              user: 0,
              sender: null,
              value: 0,
              timestamp: "",
              comment: ""
            }
          ]
        }
      ],
      statsCards: [
        {
          type: "warning",
          icon: "cf cf-btc",
          title: "Bitcoin",
          value: "0BTC",
          footerText: "Updated now",
          footerIcon: "fas fa-euro-sign"
        },
        {
          type: "purple",
          icon: "cf cf-pivx",
          title: "PIVX",
          value: "0PIV",
          footerText: "",
          footerIcon: "fas fa-euro-sign"
        },
        {
          type: "danger",
          icon: "cf cf-xmr",
          title: "Monero",
          value: "0XMR",
          footerText: "Updated now",
          footerIcon: "fas fa-euro-sign"
        }
      ]
    };
  }
};
</script>
<style>
</style>
