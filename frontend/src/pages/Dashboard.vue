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
        <chart-card title="Users behavior"
                    sub-title="24 Hours performance"
                    :chart-data="usersChart.data"
                    :chart-options="usersChart.options">
          <span slot="footer">
            <i class="ti-reload"></i> Updated 3 minutes ago
          </span>
          <div slot="legend">
            <i class="fa fa-circle text-info">PIVX</i>
            <i class="fa fa-circle text-danger">XMR</i>
            <i class="fa fa-circle text-warning">BTC</i>
          </div>
        </chart-card>
      </div>

      <div class="col-md-6 col-12">
        <p v-for="t in tokens" :key="t.id">
          {{ t.name }}
        </p>
      </div>

    </div>

  </div>
</template>
<script>
import { StatsCard, ChartCard } from "@/components/index";
import Chartist from 'chartist';

import axios from 'axios';

export default {
  mounted() {
    axios.get("/api/tokens")
    .then(response => {
      this.tokens = response.data
    })
  },


  components: {
    StatsCard,
    ChartCard
  },
  /**
   * Chart data used to render stats, charts. Should be replaced with server data
   */
  data() {
    return {
      tokens: [
        {name: 'Bitcoin'},
        {name: 'PIVX'}
      ],
      statsCards: [
        {
          type: "warning",
          icon: "cf cf-btc",
          title: "Bitcoin",
          value: "105BTC"
        },
        {
          type: "info",
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
      ],
      usersChart: {
        data: {
          labels: [
            "9:00AM",
            "12:00AM",
            "3:00PM",
            "6:00PM",
            "9:00PM",
            "12:00PM",
            "3:00AM",
            "6:00AM"
          ],
          series: [
            [287, 385, 490, 562, 594, 626, 698, 895, 952],
            [67, 152, 193, 240, 387, 435, 535, 642, 744],
            [23, 113, 67, 108, 190, 239, 307, 410, 410]
          ]
        },
        options: {
          low: 0,
          high: 1000,
          showArea: true,
          height: "245px",
          axisX: {
            showGrid: false
          },
          lineSmooth: Chartist.Interpolation.simple({
            divisor: 3
          }),
          showLine: true,
          showPoint: false
        }
      }
    };
  }
};
</script>
<style>
</style>
