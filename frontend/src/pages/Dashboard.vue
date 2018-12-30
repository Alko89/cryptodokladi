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
        </stats-card>
      </div>
    </div>

    <!--Charts-->
    <div class="row">
      <div class="col-12">
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
        <p v-for="t in tokens" :key="t.id">{{ t.name }}</p>
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

    axios.get("/api/transactions/alko/PIVX").then(response => {
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

      this.chartOptions.xaxis.categories = labels;
      this.series = [
        {
          name: "PIVX",
          data: series
        }
      ];

      this.statsCards[1].value = value.toFixed(2) + "PIV"
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
            "2018-09-19T00:00:00",
            "2018-09-19T01:30:00",
            "2018-09-19T02:30:00",
            "2018-09-19T03:30:00",
            "2018-09-19T04:30:00",
            "2018-09-19T05:30:00",
            "2018-09-19T06:30:00"
          ]
        },
        tooltip: {
          x: {
            format: "dd/MM/yy HH:mm"
          }
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
          value: "105BTC"
        },
        {
          type: "purple",
          icon: "cf cf-pivx",
          title: "PIVX",
          value: "1,345PIV"
        },
        {
          type: "danger",
          icon: "cf cf-xmr",
          title: "Monero",
          value: "23XMR"
        },
        {
          type: "success",
          icon: "cf cf-doge",
          title: "SUM",
          value: "23€"
        }
      ]
    };
  }
};
</script>
<style>
</style>
